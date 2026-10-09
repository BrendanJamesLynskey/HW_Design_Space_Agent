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
* ``[f]``: a constant is fitted **per family** when that family has at least
  :data:`MIN_FAMILY_POINTS` measured points (any tool); otherwise the family
  shares the global value. (Pipelined families have no mux terms, so
  ``c_mux``/``t_mux`` are never fitted for them.)
* ``tau_T``: one multiplicative **per-tool correction** per metric. Vivado is
  the reference tool (``tau = 1``), so the fitted constants stay on the
  Vivado scale the default model and the eval use, and Yosys/nextpnr
  numbers inform the *shape* (how cost grows with W, N, k, m) without
  dragging the absolute scale to another tool's. When only open-source
  points exist besides the two anchors, the anchors alone fix the scale.
* Fit criterion: least squares on *relative* error (so a 2,000-LUT design
  does not dominate a 150-LUT one), by alternating between the linear
  constants (non-negative least squares) and the closed-form tool factors.

Assumption to be tested by the Vivado PR: the two Vivado anchors were
synthesised from the *reference* RTL, while every other point uses the
*generated* RTL. The fit treats the anchors as Vivado-on-generated (the
generated modules are bit-identical and structurally the same datapath).
Yosys's own reference-vs-generated ratio is reported separately; the
recommended Vivado points therefore include the two generated anchors.

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
MIN_FAMILY_POINTS = 5
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


def _alternate(points: list[MeasuredPoint], feats: list[dict[str, float]], group: Any, coef: dict[str, dict[str, float]],
               fixed: set[str], tau: dict[str, dict[str, float]], iters: int) -> dict[str, set[str]]:
    """Alternate (a) non-negative LSQ for each free group's constants given the
    tool factors and (b) closed-form tool factors given the constants.
    Returns, per group, the names of the constants that were actually fitted."""
    fitted: dict[str, set[str]] = {g: set() for g in coef}
    for _ in range(iters):
        for metric, cols, meas_of in (("luts", ("c_arith", "c_mux"), lambda p: p.luts), ("ffs", ("c_ff",), lambda p: p.ffs)):
            for g in coef:
                if g in fixed:
                    continue
                idx = [i for i, p in enumerate(points) if group(p) == g]
                if not idx:
                    continue
                use = [c for c in cols if c != "c_mux" or any(feats[i]["mux"] > 0 for i in idx)]
                key = {"c_arith": "arith", "c_mux": "mux", "c_ff": "reg"}
                A = np.array([[tau[points[i].tool][metric] * feats[i][key[c]] / meas_of(points[i]) for c in use] for i in idx])
                coef[g].update(dict(zip(use, _nnls(A, np.ones(len(idx))))))
                fitted[g].update(use)
        # path: tau*(fixed + nl*tl + nm*tm) = meas  ->  rows relative to meas/tau
        for g in coef:
            if g in fixed:
                continue
            idx = [i for i, p in enumerate(points) if group(p) == g and p.fmax_mhz]
            if not idx:
                continue
            use = ["t_logic_ns"] + (["t_mux_ns"] if any(feats[i]["nm"] > 0 for i in idx) else [])
            key = {"t_logic_ns": "nl", "t_mux_ns": "nm"}
            rows, rhs = [], []
            for i in idx:
                tgt = 1000.0 / points[i].fmax_mhz / tau[points[i].tool]["path"]  # type: ignore[operator]
                rows.append([feats[i][key[c]] / tgt for c in use])
                rhs.append(1.0 - feats[i]["fixed"] / tgt)
            coef[g].update(dict(zip(use, _nnls(np.array(rows), np.array(rhs)))))
            fitted[g].update(use)
        pred = [_predict_raw(p, f, coef[group(p)]) for p, f in zip(points, feats)]
        for tl in tau:
            if tl == REFERENCE_TOOL:
                continue
            for metric, meas_of, k in (("luts", lambda p: p.luts, 0), ("ffs", lambda p: p.ffs, 1),
                                       ("path", lambda p: 1000.0 / p.fmax_mhz if p.fmax_mhz else None, 2)):
                r = [pr[k] / meas_of(p) for p, pr in zip(points, pred) if p.tool == tl and meas_of(p)]
                if r:
                    tau[tl][metric] = sum(r) / sum(x * x for x in r)
    return fitted


def fit(points: list[MeasuredPoint], base: dict[str, Any], iters: int = 60) -> Fit:
    """Two passes: (1) one pooled set of constants for every family -> the
    global constants; (2) per-family constants for each family with at least
    MIN_FAMILY_POINTS points (other families keep the global ones), refitting
    the tool factors alongside."""
    src = base["source_constants"]
    feats = [_features(p, src) for p in points]
    tools = sorted({p.tool for p in points})
    if REFERENCE_TOOL not in tools:
        raise ValueError("need at least one Vivado point (the calibration anchors) to fix the scale")
    tau = {t: {"luts": 1.0, "ffs": 1.0, "path": 1.0} for t in tools}
    pooled = {"_global": dict(base["fitted"])}
    _alternate(points, feats, lambda p: "_global", pooled, set(), tau, iters)
    glob = {k: float(v) for k, v in pooled["_global"].items()}
    fams = sorted({p.arch.family for p in points})
    per_fam = [f for f in fams if sum(p.arch.family == f for p in points) >= MIN_FAMILY_POINTS]
    coef = {"_global": dict(glob), **{f: dict(glob) for f in per_fam}}

    def group(p: MeasuredPoint) -> str:
        return p.arch.family if p.arch.family in per_fam else "_global"

    fitted = _alternate(points, feats, group, coef, {"_global"}, tau, iters)
    per_family = {f: {k: float(coef[f][k]) for k in CONST_NAMES if k in fitted[f]} for f in per_fam}
    return Fit({k: glob[k] for k in CONST_NAMES}, per_family, tau)


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
    grid = build_grid(cost_model=FpgaCostModel(str(cal_path)))
    out = {}
    for sp in sorted((specs_dir or REPO_ROOT / "specs").glob("*.yaml")):
        s = load_spec(sp)
        gt = ground_truth(grid, s)
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


def refit(measured_csvs: list[Path], name: str, base_path: Path = CALIBRATION_FILE, impact: bool = True,
          include_reference_rtl: bool = False) -> dict[str, Any]:
    base = load_calibration(str(base_path))
    pts_all = [p for c in measured_csvs for p in load(c)]
    # Open-source rows synthesised from the *reference* RTL measure Yosys's
    # handling of that RTL, not the generated designs we explore: reported,
    # not fitted (unless asked).
    fit_pts = anchor_points(base) + [p for p in pts_all if p.rtl_source == "generated" or include_reference_rtl
                                     or p.tool == REFERENCE_TOOL]
    f = fit(fit_pts, base)
    cal = f.calibration(base, name, fit_pts, [str(c.relative_to(REPO_ROOT)) if c.is_absolute() and REPO_ROOT in c.parents
                                              else str(c) for c in measured_csvs])
    out_path = base_path.with_name(f"calibration_artix7_refit_{name}.yaml")
    header = (f"# Refitted calibration '{name}' written by hw_dse.synth.recalibrate -- NOT the default.\n"
              f"# The default cost model still uses {base_path.name}. Load this one with\n"
              f"#   FpgaCostModel('{out_path.relative_to(REPO_ROOT)}')\n")
    out_path.write_text(header + yaml.safe_dump(cal, sort_keys=False, width=110))
    eval_pts = anchor_points(base) + pts_all
    before = residuals(eval_pts, FpgaCostModel(str(base_path)))
    after = residuals(eval_pts, FpgaCostModel(str(out_path)), f.tau)
    report: dict[str, Any] = {
        "name": name, "calibration_file": str(out_path.relative_to(REPO_ROOT)), "base": base["id"],
        "constants_m1": base["fitted"], "constants_refit": cal["fitted"], "per_family": cal["fitted_per_family"],
        "tool_corrections": cal["tool_corrections"], "n_fit_points": len(fit_pts),
        "summary_before": summary_by_tool(before), "summary_after": summary_by_tool(after),
        "residuals_before": before, "residuals_after": after,
    }
    if impact:
        report["ground_truth_impact"] = ground_truth_impact(out_path)
    return report


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
    out.with_suffix(".json").write_text(json.dumps(rep, indent=1))
    out.with_suffix(".md").write_text(markdown(rep))
    print(markdown(rep).split("## Residuals")[0])
    if "ground_truth_impact" in rep:
        for s, g in rep["ground_truth_impact"].items():
            print(f"{s}: winner {'CHANGES' if g['winner_changed'] else 'unchanged'} "
                  f"({g['winner_m1']} -> {g['winner_refit']}); front families {g['front_families_refit']}")
    print(f"wrote {out}.md/.json and {rep['calibration_file']}")


if __name__ == "__main__":  # pragma: no cover
    main()
