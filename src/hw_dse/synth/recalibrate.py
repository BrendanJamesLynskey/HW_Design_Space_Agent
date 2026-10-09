"""L5 back-annotation: refit the cost model to measured points, per tool.

The milestone-1 cost model has five free constants solved from two Vivado
anchors. Milestone 2 has many more *measured* points (open-source flow,
:mod:`hw_dse.synth.flow`) and will get Vivado points later. This module fits
the constants to all of them at once, without pretending the tools agree.

The model being fitted
----------------------
For a design x measured by tool T::

    LUTs_T(x)   = tau_T^lut  * ( c_arith[f] * arith_bits(x) + c_mux[f] * mux_luts(x) )
    FFs_T(x)    = tau_T^ff   *   c_ff[f]    * reg_bits(x)
    path_T(x)   = tau_T^path * ( fixed(x) + t_logic[f] * logic_levels(x) + t_mux[f] * mux_levels(x) )
    Fmax_T(x)   = 1000 / path_T(x)

* The structural counts (``arith_bits``, ``mux_luts``, ``reg_bits``, levels,
  the primitive delays inside ``fixed``) are exactly the M1 model's
  (:func:`hw_dse.models.cost_fpga.structure`); only constants are refitted.
* ``[f]``: ``c_arith``, ``c_ff`` and ``t_logic`` are fitted **per family**
  when that family has at least :data:`MIN_FAMILY_POINTS` measured points
  (about three per free parameter); otherwise the family shares the global
  value. The barrel-shifter terms ``c_mux``/``t_mux`` are always global:
  fitted per family they traded off against ``c_arith`` and generalised
  poorly (leave-one-out LUT error 24% for ``unrolled_k``).
* ``tau_T``: one multiplicative **per-tool correction** per metric. Vivado is
  the reference tool (``tau = 1``), so the fitted constants stay on the
  Vivado scale the default model and the eval use, and Yosys/nextpnr
  numbers inform the *shape* (how cost grows with W, N, k, m) without
  dragging the absolute scale to another tool's. When only open-source
  points exist besides the two anchors, the anchors alone fix the scale.
* Fit criterion: least squares on *relative* error (so a 2,000-LUT design
  does not dominate a 150-LUT one), with **every tool carrying the same total
  weight** (so 37 open-source points do not outvote the Vivado ones), by
  alternating between the linear constants (non-negative least squares) and
  the closed-form tool factors.
* The report includes a **leave-one-out** check: each generated-RTL point
  refitted without itself and predicted, the honest measure of how the
  refit generalises.

Which rows are fitted (:func:`split_rows`, :func:`refit`):

* The two calibration anchors were synthesised from the *reference* RTL.
  Vivado gives generated and reference RTL the same area within 4% but not
  the same Fmax (generated ``iterative`` -13%, ``pipelined`` +20%), so as
  soon as a CSV has a Vivado row for the generated equivalent of an anchor,
  that row replaces the anchor in the fit (the anchor is still reported).
* Vivado rows measured *post-route* are reported, not fitted: the anchors
  and the default model are on Vivado's post-synthesis timing scale.
* A design measured twice by the same tool and flow counts once.

Outputs (:func:`refit`, ``python -m hw_dse.synth.recalibrate``):

* a new named calibration YAML next to the default one (the default is never
  overwritten), with the constants, per-family overrides, tool factors and
  the provenance of every point;
* residuals at every measured point **before** (the M1 calibration as-is)
  and **after** the refit;
* the ground truth recomputed under the new calibration: does each spec's
  winner change, and which families reach a Pareto front.
"""

from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from hw_dse.families import ArchConfig
from hw_dse.models.cost_fpga import CALIBRATION_FILE, FpgaCostModel, _path_terms, anchor_arch, load_calibration, structure
from hw_dse.rtl.generator import REPO_ROOT
from hw_dse.synth.measured import MeasuredPoint, load

REFERENCE_TOOL = "vivado"
MIN_FAMILY_POINTS = 3 * len(("c_arith", "c_ff", "t_logic_ns"))  # ~3 points per free parameter
CONST_NAMES = ("c_arith", "c_mux", "c_ff", "t_logic_ns", "t_mux_ns")


def anchor_points(cal: dict[str, Any]) -> list[MeasuredPoint]:
    """The calibration's Vivado anchors as measured points (tool ``vivado``)."""
    out = []
    for a in cal["anchors"]:
        out.append(MeasuredPoint("vivado", "2025.2", cal["device"], "reference", anchor_arch(a), float(a["luts"]),
                                 float(a["ffs"]), float(a["fmax_mhz"]),
                                 extra={"fmax_kind": "post-synthesis (1000/(10-WNS))", "source_log": a["source"].strip()}))
    return out


def _nnls(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Tiny non-negative least squares: drop variables that go negative, re-solve."""
    active = list(range(a.shape[1]))
    x = np.zeros(a.shape[1])
    while active:
        sol, *_ = np.linalg.lstsq(a[:, active], b, rcond=None)
        if np.all(sol >= 0):
            x[:] = 0
            x[active] = sol
            return x
        active.pop(int(np.argmin(sol)))
    return x


@dataclass
class Fit:
    constants: dict[str, float]  # global
    per_family: dict[str, dict[str, float]]
    tau: dict[str, dict[str, float]]  # tool -> {"luts","ffs","path"}

    def calibration(self, base: dict[str, Any], name: str, points: list[MeasuredPoint], sources: list[str]) -> dict[str, Any]:
        cal = copy.deepcopy(base)
        cal["id"] = f"artix7-xc7a35t-refit-{name}"
        cal["fitted"] = {k: round(float(v), 6) for k, v in self.constants.items()}
        cal["fitted_per_family"] = {f: {k: round(float(v), 6) for k, v in d.items()} for f, d in self.per_family.items()}
        cal["tool_corrections"] = {t: {k: round(float(v), 6) for k, v in d.items()} for t, d in self.tau.items()}
        cal["refit"] = {
            "from_calibration": base["id"],
            "n_points": len(points),
            "points_by_tool": {t: sum(p.tool == t for p in points) for t in sorted({p.tool for p in points})},
            "sources": sources,
            "method": "hw_dse.synth.recalibrate: relative least squares, per-family constants where a family has "
                      f">= {MIN_FAMILY_POINTS} points, one multiplicative correction per tool and metric "
                      f"({REFERENCE_TOOL} = 1)",
        }
        return cal


def _features(p: MeasuredPoint, src: dict[str, float]) -> dict[str, float]:
    s = structure(p.arch)
    fixed, nl, nm = _path_terms(s, p.arch, src)
    return {"arith": s.arith_bits, "mux": s.mux_luts, "reg": s.reg_bits, "fixed": fixed, "nl": nl, "nm": nm}


PER_FAMILY_CONSTANTS = ("c_arith", "c_ff", "t_logic_ns")
"""Constants a family may override. The barrel-shifter terms (``c_mux``,
``t_mux_ns``) are always shared: only the two FSM families have them, and
fitting them per family let them trade off against ``c_arith``/``t_logic``
(collinear features), which generalised poorly in leave-one-out tests."""


def tool_weights(points: list[MeasuredPoint]) -> list[float]:
    """Every tool carries the same total weight, whatever its point count.

    Without this, 37 open-source points outvote 2 Vivado points 37:2 and the
    reference tool's own points end up far from its own scale.
    """
    n = {t: sum(p.tool == t for p in points) for t in {p.tool for p in points}}
    return [1.0 / n[p.tool] for p in points]


def _alternate(points: list[MeasuredPoint], feats: list[dict[str, float]], group: Any, coef: dict[str, dict[str, float]],
               free: dict[str, tuple[str, ...]], tau: dict[str, dict[str, float]], iters: int,
               weights: list[float]) -> dict[str, set[str]]:
    """Alternate (a) weighted non-negative LSQ for each group's *free*
    constants given the tool factors (the other constants are held fixed and
    move to the right-hand side) and (b) weighted closed-form tool factors
    given the constants. Returns, per group, the constants actually fitted."""
    fitted: dict[str, set[str]] = {g: set() for g in coef}
    sw = [math.sqrt(w) for w in weights]
    key = {"c_arith": "arith", "c_mux": "mux", "c_ff": "reg", "t_logic_ns": "nl", "t_mux_ns": "nm"}
    for _ in range(iters):
        for metric, cols, meas_of in (("luts", ("c_arith", "c_mux"), lambda p: p.luts), ("ffs", ("c_ff",), lambda p: p.ffs)):
            for g in coef:
                idx = [i for i, p in enumerate(points) if group(p) == g]
                use = [c for c in cols if c in free[g] and (c != "c_mux" or any(feats[i]["mux"] > 0 for i in idx))]
                if not idx or not use:
                    continue
                held = [c for c in cols if c not in use]
                A, b = [], []
                for i in idx:
                    s = tau[points[i].tool][metric] / meas_of(points[i])
                    A.append([sw[i] * s * feats[i][key[c]] for c in use])
                    b.append(sw[i] * (1.0 - s * sum(coef[g][c] * feats[i][key[c]] for c in held)))
                coef[g].update(dict(zip(use, _nnls(np.array(A), np.array(b)))))
                fitted[g].update(use)
        # path: tau*(fixed + nl*tl + nm*tm) = meas, rows relative to meas/tau
        for g in coef:
            idx = [i for i, p in enumerate(points) if group(p) == g and p.fmax_mhz]
            use = [c for c in ("t_logic_ns", "t_mux_ns") if c in free[g]
                   and (c != "t_mux_ns" or any(feats[i]["nm"] > 0 for i in idx))]
            if not idx or not use:
                continue
            held = [c for c in ("t_logic_ns", "t_mux_ns") if c not in use]
            rows, rhs = [], []
            for i in idx:
                tgt = 1000.0 / points[i].fmax_mhz / tau[points[i].tool]["path"]  # type: ignore[operator]
                rows.append([sw[i] * feats[i][key[c]] / tgt for c in use])
                rhs.append(sw[i] * (1.0 - (feats[i]["fixed"] + sum(coef[g][c] * feats[i][key[c]] for c in held)) / tgt))
            coef[g].update(dict(zip(use, _nnls(np.array(rows), np.array(rhs)))))
            fitted[g].update(use)
        pred = [_predict_raw(p, f, coef[group(p)]) for p, f in zip(points, feats)]
        for tl in tau:
            if tl == REFERENCE_TOOL:
                continue
            for metric, meas_of, k in (("luts", lambda p: p.luts, 0), ("ffs", lambda p: p.ffs, 1),
                                       ("path", lambda p: 1000.0 / p.fmax_mhz if p.fmax_mhz else None, 2)):
                rw = [(w, pr[k] / meas_of(p)) for p, pr, w in zip(points, pred, weights) if p.tool == tl and meas_of(p)]
                if rw:
                    tau[tl][metric] = sum(w * r for w, r in rw) / sum(w * r * r for w, r in rw)
    return fitted


def fit(points: list[MeasuredPoint], base: dict[str, Any], iters: int = 60) -> Fit:
    """Two passes, every tool weighted equally (:func:`tool_weights`):
    (1) one pooled set of all five constants -> the global constants;
    (2) for each family with at least MIN_FAMILY_POINTS points, its own
    ``c_arith``/``c_ff``/``t_logic_ns`` (:data:`PER_FAMILY_CONSTANTS`; the
    shifter terms stay global), refitting the tool factors alongside."""
    src = base["source_constants"]
    feats = [_features(p, src) for p in points]
    tools = sorted({p.tool for p in points})
    if REFERENCE_TOOL not in tools:
        raise ValueError("need at least one Vivado point (the calibration anchors) to fix the scale")
    w = tool_weights(points)
    tau = {t: {"luts": 1.0, "ffs": 1.0, "path": 1.0} for t in tools}
    pooled = {"_global": dict(base["fitted"])}
    _alternate(points, feats, lambda p: "_global", pooled, {"_global": CONST_NAMES}, tau, iters, w)
    glob = {k: float(v) for k, v in pooled["_global"].items()}
    fams = sorted({p.arch.family for p in points})
    per_fam = [f for f in fams if sum(p.arch.family == f for p in points) >= MIN_FAMILY_POINTS]
    coef = {"_global": dict(glob), **{f: dict(glob) for f in per_fam}}

    def group(p: MeasuredPoint) -> str:
        return p.arch.family if p.arch.family in per_fam else "_global"

    free = {"_global": (), **{f: PER_FAMILY_CONSTANTS for f in per_fam}}
    fitted = _alternate(points, feats, group, coef, free, tau, iters, w)
    per_family = {f: {k: float(coef[f][k]) for k in CONST_NAMES if k in fitted[f]} for f in per_fam}
    return Fit({k: glob[k] for k in CONST_NAMES}, per_family, tau)


def predict(f: Fit, p: MeasuredPoint, src: dict[str, float]) -> tuple[float, float, float | None]:
    """(LUTs, FFs, Fmax) the fit predicts for ``p`` on ``p.tool``'s scale."""
    c = {**f.constants, **f.per_family.get(p.arch.family, {})}
    t = f.tau.get(p.tool, {"luts": 1.0, "ffs": 1.0, "path": 1.0})
    luts, ffs, path = _predict_raw(p, _features(p, src), c)
    return luts * t["luts"], ffs * t["ffs"], 1000.0 / (path * t["path"])


def leave_one_out(points: list[MeasuredPoint], base: dict[str, Any], targets: list[int]) -> list[dict[str, Any]]:
    """Refit without each target point in turn and predict it: an
    out-of-sample check on how well the refit generalises."""
    src = base["source_constants"]
    out = []
    for i in targets:
        p = points[i]
        f = fit(points[:i] + points[i + 1:], base, iters=30)
        luts, ffs, fmax = predict(f, p, src)
        out.append({"family": p.arch.family, "key": p.arch.key(), "tool": p.tool,
                    "luts_err_pct": (luts / p.luts - 1) * 100, "ffs_err_pct": (ffs / p.ffs - 1) * 100,
                    "fmax_err_pct": (fmax / p.fmax_mhz - 1) * 100 if p.fmax_mhz else None})
    return out


def _predict_raw(p: MeasuredPoint, f: dict[str, float], c: dict[str, float]) -> tuple[float, float, float]:
    luts = c["c_arith"] * f["arith"] + c["c_mux"] * f["mux"]
    ffs = c["c_ff"] * f["reg"]
    path = f["fixed"] + f["nl"] * c["t_logic_ns"] + f["nm"] * c["t_mux_ns"]
    return luts, ffs, path


def residuals(points: list[MeasuredPoint], model: FpgaCostModel, tau: dict[str, dict[str, float]] | None = None) -> list[dict[str, Any]]:
    """Per point: model (x tool factor) vs measured, as % error."""
    out = []
    for p in points:
        e = model.estimate(p.arch)
        t = (tau or {}).get(p.tool, {"luts": 1.0, "ffs": 1.0, "path": 1.0})
        luts, ffs = e.area["luts"] * t["luts"], e.area["ffs"] * t["ffs"]
        fmax = 1000.0 / (e.critical_path_ns * t["path"])
        out.append({
            "tool": p.tool, "rtl_source": p.rtl_source, "key": p.arch.key(),
            "luts_meas": p.luts, "luts_model": round(luts, 1), "luts_err_pct": round((luts / p.luts - 1) * 100, 1),
            "ffs_meas": p.ffs, "ffs_model": round(ffs, 1), "ffs_err_pct": round((ffs / p.ffs - 1) * 100, 1) if p.ffs else None,
            "fmax_meas": p.fmax_mhz, "fmax_model": round(fmax, 1),
            "fmax_err_pct": round((fmax / p.fmax_mhz - 1) * 100, 1) if p.fmax_mhz else None,
        })
    return out


def _rms(xs: list[float | None]) -> float:
    v = [x for x in xs if x is not None]
    return math.sqrt(sum(x * x for x in v) / len(v)) if v else float("nan")


def summary_by_tool(res: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    out = {}
    for t in sorted({(r["tool"], r["rtl_source"]) for r in res}):
        rs = [r for r in res if (r["tool"], r["rtl_source"]) == t]
        out[f"{t[0]} ({t[1]} RTL)"] = {"n": len(rs), **{f"rms_{m}_err_pct": round(_rms([r[f"{m}_err_pct"] for r in rs]), 1)
                                                      for m in ("luts", "ffs", "fmax")}}
    return out


def ground_truth_impact(cal_path: Path, specs_dir: Path | None = None) -> dict[str, Any]:
    """Recompute every spec's ground truth under ``cal_path`` vs the committed one."""
    from hw_dse import accuracy_table
    from hw_dse.benchmark import build_grid, ground_truth
    from hw_dse.spec import load_spec

    accuracy_table.preload()
    old = json.loads((REPO_ROOT / "eval" / "data" / "ground_truth.json").read_text())
    model = FpgaCostModel(str(cal_path))
    grid = build_grid(cost_model=model)
    out = {}
    for sp in sorted((specs_dir or REPO_ROOT / "specs").glob("*.yaml")):
        s = load_spec(sp)
        gt = ground_truth(grid, s, model)
        new_sel = gt["selected"]["key"] if gt["selected"] else None
        old_sel = old[s.name]["selected"]["key"] if old[s.name]["selected"] else None
        fams: dict[str, int] = {}
        for r in gt["front"]:
            fams[r["family"]] = fams.get(r["family"], 0) + 1
        out[s.name] = {"winner_m1": old_sel, "winner_refit": new_sel, "winner_changed": new_sel != old_sel,
                       "feasible_m1": old[s.name]["n_feasible"], "feasible_refit": gt["n_feasible"],
                       "front_families_refit": fams,
                       "best_throughput_refit": round(gt["best_throughput_msps_any"], 1)}
    return out


def is_post_route(p: MeasuredPoint) -> bool:
    return p.extra.get("fmax_kind", "").strip().lower().startswith("post-route")


def split_rows(measured_csvs: list[Path]) -> tuple[list[MeasuredPoint], list[MeasuredPoint], list[dict[str, str]]]:
    """Load every CSV; return (rows to fit, report-only rows, duplicates dropped).

    * The calibration anchors and the eval's cost model are on Vivado's
      *post-synthesis* scale, so Vivado rows measured post-route are
      reported (as tool ``vivado post-route``, no tool factor) but not fitted.
    * The same design measured twice by the same tool and flow (e.g. the
      review's spot-check and the full Vivado run) is counted once: the row
      from the CSV given first wins.
    """
    seen: dict[tuple[str, str, str, bool], str] = {}
    fit_rows, report_only, dropped = [], [], []
    for c in measured_csvs:
        for p in load(c):
            k = (p.tool, p.rtl_source, p.arch.key(), is_post_route(p))
            if k in seen:
                dropped.append({"tool": p.tool, "key": p.arch.key(), "csv": c.name, "kept_from": seen[k]})
                continue
            seen[k] = c.name
            if p.tool == REFERENCE_TOOL and is_post_route(p):
                report_only.append(dataclasses.replace(p, tool=f"{REFERENCE_TOOL} post-route"))
            else:
                fit_rows.append(p)
    return fit_rows, report_only, dropped


def refit(measured_csvs: list[Path], name: str, base_path: Path = CALIBRATION_FILE, impact: bool = True,
          include_reference_rtl: bool = False) -> dict[str, Any]:
    base = load_calibration(str(base_path))
    pts_all, report_only, dropped = split_rows(measured_csvs)
    # Open-source rows synthesised from the *reference* RTL measure Yosys's
    # handling of that RTL, not the generated designs we explore: reported,
    # not fitted (unless asked).
    # The calibration's Vivado anchors were synthesised from the *reference*
    # RTL. Once Vivado has measured the *generated* equivalent of an anchor,
    # that row replaces it (a spot-check found +20% Fmax on generated RTL).
    viv_gen = {p.arch.key() for p in pts_all if p.tool == REFERENCE_TOOL and p.rtl_source == "generated"}
    anchors = [a for a in anchor_points(base) if a.arch.key() not in viv_gen]
    fit_pts = anchors + [p for p in pts_all if p.rtl_source == "generated" or include_reference_rtl]
    f = fit(fit_pts, base)
    loo_idx = [i for i, p in enumerate(fit_pts) if p.rtl_source == "generated"]
    loo = leave_one_out(fit_pts, base, loo_idx) if loo_idx else []
    cal = f.calibration(base, name, fit_pts, [str(c.relative_to(REPO_ROOT)) if c.is_absolute() and REPO_ROOT in c.parents
                                              else str(c) for c in measured_csvs])
    out_path = base_path.with_name(f"calibration_artix7_refit_{name}.yaml")
    header = (f"# Refitted calibration '{name}' written by hw_dse.synth.recalibrate -- NOT the default.\n"
              f"# The default cost model still uses {base_path.name}. Load this one with\n"
              f"#   FpgaCostModel('{out_path.relative_to(REPO_ROOT)}')\n")
    out_path.write_text(header + yaml.safe_dump(cal, sort_keys=False, width=110))
    eval_pts = anchor_points(base) + pts_all + report_only
    before = residuals(eval_pts, FpgaCostModel(str(base_path)))
    after = residuals(eval_pts, FpgaCostModel(str(out_path)), f.tau)
    report: dict[str, Any] = {
        "name": name, "calibration_file": str(out_path.relative_to(REPO_ROOT)), "base": base["id"],
        "constants_m1": base["fitted"], "constants_refit": cal["fitted"], "per_family": cal["fitted_per_family"],
        "tool_corrections": cal["tool_corrections"], "n_fit_points": len(fit_pts),
        "summary_before": summary_by_tool(before), "summary_after": summary_by_tool(after),
        "residuals_before": before, "residuals_after": after,
        "anchors_used": [a.arch.key() for a in anchors],
        "report_only": [f"{p.tool}: {p.arch.key()}" for p in report_only], "duplicates_dropped": dropped,
        "leave_one_out": loo, "loo_summary": _loo_summary(loo, after, fit_pts, loo_idx),
    }
    if impact:
        report["ground_truth_impact"] = ground_truth_impact(out_path)
    return report


def _loo_summary(loo: list[dict[str, Any]], after: list[dict[str, Any]], fit_pts: list[MeasuredPoint],
                 loo_idx: list[int]) -> dict[str, dict[str, Any]]:
    """In-sample vs leave-one-out RMS % error per family (generated-RTL points)."""
    ins = {(r["tool"], r["key"], r["rtl_source"]): r for r in after}
    out: dict[str, dict[str, Any]] = {}
    tools = sorted({r["tool"] for r in loo})
    groups = ["all", *([f"all {t}" for t in tools] if len(tools) > 1 else []), *sorted({r["family"] for r in loo})]
    for fam in groups:
        rows = [r for r in loo if fam in ("all", r["family"], f"all {r['tool']}")]
        insample = [ins[(r["tool"], r["key"], "generated")] for r in rows]
        out[fam] = {"n": len(rows), **{f"{m}_in": round(_rms([x[f"{m}_err_pct"] for x in insample]), 1)
                                       for m in ("luts", "ffs", "fmax")},
                    **{f"{m}_loo": round(_rms([x[f"{m}_err_pct"] for x in rows]), 1) for m in ("luts", "ffs", "fmax")}}
    return out


def markdown(rep: dict[str, Any]) -> str:
    L = [f"# L5 refit `{rep['name']}`\n",
         f"Generated by `python -m hw_dse.synth.recalibrate`. New calibration: `{rep['calibration_file']}` "
         f"(fitted on {rep['n_fit_points']} points). The default cost model is unchanged (`{rep['base']}`).\n",
         "## Constants\n", "| constant | M1 (2 anchors) | refit (global) |", "|---|---|---|"]
    for k in CONST_NAMES:
        L.append(f"| {k} | {rep['constants_m1'][k]:.4f} | {rep['constants_refit'][k]:.4f} |")
    L.append("\nPer-family overrides: " + (", ".join(f"`{f}`: " + ", ".join(f"{k}={v:.4f}" for k, v in d.items())
                                                for f, d in rep["per_family"].items()) or "none"))
    L.append("\nTool corrections (measured ≈ factor × model, Vivado = 1): " + "; ".join(
        f"`{t}`: LUT ×{d['luts']:.3f}, FF ×{d['ffs']:.3f}, path ×{d['path']:.3f}" for t, d in rep["tool_corrections"].items()))
    L.append("\nFit: every tool carries equal total weight; per-family overrides only for c_arith, c_ff and "
             f"t_logic_ns, for families with >= {MIN_FAMILY_POINTS} points. Vivado anchors used: "
             + (", ".join(f"`{k}`" for k in rep.get("anchors_used", [])) or "none (superseded by generated-RTL Vivado rows)"))
    if rep.get("report_only"):
        L.append(f"\nReported, not fitted: {len(rep['report_only'])} Vivado post-route rows (tool `vivado post-route`; "
                 "the anchors and the default model are post-synthesis), shown with no tool factor.")
    for d in rep.get("duplicates_dropped", []):
        L.append(f"\nCounted once: `{d['key']}` ({d['tool']}) is in both `{d['kept_from']}` (kept) and `{d['csv']}` (dropped).")
    if rep.get("loo_summary"):
        L.append("\n## Out-of-sample check: leave-one-out RMS error (generated-RTL points)\n")
        L.append("Each point refitted without itself and predicted on its own tool's scale; in-sample → leave-one-out.\n")
        L.append("| family | points | LUT | FF | Fmax |")
        L.append("|---|---|---|---|---|")
        for fam, s in rep["loo_summary"].items():
            L.append(f"| {fam} | {s['n']} | {s['luts_in']} → {s['luts_loo']}% | {s['ffs_in']} → {s['ffs_loo']}% | "
                     f"{s['fmax_in']} → {s['fmax_loo']}% |")
    L.append("\n## RMS error by tool (before = M1 calibration as-is, no tool correction; after = refit × tool factor)\n")
    L.append("| tool (RTL) | points | LUT before | LUT after | FF before | FF after | Fmax before | Fmax after |")
    L.append("|---|---|---|---|---|---|---|---|")
    for t, b in rep["summary_before"].items():
        a = rep["summary_after"][t]
        L.append(f"| {t} | {b['n']} | {b['rms_luts_err_pct']}% | {a['rms_luts_err_pct']}% | {b['rms_ffs_err_pct']}% | "
                 f"{a['rms_ffs_err_pct']}% | {b['rms_fmax_err_pct']}% | {a['rms_fmax_err_pct']}% |")
    L.append("\n## Residuals at every measured point\n")
    L.append("| tool | RTL | design | LUT meas | LUT M1 (err) | LUT refit (err) | FF meas | FF M1 (err) | FF refit (err) | "
             "Fmax meas | Fmax M1 (err) | Fmax refit (err) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for b, a in zip(rep["residuals_before"], rep["residuals_after"]):
        def cell(r: dict[str, Any], m: str) -> str:
            return "—" if r[f"{m}_err_pct"] is None else f"{r[f'{m}_model']:.0f} ({r[f'{m}_err_pct']:+.0f}%)"
        fm = "—" if b["fmax_meas"] is None else f"{b['fmax_meas']:.1f}"
        L.append(f"| {b['tool']} | {b['rtl_source']} | `{b['key']}` | {b['luts_meas']:.0f} | {cell(b, 'luts')} | {cell(a, 'luts')} | "
                 f"{b['ffs_meas']:.0f} | {cell(b, 'ffs')} | {cell(a, 'ffs')} | {fm} | {cell(b, 'fmax')} | {cell(a, 'fmax')} |")
    if "ground_truth_impact" in rep:
        L.append("\n## Ground truth under the refit calibration\n")
        L.append("| spec | winner (M1 calibration) | winner (refit) | changed? | feasible designs M1 → refit | families on the refit front |")
        L.append("|---|---|---|---|---|---|")
        for s, g in rep["ground_truth_impact"].items():
            L.append(f"| {s} | `{g['winner_m1']}` | `{g['winner_refit']}` | {'**yes**' if g['winner_changed'] else 'no'} | "
                     f"{g['feasible_m1']:,} → {g['feasible_refit']:,} | "
                     f"{', '.join(f'{k} ({v})' for k, v in g['front_families_refit'].items()) or 'none'} |")
    return "\n".join(L) + "\n"


def main() -> None:  # pragma: no cover - CLI
    ap = argparse.ArgumentParser(description="Refit the Artix-7 cost model to measured points (L5).")
    ap.add_argument("--measured", action="append", required=True, help="measured-points CSV (repeatable)")
    ap.add_argument("--name", required=True, help="name of the new calibration, e.g. yosys-nextpnr or vivado-2025.2")
    ap.add_argument("--no-impact", action="store_true", help="skip the ground-truth recomputation (~20 s)")
    args = ap.parse_args()
    rep = refit([Path(m).resolve() for m in args.measured], args.name, impact=not args.no_impact)
    out = REPO_ROOT / "eval" / "data" / f"l5_refit_{args.name}"
    # not with_suffix(): a name like "vivado-2025.2" already contains a dot
    out.with_name(out.name + ".json").write_text(json.dumps(rep, indent=1))
    out.with_name(out.name + ".md").write_text(markdown(rep))
    print(markdown(rep).split("## Residuals")[0])
    if "ground_truth_impact" in rep:
        for s, g in rep["ground_truth_impact"].items():
            print(f"{s}: winner {'CHANGES' if g['winner_changed'] else 'unchanged'} "
                  f"({g['winner_m1']} -> {g['winner_refit']}); front families {g['front_families_refit']}")
    print(f"wrote {out}.md/.json and {rep['calibration_file']}")


if __name__ == "__main__":  # pragma: no cover
    main()
