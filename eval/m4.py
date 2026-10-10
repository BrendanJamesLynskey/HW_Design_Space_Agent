"""Milestone 4 eval: the ASIC target, the fleet A/B, the L2 -> L1 feedback.

Subcommands are registered into ``eval/run_eval.py`` (:func:`register`)::

    python eval/run_eval.py ground-truth-m4      # ASIC specs, exhaustive; FPGA twins; family rankings
    python eval/run_eval.py baselines-m4         # NSGA-II / random on the ASIC specs, 5 seeds
    python eval/run_eval.py models-m4            # /api/v1/models check (free) -> eval/data/models_check_m4.json
    python eval/run_eval.py key-usage-m4 --tag before_eval
    python eval/run_eval.py agent-m4 --model qwen/qwen3.8-27b --reasoning off [--pilot]
    python eval/run_eval.py fleet-m4 --model qwen/qwen3.8-27b --reasoning off [--arm fleet|single] [--pilot]

Everything is written to M4's own files and directories; M1-M3 data is never
rewritten. ``report_m4`` appends the M4 section to ``results.md``.
"""

from __future__ import annotations

import argparse
import json
import pickle
import statistics
import time
from pathlib import Path
from typing import Any

from run_eval import (  # type: ignore[import-not-found]  # noqa: E402 - eval/ is on sys.path
    DATA, LEDGER, ROOT, SEEDS, _ms, _slim, _slim_sys, _slug, accuracy_table, build_grid, ground_truth, ledger,
    load_spec, run_baseline, score_run,
)

from hw_dse.spec import Spec

ASIC_SPECS = ("asic_low_area", "asic_power_50msps", "asic_multiaxis_control")
GT_M4_FILE = DATA / "ground_truth_m4.json"
BASELINES_M4 = DATA / "baselines_m4.json"
M4_DIRS = {"agent": DATA / "agent_m4", "fleet_ab": DATA / "fleet_m4", "pilot": DATA / "m4_pilot"}
KEY_USAGE_M4 = DATA / "key_usage_m4.json"
MODELS_CHECK_M4 = DATA / "models_check_m4.json"
M4_CAP = 5.0
GRID_CACHE = ROOT / "build" / "grids"
# The FPGA twin of each ASIC spec (for the family-ranking comparison): the same
# constraints, objectives and selection with the ASIC area metric replaced by
# the FPGA one. The twins are scored on the FPGA ground truth (M1 cost model).
AREA_TWIN = {"area_um2": "luts_plus_ffs", "gate_eq": "luts_plus_ffs"}


def asic_spec(name: str) -> Spec:
    return load_spec(ROOT / "specs" / "asic" / f"{name}.yaml")


def fpga_twin(s: Spec) -> Spec:
    d = s.model_dump()
    d["name"] = s.name + "__fpga_twin"
    d["target"] = "fpga-artix7"
    for o in d["objectives"]:
        if o["metric"] in AREA_TWIN:
            o["metric"], o["ref"] = AREA_TWIN[o["metric"]], o["ref"] / 10.0  # (ref only matters for HV)
    for c in d["constraints"]:
        c["metric"] = AREA_TWIN.get(c["metric"], c["metric"])
    d["select_by"] = AREA_TWIN.get(d["select_by"], d["select_by"])
    return Spec.model_validate(d)


def cached_grid(cost_model: Any) -> Any:
    """``build_grid`` (6-7 minutes for 635,040 designs), cached under build/grids/ by calibration id."""
    GRID_CACHE.mkdir(parents=True, exist_ok=True)
    path = GRID_CACHE / f"{cost_model.calibration_id}.pkl"
    if path.exists():
        g = pickle.loads(path.read_bytes())
        g.cost_model = cost_model
        # The cache is keyed by calibration id; check a spread of designs anyway.
        for i in range(0, len(g), 9973):
            e = cost_model.estimate(g.arch(i))
            if abs(e.fmax_mhz - g.fmax_mhz[i]) > 1e-9 or abs(e.area["ffs"] - g.ffs[i]) > 1e-9:
                raise SystemExit(f"stale grid cache {path}: delete it and re-run")
        return g
    g = build_grid(verbose=True, cost_model=cost_model)
    cm, g.cost_model = g.cost_model, None
    path.write_bytes(pickle.dumps(g))
    g.cost_model = cm
    return g


def _slim4(rec: dict[str, Any] | None, spec: Spec) -> dict[str, Any] | None:
    out = _slim_sys(rec, spec)
    if out is not None and rec is not None:
        for k in ("area_um2", "gate_eq"):
            if k in rec:
                out[k] = rec[k]
        if spec.target_kind == "asic":
            out.pop("luts", None)
            out.pop("luts_plus_ffs", None)
    return out


def family_bests(grid: Any, spec: Spec, system: str = "simulated") -> dict[str, Any]:
    """Per family: the best feasible design by the spec's selection rule (truth view)."""
    import numpy as np

    from hw_dse.benchmark import _feasible_mask
    from hw_dse.families import REGISTRY

    m = grid.metrics(spec, system) if spec.system is not None else grid.metrics(spec)
    feas = _feasible_mask(m, spec)
    sign = 1.0 if spec.select_direction == "min" else -1.0
    out: dict[str, Any] = {}
    for i, fam in enumerate(REGISTRY):
        idx = np.flatnonzero(feas & (grid.family == i))
        if not idx.size:
            out[fam] = None
            continue
        vals = sign * m[spec.select_by][idx]
        j = int(idx[int(np.argmin(vals))])
        out[fam] = {"key": grid.arch(j).key(), spec.select_by: float(m[spec.select_by][j]),
                    "throughput_msps": float(m["throughput_msps"][j]), "n_feasible": int(idx.size)}
    return out


def ranking(bests: dict[str, Any], spec: Spec) -> list[str]:
    sign = 1.0 if spec.select_direction == "min" else -1.0
    have = [f for f, b in bests.items() if b]
    return sorted(have, key=lambda f: sign * bests[f][spec.select_by])


def cmd_ground_truth_m4(_: argparse.Namespace) -> None:
    """Exhaustive ground truth on the ASIC target (system metrics simulated for the
    system spec, with the L1-bound view alongside), each ASIC spec's per-family
    bests, and the same for its FPGA twin (M1 cost model): does the family
    ranking differ between targets?"""
    import numpy as np

    from hw_dse.benchmark import _feasible_mask, select_design
    from hw_dse.evaluate import default_asic_cost_model, default_cost_model, evaluate

    accuracy_table.preload()
    t0 = time.time()
    ga = cached_grid(default_asic_cost_model())
    gf = cached_grid(default_cost_model())
    out: dict[str, Any] = {"cost_model": ga.cost_model.provenance, "fpga_cost_model": gf.cost_model.provenance}
    for name in ASIC_SPECS:
        s = asic_spec(name)
        gt = ground_truth(ga, s)
        row: dict[str, Any] = {
            "n_designs": gt["n_designs"], "n_feasible": gt["n_feasible"], "feasible": gt["feasible"],
            "hv_true": gt.get("hv_true", 0.0), "best_throughput_msps_any": gt["best_throughput_msps_any"],
            "selected": _slim4(gt["selected"], s), "front": [_slim4(r, s) for r in gt["front"]],
            "family_bests": family_bests(ga, s),
        }
        row["family_ranking"] = ranking(row["family_bests"], s)
        if s.system is not None:
            mb = ga.metrics(s, "bound")
            fb = _feasible_mask(mb, s)
            idx = np.flatnonzero(fb)
            sel = mb[s.select_by][idx]
            ties = idx[np.flatnonzero(sel == (sel.min() if s.select_direction == "min" else sel.max()))]
            bsel = select_design([evaluate(ga.arch(int(i)), s) for i in ties], s)
            row["n_feasible_l1_bound"] = int(fb.sum())
            row["l1_bound_selected"] = _slim4(bsel, s)
            row["l2_changes_winner"] = bool(bsel and gt["selected"] and bsel["key"] != gt["selected"]["key"])
            row["family_bests_l1_bound"] = family_bests(ga, s, "bound")
        tw = fpga_twin(s)
        gtw = ground_truth(gf, tw)
        row["fpga_twin"] = {"spec": tw.model_dump(), "n_feasible": gtw["n_feasible"],
                            "selected": _slim4(gtw["selected"], tw), "family_bests": family_bests(gf, tw)}
        row["fpga_twin"]["family_ranking"] = ranking(row["fpga_twin"]["family_bests"], tw)
        row["ranking_differs"] = row["family_ranking"] != row["fpga_twin"]["family_ranking"]
        row["winner_family_differs"] = (bool(gt["selected"] and gtw["selected"])
                                        and gt["selected"]["family"] != gtw["selected"]["family"])
        out[name] = row
        print(f"{name}: {gt['n_feasible']} feasible, selected {gt['selected']['key'] if gt['selected'] else None}; "
              f"ranking ASIC {row['family_ranking']} vs FPGA twin {row['fpga_twin']['family_ranking']}", flush=True)
    GT_M4_FILE.write_text(json.dumps(out, indent=1))
    print(f"wrote {GT_M4_FILE} in {time.time() - t0:.0f}s")


def load_gt_m4() -> dict[str, Any]:
    return json.loads(GT_M4_FILE.read_text())


def score_m4(records: list[dict[str, Any]], spec: Spec, declared_infeasible: bool | None,
             selected: dict[str, Any] | None) -> dict[str, Any]:
    """score_run against the ASIC ground truth; system metrics re-scored by L2 simulation."""
    if spec.system is not None:
        from hw_dse.l2.node import simulate_record

        records = [simulate_record(r, spec) for r in records]
        selected = simulate_record(selected, spec) if selected else None
    return score_run(records, spec, load_gt_m4()[spec.name], declared_infeasible=declared_infeasible,
                     selected=selected)


def cmd_baselines_m4(_: argparse.Namespace) -> None:
    from hw_dse.agent.summary import merged_front
    from hw_dse.benchmark import select_design
    from hw_dse.l2.node import l2_select

    accuracy_table.preload()
    out: dict[str, Any] = {}
    for name in ASIC_SPECS:
        s = asic_spec(name)
        for sampler in ("nsga2", "random"):
            for seed in SEEDS["m2"]:
                recs = run_baseline(s, sampler, seed)
                sel = select_design(merged_front(recs, s), s)
                if s.system is not None:
                    sel = l2_select(recs, sel, s)["selected"]
                sc = score_m4(recs, s, None if sel else True, sel)
                out[f"{name}|{sampler}|{seed}"] = {"spec": name, "method": sampler, "seed": seed, **sc}
                print(name, sampler, seed, "HV", sc["hv_frac"], "regret", sc["select_regret"], flush=True)
    BASELINES_M4.write_text(json.dumps(out, indent=1))
    print(f"wrote {BASELINES_M4}")


# ---------------------------------------------------------------------------
# Registration into run_eval.py
# ---------------------------------------------------------------------------

def register(sub: Any) -> None:
    sub.add_parser("ground-truth-m4").set_defaults(fn=cmd_ground_truth_m4)
    sub.add_parser("baselines-m4").set_defaults(fn=cmd_baselines_m4)


def report_m4(L: list[str]) -> None:  # filled in below as the M4 data lands
    if not GT_M4_FILE.exists():
        return


__all__ = ["register", "report_m4", "ASIC_SPECS", "LEDGER", "_ms", "_slim", "_slug", "ledger", "statistics", "Path"]
