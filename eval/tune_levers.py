"""Tune the whole-curve levers offline, against real recorded LLM behaviour.

    python eval/tune_levers.py            # every variant, every recorded M1 run -> eval/data/levers_offline.json
    python eval/tune_levers.py --report   # print the table from the saved JSON

Why this works without spending a cent: every milestone-1 live run left its
complete LLM trace in ``eval/data/traces/``. :class:`ReplayArchitect` feeds
those recorded decisions back into today's graph in the same order, with the
same seeds. With the levers off (``LEVERS_M1``) the replay reproduces every
recorded M1 score exactly (checked by ``tests/test_levers.py``); switching a
lever on then shows what that deterministic code would have done *for the
decisions the evaluated LLMs actually made*. The heuristic (rule-based)
architect runs alongside as a second, simpler driver.

Each variant is scored on all 48 recorded runs (4 model configurations x 4
specs x 3 seeds) against the exhaustive ground truth: hypervolume fraction,
selection regret and evaluations used. The chosen setting becomes
``LEVERS_M2`` in ``hw_dse.agent.graph``.

Caveat, stated in the README too: a replay holds the LLM's decisions fixed.
Live, the LLM sees different summaries once a lever changes what was
explored, and may decide differently; the live pilot and the 5-seed eval
are the real test.
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

OUT = ROOT / "eval" / "data" / "levers_offline.json"
OUT2 = ROOT / "eval" / "data" / "levers_offline_round2.json"
OUT3 = ROOT / "eval" / "data" / "levers_offline_round3.json"

VARIANTS_ROUND2: dict[str, dict[str, Any]] = {
    "M1 (levers off)": {"coverage_reserve": 0.0, "coverage_box": "full", "warm_start": False, "hv_epsilon": None},
    "g-reserve 0.25, anchored": {"coverage_reserve": 0.25, "coverage_box": "front_anchored", "warm_start": False},
    "g-reserve 0.40, anchored": {"coverage_reserve": 0.40, "coverage_box": "front_anchored", "warm_start": False},
    "g-reserve 0.50, anchored": {"coverage_reserve": 0.50, "coverage_box": "front_anchored", "warm_start": False},
    "g-reserve 0.40, anchored, warm<=4": {"coverage_reserve": 0.40, "coverage_box": "front_anchored",
                                          "warm_start": True, "warm_start_max": 4},
    "g-reserve 0.50, anchored, warm<=4": {"coverage_reserve": 0.50, "coverage_box": "front_anchored",
                                          "warm_start": True, "warm_start_max": 4},
}
"""Round 2, after round 1 (VARIANTS): the reserve is gated on feasibility
("g-"), and warm starts are capped to a few front designs."""

VARIANTS_ROUND3: dict[str, dict[str, Any]] = {
    "g-reserve 0.40, anchored, slack (1,2)": {"coverage_reserve": 0.40, "coverage_box": "front_anchored",
                                              "warm_start": False, "anchor_slack": (1, 2)},
    "g-reserve 0.40, anchored, slack (2,3)": {"coverage_reserve": 0.40, "coverage_box": "front_anchored",
                                              "warm_start": False, "anchor_slack": (2, 3)},
    "g-reserve 0.40, anchored, slack (3,4)": {"coverage_reserve": 0.40, "coverage_box": "front_anchored",
                                              "warm_start": False, "anchor_slack": (3, 4)},
}
"""Round 3, after the live pilot: how far below the front the box starts.
Also re-scores slack (1,2) under the final stop rule (a final front-mapping
round whenever budget is left)."""

VARIANTS: dict[str, dict[str, Any]] = {
    "M1 (levers off)": {"coverage_reserve": 0.0, "coverage_box": "full", "warm_start": False, "hv_epsilon": None},
    "reserve 0.25, full box": {"coverage_reserve": 0.25, "coverage_box": "full", "warm_start": False},
    "reserve 0.25, full box, warm": {"coverage_reserve": 0.25, "coverage_box": "full", "warm_start": True},
    "reserve 0.25, anchored": {"coverage_reserve": 0.25, "coverage_box": "front_anchored", "warm_start": False},
    "reserve 0.25, anchored, warm": {"coverage_reserve": 0.25, "coverage_box": "front_anchored", "warm_start": True},
    "reserve 0.40, anchored, warm": {"coverage_reserve": 0.40, "coverage_box": "front_anchored", "warm_start": True},
    "reserve 0.50, anchored, warm": {"coverage_reserve": 0.50, "coverage_box": "front_anchored", "warm_start": True},
    "reserve 0.25, anchored, warm, eps 0": {"coverage_reserve": 0.25, "coverage_box": "front_anchored",
                                            "warm_start": True, "hv_epsilon": 0.0},
}


def recorded_runs() -> list[dict[str, Any]]:
    out = []
    for p in sorted((ROOT / "eval" / "data" / "agent").glob("*/*.json")):
        row = json.loads(p.read_text())
        trace = ROOT / "eval" / "data" / "traces" / Path(row["run_dir"]).relative_to("runs/eval") / "llm_trace.jsonl"
        label = row["model_requested"] + ("" if row["reasoning"] == "provider default" else f", reasoning {row['reasoning']}")
        out.append({"spec": row["spec"], "seed": row["seed"], "driver": label, "trace": str(trace),
                    "m1": {k: row[k] for k in ("hv_frac", "select_regret", "n_evals")}})
    return out


def _one(job: tuple[str, dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    from hw_dse import accuracy_table
    from hw_dse.agent.llm import HeuristicArchitect, ReplayArchitect
    from hw_dse.agent.runner import run_agent
    from hw_dse.benchmark import score_run
    from hw_dse.spec import load_spec

    accuracy_table.preload()
    name, levers, run = job
    spec = load_spec(ROOT / "specs" / f"{run['spec']}.yaml")
    gt = json.loads((ROOT / "eval" / "data" / "ground_truth.json").read_text())[spec.name]
    llm = HeuristicArchitect() if run["trace"] == "heuristic" else ReplayArchitect(run["trace"])
    with tempfile.TemporaryDirectory() as tmp:
        res = run_agent(spec, llm=llm, seed=run["seed"], run_root=Path(tmp), levers=levers)
    sc = score_run(res["evaluations_ordered"], spec, gt, declared_infeasible=res["llm_declared_infeasible"],
                   selected=res["selected"])
    return {"variant": name, "spec": run["spec"], "seed": run["seed"], "driver": run["driver"],
            "hv_frac": sc["hv_frac"], "select_regret": sc["select_regret"], "n_evals": sc["n_evals"],
            "infeasibility_correct": sc["infeasibility_correct"], "coverage_rounds": res["coverage_rounds"]}


def run_all(variants: dict[str, dict[str, Any]], workers: int = 4) -> list[dict[str, Any]]:
    runs = recorded_runs()
    specs = sorted({r["spec"] for r in runs})
    runs += [{"spec": s, "seed": seed, "driver": "heuristic architect (fake)", "trace": "heuristic", "m1": {}}
             for s in specs for seed in (0, 1, 2)]
    jobs = [(n, lv, r) for n, lv in variants.items() for r in runs]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(_one, jobs, chunksize=4))


def table(rows: list[dict[str, Any]]) -> str:
    def m(xs: list[float | None]) -> str:
        v = [x for x in xs if x is not None]
        return f"{statistics.mean(v):.3f}" if v else "n/a"

    specs = ["dds_250msps", "low_area_control", "high_precision"]
    L = ["| variant | driver | " + " | ".join(f"{s} HV / regret / evals" for s in specs) + " | infeasible spec correct |",
         "|---|---|" + "---|" * len(specs) + "---|"]
    variants = list(dict.fromkeys(r["variant"] for r in rows))
    for drv_group in ("LLM replays", "heuristic architect (fake)"):
        for v in variants:
            sel = [r for r in rows if r["variant"] == v and ((r["driver"] == drv_group) if drv_group.startswith("heur")
                                                             else not r["driver"].startswith("heur"))]
            cells = []
            for s in specs:
                rs = [r for r in sel if r["spec"] == s]
                reg = [r["select_regret"] for r in rs]
                cells.append(f"{m([r['hv_frac'] for r in rs])} / "
                             f"{(statistics.mean([x for x in reg if x is not None]) * 100) if any(x is not None for x in reg) else float('nan'):+.1f}% / "
                             f"{statistics.mean(r['n_evals'] for r in rs):.0f}")
            inf = [r for r in sel if r["spec"] == "infeasible_dds_400msps"]
            L.append(f"| {v} | {drv_group} | " + " | ".join(cells) + f" | {sum(r['infeasibility_correct'] for r in inf)}/{len(inf)} |")
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--round", type=int, choices=(1, 2, 3), default=3)
    args = ap.parse_args()
    variants, out = {1: (VARIANTS, OUT), 2: (VARIANTS_ROUND2, OUT2), 3: (VARIANTS_ROUND3, OUT3)}[args.round]
    if not args.report:
        rows = run_all(variants, args.workers)
        out.write_text(json.dumps({"variants": variants, "rows": rows}, indent=1))
        print(f"wrote {out}")
    rows = json.loads(out.read_text())["rows"]
    print(table(rows))


if __name__ == "__main__":
    main()
