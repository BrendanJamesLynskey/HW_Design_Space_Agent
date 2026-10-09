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


def back_annotate(spec: Spec, front: list[dict[str, Any]], selected: dict[str, Any] | None,
                  options: dict[str, Any] | None = None) -> dict[str, Any]:
    """The node's logic, as a pure function of the run's front and selection."""
    opts = options or {}
    if opts.get("enabled") is False or selected is None:
        return {"status": "skipped", "reason": "disabled" if selected else "no design selected"}
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
        cmp = {"tool": p.tool, "tool_version": p.tool_version, "provenance": p.provenance}
        for m, meas in (("luts", p.luts), ("ffs", p.ffs), ("fmax_mhz", p.fmax_mhz)):
            est = float(selected[m])
            cmp[m] = {"estimate": round(est, 1), "measured": meas, "diff_pct": round((meas / est - 1) * 100, 1)}
        out["comparisons"].append(cmp)
    # Winner check over the front designs that have measurements.
    measured_front = []
    for r in front:
        for p in idx.get(r["key"], []):
            measured_front.append(_measured_record(p, spec, factors))
    sel_meas = [m for m in measured_front if m["key"] == key]
    best = select_design(measured_front, spec)
    out["n_front_designs_measured"] = len({m["key"] for m in measured_front})
    out["n_front_designs"] = len(front)
    if sel_meas and not all(m["feasible"] for m in sel_meas):
        out["winner_changed"] = True
        out["why"] = "the selected design violates the spec with measured numbers: " + "; ".join(
            f"{k} by {v * 100:.1f}%" for m in sel_meas for k, v in m["violations"].items() if v > 0)
    elif best is not None and best["key"] != key:
        out["winner_changed"] = True
        out["why"] = (f"with measured numbers the spec's rule prefers {best['key']} "
                      f"({spec.select_by} {best[spec.select_by]:.4g} vs {sel_meas[0][spec.select_by]:.4g})")
    else:
        out["why"] = "the selected design is still the best measured front design" + (
            "" if out["n_front_designs_measured"] > 1 else " (it is the only front design with measurements)")
    if not factors:
        out["notes"].append("no tool factors: measured numbers compared as-is (they come from a different tool "
                            "than the Vivado-calibrated estimate)")
    return out
