"""Milestone 3 offline checks: no LLM, no spend.

    python eval/m3_offline.py replay     # all 60 M2 runs through today's graph -> eval/data/m2_replay.json
    python eval/m3_offline.py mapfront   # the map_front fix on the M2 specs     -> eval/data/m3_mapfront_fix.json
    python eval/m3_offline.py report     # print both tables

``replay`` is the comparability proof behind reusing the M2 live runs in the
M3 A/B (see :mod:`hw_dse.agent.replay`).

``mapfront`` answers "does the M3 fix (map families that were explored but
found nothing feasible) change anything on the existing specs?" with two
scripted architects, levers ``LEVERS_M2`` vs ``LEVERS_M2 + fix``:

* the 60 recorded M2 runs replayed (``ReplayArchitect``: the decisions the
  live models actually made, held fixed);
* the rule-based ``HeuristicArchitect`` on the four M2 specs, seeds 0-4.

A replay holds the LLM's decisions fixed; a live model might react to the
different summaries. The live M3 runs on the new specs use the fix.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

OUT_REPLAY = ROOT / "eval" / "data" / "m2_replay.json"
OUT_FIX = ROOT / "eval" / "data" / "m3_mapfront_fix.json"
M2_SPECS = ("dds_250msps", "low_area_control", "high_precision", "infeasible_dds_400msps")


def _replay(row: dict[str, Any]) -> dict[str, Any]:
    from hw_dse.agent.replay import compare, replay_run

    return compare(row, replay_run(row))


def _fix_job(job: tuple[str, str, dict[str, Any]]) -> dict[str, Any]:
    from hw_dse import accuracy_table
    from hw_dse.agent.graph import LEVERS_M2, LEVERS_M3
    from hw_dse.agent.llm import HeuristicArchitect
    from hw_dse.agent.replay import replay_run
    from hw_dse.agent.runner import run_agent
    from hw_dse.benchmark import score_run
    from hw_dse.spec import load_spec

    accuracy_table.preload()
    variant, driver, row = job
    levers = {"m2": LEVERS_M2, "fix": LEVERS_M3, "fix-all": {**LEVERS_M2, "map_unfeasible_families": True}}[variant]
    if driver == "replay":
        rep = replay_run(row, levers)
        res, sc = rep["res"], rep["score"]
    else:
        spec = load_spec(ROOT / "specs" / f"{row['spec']}.yaml")
        gt = json.loads((ROOT / "eval" / "data" / "ground_truth.json").read_text())[spec.name]
        with tempfile.TemporaryDirectory() as tmp:
            res = run_agent(spec, llm=HeuristicArchitect(), seed=row["seed"], run_root=Path(tmp), levers=levers)
        sc = score_run(res["evaluations_ordered"], spec, gt, declared_infeasible=res["llm_declared_infeasible"],
                       selected=res["selected"])
    return {"variant": variant, "driver": driver if driver != "replay" else row["model_requested"], "spec": row["spec"],
            "seed": row["seed"], "hv_frac": sc["hv_frac"], "select_regret": sc["select_regret"], "n_evals": sc["n_evals"],
            "selected_key": sc["selected_key"], "infeasibility_correct": sc["infeasibility_correct"]}


def cmd_replay(args: argparse.Namespace) -> None:
    from hw_dse.agent.replay import m2_runs

    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(_replay, m2_runs()))
    OUT_REPLAY.write_text(json.dumps({"n_runs": len(rows), "n_identical": sum(r["identical"] for r in rows),
                                      "rows": rows}, indent=1))
    print(f"{sum(r['identical'] for r in rows)}/{len(rows)} identical -> {OUT_REPLAY}")


def cmd_mapfront(args: argparse.Namespace) -> None:
    from hw_dse.agent.replay import m2_runs

    variants = ("m2", "fix-all", "fix")
    jobs = [(v, "replay", r) for v in variants for r in m2_runs()]
    jobs += [(v, "heuristic architect (fake)", {"spec": s, "seed": seed}) for v in variants for s in M2_SPECS
             for seed in range(5)]
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(_fix_job, jobs, chunksize=2))
    OUT_FIX.write_text(json.dumps({"rows": rows}, indent=1))
    print(f"wrote {OUT_FIX}")
    print(table_fix(rows, "fix-all"))
    print(table_fix(rows, "fix"))


def _m(xs: list[float | None], pct: bool = False) -> str:
    v = [x for x in xs if x is not None]
    if not v:
        return "n/a"
    k = 100 if pct else 1
    return f"{statistics.mean(v) * k:+.1f}%" if pct else f"{statistics.mean(v):.3f}"


def table_fix(rows: list[dict[str, Any]], fix: str = "fix") -> str:
    """Per driver group and spec: HV / regret with the M2 levers -> with the fix, and runs that changed.
    ``fix`` = "fix" (the gated M3 default) or "fix-all" (every unfeasible family)."""
    L = [f"| driver | spec | runs | HV M2 levers → {fix} | regret M2 levers → {fix} | runs whose selection changed |",
         "|---|---|---|---|---|---|"]
    groups = [("LLM replays (3 models x 5 seeds)", lambda d: not d.startswith("heuristic")),
              ("heuristic architect (fake)", lambda d: d.startswith("heuristic"))]
    for gname, pred in groups:
        for s in M2_SPECS:
            a = sorted([r for r in rows if r["variant"] == "m2" and pred(r["driver"]) and r["spec"] == s],
                       key=lambda r: (r["driver"], r["seed"]))
            b = sorted([r for r in rows if r["variant"] == fix and pred(r["driver"]) and r["spec"] == s],
                       key=lambda r: (r["driver"], r["seed"]))
            changed = sum(x["selected_key"] != y["selected_key"] for x, y in zip(a, b))
            hv = f"{_m([r['hv_frac'] for r in a])} → {_m([r['hv_frac'] for r in b])}"
            rg = f"{_m([r['select_regret'] for r in a], True)} → {_m([r['select_regret'] for r in b], True)}"
            L.append(f"| {gname} | {s} | {len(a)} | {hv} | {rg} | {changed} |")
    return "\n".join(L)


def cmd_report(_: argparse.Namespace) -> None:
    rep = json.loads(OUT_REPLAY.read_text())
    print(f"M2 replay: {rep['n_identical']}/{rep['n_runs']} identical")
    rows = json.loads(OUT_FIX.read_text())["rows"]
    print(table_fix(rows, "fix-all"))
    print(table_fix(rows, "fix"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("replay", "mapfront", "report"))
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    {"replay": cmd_replay, "mapfront": cmd_mapfront, "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    main()
