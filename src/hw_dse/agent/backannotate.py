"""The L5 hook in the agent graph: check the selected design against measured data.

After ``select`` picks a design off the *estimated* Pareto front, the
``back_annotate`` node asks: do real implementation results agree?

1. **Find measured data** for the selected design: rows of the
   measured-points CSVs (:mod:`hw_dse.synth.measured`; by default the
   committed open-source L4 sweep, ``eval/data/l4_synthesis.csv``) whose
   design key matches, from generated RTL. If there is none and the run was
   configured with ``synthesize=True`` and the toolchain is available, the
   node *produces* it by running the L4 flow on the selected design (one
   nextpnr seed).
2. **Compare** measured LUTs, FFs and Fmax with the estimates, per tool, as
   percentage differences. Numbers keep their provenance: the estimate is
   ``estimate: cost_fpga (...)``, the measurement ``measured (<tool> <ver>)``.
3. **Flag a winner change.** Every front design with measured data is
   re-evaluated with its measured numbers, converted to the Vivado scale the
   cost model uses by the per-tool factors of a refit calibration
   (:mod:`hw_dse.synth.recalibrate`) when one is given. If the selected
   design becomes infeasible, or the spec's selection rule now prefers
   another measured front design, the node raises ``winner_changed`` and
   says why. (It cannot see designs that have no measurement, and says so.)

The node never calls the LLM and never changes the selection: it reports.
Everything it needs can come from recorded CSVs, so it is tested offline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hw_dse.benchmark import select_design
from hw_dse.evaluate import default_cost_model, evaluate
from hw_dse.families import ArchConfig, REGISTRY
from hw_dse.models.cost_base import CostEstimate
from hw_dse.rtl.generator import REPO_ROOT
from hw_dse.spec import Spec

DEFAULT_MEASURED = [REPO_ROOT / "eval" / "data" / "l4_synthesis.csv"]
DEFAULT_REFIT = REPO_ROOT / "src" / "hw_dse" / "models" / "calibration_artix7_refit_yosys-nextpnr.yaml"


class _MeasuredCost:
    """A one-design 'cost model' that returns measured numbers (scaled by tool factors)."""

    name = "measured"
    target = "fpga"

    def __init__(self, luts: float, ffs: float, fmax: float, provenance: str) -> None:
        cm = default_cost_model()
        self.calibration_id = provenance
        self.power_norm = cm.power_norm
        self._est = CostEstimate(area={"luts": luts, "ffs": ffs}, fmax_mhz=fmax, critical_path_ns=1000.0 / fmax,
                                 switching_resources=luts + ffs, activity_factor=cm.src["activity_factor"],
                                 provenance=provenance)

    def estimate(self, arch: ArchConfig) -> CostEstimate:  # noqa: ARG002 - one design only
        return self._est


def _arch_of(rec: dict[str, Any]) -> ArchConfig:
    names = [p.name for p in REGISTRY[rec["family"]].params]
    return ArchConfig.from_params(rec["family"], {n: rec[n] for n in names})


def load_index(csvs: list[Path]) -> dict[str, list[Any]]:
    from hw_dse.synth.measured import load

    idx: dict[str, list[Any]] = {}
    for c in csvs:
        if Path(c).exists():
            for p in load(c):
                if p.rtl_source == "generated" and p.fmax_mhz:
                    idx.setdefault(p.arch.key(), []).append(p)
    return idx


def tool_factors(calibration: Path | None) -> dict[str, dict[str, float]]:
    if calibration is None or not Path(calibration).exists():
        return {}
    import yaml

    return (yaml.safe_load(Path(calibration).read_text()) or {}).get("tool_corrections") or {}


def _measured_record(p: Any, spec: Spec, factors: dict[str, dict[str, float]]) -> dict[str, Any]:
    f = factors.get(p.tool)
    luts, ffs, fmax = p.luts, p.ffs, float(p.fmax_mhz)
    prov = p.provenance
    if f:
        luts, ffs, fmax = luts / f["luts"], ffs / f["ffs"], fmax * f["path"]
        prov += f", scaled to the Vivado scale by tool factors LUT/{f['luts']:.3f} FF/{f['ffs']:.3f} path/{f['path']:.3f}"
    return evaluate(p.arch, spec, cost_model=_MeasuredCost(luts, ffs, fmax, prov))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Milestone 4: the ASIC target is back-annotated against its own measurements
# ---------------------------------------------------------------------------

ASIC_MEASURED = [REPO_ROOT / "eval" / "data" / "asic_synthesis.csv", REPO_ROOT / "eval" / "data" / "asic_validation.csv"]


class _MeasuredAsicCost:
    """One ASIC design's measured area, FFs and Fmax as a 'cost model'; the power
    index uses the default model's fitted weights on the measured counts."""

    name = "measured"
    target = "asic"

    def __init__(self, p: Any) -> None:
        from hw_dse.evaluate import default_asic_cost_model

        cm = default_asic_cost_model()
        self.calibration_id = p.provenance
        self.power_norm = cm.power_norm
        w = cm.fit
        self._est = CostEstimate(area={"area_um2": p.area_um2, "gate_eq": p.gate_eq, "ffs": p.ffs},
                                 fmax_mhz=float(p.fmax_mhz), critical_path_ns=float(p.critical_path_ns),
                                 switching_resources=w["w_ff"] * p.ffs + w["w_area"] * p.area_um2,
                                 activity_factor=cm.src["activity_factor"], provenance=p.provenance)

    def estimate(self, arch: ArchConfig) -> CostEstimate:  # noqa: ARG002 - one design only
        return self._est


def back_annotate_asic(spec: Spec, front: list[dict[str, Any]], selected: dict[str, Any],
                       opts: dict[str, Any]) -> dict[str, Any]:
    """ASIC version of :func:`back_annotate`: the committed sky130 measurements
    (calibration sweep + held-out validation set), never the FPGA ones. Compares
    area, FFs and Fmax, re-checks feasibility of every measured front design with
    its measured numbers (system metrics simulated at the measured clock) and
    flags a winner change. There is no separate ASIC refit to re-explore under
    (the default ASIC model *is* the fit to these points), so the L5 loop does
    not run: ``reexplore_available`` is False and the report says so."""
    from hw_dse.synth.asic import load_csv

    csvs = [Path(c) for c in (opts.get("asic_measured_csvs") or ASIC_MEASURED)]
    idx: dict[str, Any] = {}
    for c in csvs:
        if c.exists():
            for p in load_csv(c):
                idx.setdefault(p.arch.key(), p)

    def measured_rec(p: Any) -> dict[str, Any]:
        r = evaluate(p.arch, spec, cost_model=_MeasuredAsicCost(p))  # type: ignore[arg-type]
        if spec.system is not None:
            from hw_dse.l2.node import simulate_record

            r = simulate_record(r, spec)
        return r

    key = selected["key"]
    out: dict[str, Any] = {"status": "no_measured_data", "target": "asic", "selected_key": key,
                           "produced_by_synthesis": False, "measured_sources": [str(c) for c in csvs],
                           "comparisons": [], "winner_changed": False, "reexplore_available": False,
                           "notes": ["ASIC target: no refit calibration to re-explore under; a flagged winner "
                                     "change is reported, not acted on"]}
    if key not in idx:
        out["notes"].append("no measured data for the selected design; nothing to compare")
        return out
    p = idx[key]
    out["status"] = "compared"
    cmp: dict[str, Any] = {"tool": p.row["tool"], "tool_version": p.row["tool_version"], "provenance": p.provenance}
    for m, meas in (("area_um2", p.area_um2), ("ffs", p.ffs), ("fmax_mhz", p.fmax_mhz)):
        est = float(selected[m])
        cmp[m] = {"estimate": round(est, 1), "measured": meas, "diff_pct": round((float(meas) / est - 1) * 100, 1)}
    out["comparisons"].append(cmp)
    mfront = [measured_rec(idx[r["key"]]) for r in front if r["key"] in idx]
    sel = next((m for m in mfront if m["key"] == key), None) or measured_rec(p)
    best = select_design(mfront + ([sel] if sel not in mfront else []), spec)
    out["n_front_designs"] = len(front)
    out["n_front_designs_measured"] = len({m["key"] for m in mfront})
    if not sel["feasible"]:
        out["winner_changed"] = True
        out["why"] = "the selected design violates the spec with measured numbers: " + "; ".join(
            f"{k} by {v * 100:.1f}%" for k, v in sel["violations"].items() if v > 0)
    elif best is not None and best["key"] != key:
        out["winner_changed"] = True
        out["why"] = (f"with measured numbers the spec's rule prefers {best['key']} "
                      f"({spec.select_by} {best[spec.select_by]:.4g} vs {sel[spec.select_by]:.4g})")
    else:
        out["why"] = "the selected design is still the best measured front design" + (
            "" if out["n_front_designs_measured"] > 1 else " (it is the only front design with measurements)")
    out["winner_checks"] = [{"tool": p.row["tool"], "winner_changed": out["winner_changed"], "why": out["why"],
                             "n_front_designs_measured": out["n_front_designs_measured"]}]
    return out


def back_annotate(spec: Spec, front: list[dict[str, Any]], selected: dict[str, Any] | None,
                  options: dict[str, Any] | None = None) -> dict[str, Any]:
    """The node's logic, as a pure function of the run's front and selection."""
    opts = options or {}
    if opts.get("enabled") is False or selected is None:
        return {"status": "skipped", "reason": "disabled" if selected else "no design selected"}
    if spec.target_kind == "asic":
        return back_annotate_asic(spec, front, selected, opts)
    csvs = [Path(c) for c in (opts.get("measured_csvs") or DEFAULT_MEASURED)]
    calib = opts.get("calibration", DEFAULT_REFIT)
    factors = tool_factors(Path(calib) if calib else None)
    idx = load_index(csvs)
    notes: list[str] = []
    key = selected["key"]
    produced = False
    if key not in idx and opts.get("synthesize"):
        from hw_dse.synth.flow import Runner, synthesize_arch
        from hw_dse.synth.measured import MeasuredPoint

        runner = Runner.from_env()
        ok, why = runner.available()
        if ok:
            r = synthesize_arch(_arch_of(selected), runner, pnr=True, seed=1)
            v = runner.versions(Path(r.workdir))
            idx[key] = [MeasuredPoint("yosys+nextpnr-xilinx", f"yosys {v['yosys']} + nextpnr-xilinx {v['nextpnr']}",
                                      "xc7a35tcpg236-1", "generated", _arch_of(selected), float(r.luts), float(r.ffs),
                                      r.fmax_mhz, float(r.carry4), {"fmax_kind": "post-route, seed 1"})]
            produced = True
        else:
            notes.append(f"synthesis requested but unavailable: {why}")
    out: dict[str, Any] = {"status": "no_measured_data", "selected_key": key, "produced_by_synthesis": produced,
                           "measured_sources": [str(c) for c in csvs], "tool_factors_from": str(calib) if factors else None,
                           "comparisons": [], "winner_changed": False, "notes": notes}
    if key not in idx:
        out["notes"].append("no measured data for the selected design; nothing to compare")
        return out
    out["status"] = "compared"
    for p in idx[key]:
        f = factors.get(p.tool)
        cmp: dict[str, Any] = {"tool": p.tool, "tool_version": p.tool_version, "provenance": p.provenance,
                               "tool_factors_applied": bool(f)}
        for m, meas, fk in (("luts", p.luts, "luts"), ("ffs", p.ffs, "ffs"), ("fmax_mhz", p.fmax_mhz, "path")):
            est = float(selected[m])
            # diff_pct: the tool's raw number vs the (Vivado-scale) estimate.
            # diff_pct_scaled: the same number first converted to the Vivado
            # scale by the tool's refit factor -- the like-for-like view, and
            # the one the winner check below uses.
            scaled = meas if not f else (meas * f["path"] if fk == "path" else meas / f[fk])
            cmp[m] = {"estimate": round(est, 1), "measured": meas, "diff_pct": round((meas / est - 1) * 100, 1),
                      "measured_scaled": round(scaled, 1), "diff_pct_scaled": round((scaled / est - 1) * 100, 1)}
        out["comparisons"].append(cmp)
    # Winner check, one tool at a time: tools are never mixed in one ranking.
    out["n_front_designs"] = len(front)
    checks = []
    for tool in sorted({p.tool for p in idx[key]}, key=lambda t: (t != "vivado", t)):
        measured_front = [_measured_record(p, spec, factors) for r in front for p in idx.get(r["key"], []) if p.tool == tool]
        sel = next(m for m in measured_front if m["key"] == key) if any(m["key"] == key for m in measured_front) else None
        best = select_design(measured_front, spec)
        chk: dict[str, Any] = {"tool": tool, "n_front_designs_measured": len({m["key"] for m in measured_front}),
                               "winner_changed": False}
        if sel is None:
            chk["why"] = "the selected design is not on the front set measured by this tool"
        elif not sel["feasible"]:
            chk["winner_changed"] = True
            chk["why"] = "the selected design violates the spec with measured numbers: " + "; ".join(
                f"{k} by {v * 100:.1f}%" for k, v in sel["violations"].items() if v > 0)
        elif best is not None and best["key"] != key:
            chk["winner_changed"] = True
            chk["why"] = (f"with measured numbers the spec's rule prefers {best['key']} "
                          f"({spec.select_by} {best[spec.select_by]:.4g} vs {sel[spec.select_by]:.4g})")
        else:
            chk["why"] = "the selected design is still the best measured front design" + (
                "" if chk["n_front_designs_measured"] > 1 else " (it is the only front design with measurements)")
        checks.append(chk)
    out["winner_checks"] = checks
    # The headline verdict comes from the reference tool (Vivado) when it has
    # measured the design, otherwise from the first tool that has.
    head = checks[0]
    out["winner_changed"], out["why"] = head["winner_changed"], f"{head['tool']}: {head['why']}"
    out["n_front_designs_measured"] = head["n_front_designs_measured"]
    others = [c for c in checks[1:] if c["winner_changed"] != head["winner_changed"]]
    if others:
        out["notes"].append("tools disagree: " + "; ".join(f"{c['tool']}: {c['why']}" for c in others))
    if not factors:
        out["notes"].append("no tool factors: measured numbers compared as-is (they come from a different tool "
                            "than the Vivado-calibrated estimate)")
    return out


# ---------------------------------------------------------------------------
# Closing the loop (milestone 3): re-explore when the winner changes
# ---------------------------------------------------------------------------

DEFAULT_REEXPLORE_CALIBRATION = REPO_ROOT / "src" / "hw_dse" / "models" / "calibration_artix7_refit_vivado-2025.2.yaml"
DEFAULT_REEXPLORE_EVALS = 60


def reexplore_boxes(rows: list[dict[str, Any]], slack: int = 2) -> dict[str, dict[str, Any]]:
    """Per family, a box around the given designs: every integer parameter
    from (min - slack) to (max + slack), clamped to the registry; categorical
    parameters keep their full choices."""
    out: dict[str, dict[str, Any]] = {}
    for fam in dict.fromkeys(r["family"] for r in rows):
        mine = [r for r in rows if r["family"] == fam]
        box: dict[str, Any] = {}
        for p in REGISTRY[fam].params:
            if p.kind == "int":
                vals = [int(r[p.name]) for r in mine]
                box[p.name] = (max(p.low, min(vals) - slack), min(p.high, max(vals) + slack))
            else:
                box[p.name] = p.choices
        out[fam] = box
    return out


def reexplore(spec: Spec, front: list[dict[str, Any]], selected: dict[str, Any] | None, ba: dict[str, Any],
              options: dict[str, Any] | None = None, seed: int = 0) -> dict[str, Any]:
    """The ``l5_reexplore`` node's logic: search again where the measurements are.

    Runs after ``back_annotate`` has flagged a winner change. The measured
    numbers say the estimate was wrong near the selected design, so:

    1. **Where:** the front designs that have measurements (and the selected
       design), each family boxed by :func:`reexplore_boxes`.
    2. **With what model:** the refitted calibration
       (``calibration_artix7_refit_vivado-2025.2.yaml`` by default): the
       cost model the measurements produced, on the Vivado scale.
    3. **How much:** ``reexplore_evals`` (default 60) NSGA-II evaluations,
       split over the families. This is a separate L5 budget: these
       evaluations are kept apart from the run's L1 evaluations
       (``l5_evaluations``) so the L1 budget comparison with the baselines is
       untouched.
    4. **Re-select:** the spec's rule over the new evaluations plus the old
       front re-scored under the refit (a deterministic recomputation, not new
       evaluations); for a spec with a system scenario the result goes through
       the L2 shortlist again.

    Every number in the result is an ``estimate`` naming the refit
    calibration; nothing here is presented as measured.
    """
    from hw_dse.explore import run_family_study
    from hw_dse.models.cost_fpga import FpgaCostModel

    opts = options or {}
    calib = Path(opts.get("reexplore_calibration") or DEFAULT_REEXPLORE_CALIBRATION)
    cm = FpgaCostModel(str(calib))
    budget = int(opts.get("reexplore_evals", DEFAULT_REEXPLORE_EVALS))
    idx = load_index([Path(c) for c in (opts.get("measured_csvs") or DEFAULT_MEASURED)])
    anchors = [r for r in front if r["key"] in idx]
    if selected is not None and selected["key"] not in {r["key"] for r in anchors}:
        anchors.append(selected)
    boxes = reexplore_boxes(anchors)
    fams = list(boxes)
    per = [budget // len(fams)] * len(fams)
    for i in range(budget - sum(per)):
        per[i % len(fams)] += 1
    recs: list[dict[str, Any]] = []
    for i, (fam, n) in enumerate(zip(fams, per)):
        if n <= 0:
            continue
        recs += run_family_study(fam, boxes[fam], spec, n, seed * 7919 + 4243 + i, tag={"round": "L5"}, cost_model=cm)
    rescored = [evaluate(_arch_of(r), spec, cm) for r in front]
    pool = recs + rescored
    from hw_dse.agent.summary import merged_front

    new_front = merged_front(pool, spec)
    sel = select_design(new_front, spec)
    l2_note = None
    if spec.system is not None and sel is not None:
        from hw_dse.l2.node import l2_select

        l2 = l2_select(pool, sel, spec)
        sel, l2_note = l2["selected"], l2.get("why")
    before = selected["key"] if selected else None
    return {
        "status": "reexplored",
        "trigger": ba.get("why"),
        "calibration": cm.calibration_id,
        "calibration_path": str(calib),
        "anchors": [r["key"] for r in anchors],
        "boxes": {f: {k: list(v) for k, v in b.items()} for f, b in boxes.items()},
        "n_evals": len(recs),
        "selected_before": before,
        "selected": sel,
        "selected_key": sel["key"] if sel else None,
        "changed": bool(sel and sel["key"] != before),
        "l2": l2_note,
        "evaluations": recs,
    }
