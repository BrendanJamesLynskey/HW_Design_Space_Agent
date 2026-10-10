"""Replay committed live runs through today's graph (comparability checks).

Milestone 3 changes the graph (an L2 node, an L5 loop, a new lever), and the
A/B in M3 reuses the milestone-2 live runs for the four M2 specs. That reuse
is only honest if today's graph, given the *same architect outputs*, makes
the same decisions and the same evaluations as the M2 graph did. This module
replays each committed M2 run:

* :class:`~hw_dse.agent.llm.ReplayArchitect` answers every ``propose`` /
  ``analyse`` call with the object the live model returned (from the
  committed ``llm_trace.jsonl`` under ``eval/data/traces/m2/``);
* the run uses the same spec, seed and levers (``LEVERS_M2``, the default for
  a spec without a system scenario);
* the result is compared with the committed summary JSON
  (``eval/data/agent_m2/``) *and* the committed ``evaluations.csv.gz``:
  decisions, status, rounds, front-mapping rounds, every evaluated design key
  in canonical order, HV fraction, selection regret and the selected design;
* and the architect's *inputs*: every system and user prompt the graph sent
  is byte-identical to the recorded one, and every recorded call was consumed.

``tests/test_m2_replay.py`` replays a sample on every run of the suite and all
60 runs when ``HW_DSE_REPLAY_FULL=1`` (CI sets it); ``eval/m3_offline.py``
records the full result in ``eval/data/m2_replay.json``.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import tempfile
from pathlib import Path
from typing import Any

from hw_dse.rtl.generator import REPO_ROOT

DATA = REPO_ROOT / "eval" / "data"


def m2_runs() -> list[dict[str, Any]]:
    """Every committed M2 eval run (not the pilot), with its trace directory."""
    out = []
    for p in sorted((DATA / "agent_m2").glob("*/*.json")):
        row = json.loads(p.read_text())
        tdir = DATA / "traces" / "m2" / Path(row["run_dir"]).relative_to("runs/eval_m2")
        out.append({**row, "_summary": str(p.relative_to(REPO_ROOT)), "_trace_dir": str(tdir)})
    return out


def recorded_keys(trace_dir: str | Path) -> list[str]:
    with gzip.open(Path(trace_dir) / "evaluations.csv.gz", "rt", newline="") as fh:
        return [r["key"] for r in csv.DictReader(io.StringIO(fh.read()))]


def replay_run(row: dict[str, Any], levers: dict[str, Any] | None = None) -> dict[str, Any]:
    """Replay one recorded run; return today's result and what was compared."""
    from hw_dse import accuracy_table
    from hw_dse.agent.graph import LEVERS_M2
    from hw_dse.agent.llm import ReplayArchitect
    from hw_dse.agent.runner import run_agent
    from hw_dse.benchmark import score_run
    from hw_dse.spec import load_spec

    accuracy_table.preload()
    spec = load_spec(REPO_ROOT / "specs" / f"{row['spec']}.yaml")
    gt = json.loads((DATA / "ground_truth.json").read_text())[spec.name]
    trace = Path(row["_trace_dir"]) / "llm_trace.jsonl"
    arch = ReplayArchitect(str(trace))
    with tempfile.TemporaryDirectory() as tmp:
        res = run_agent(spec, llm=arch, seed=int(row["seed"]), run_root=Path(tmp),
                        levers=levers if levers is not None else LEVERS_M2)
    calls = [r for r in arch.tracer.records if r.get("recorded_system") is not None]
    sc = score_run(res["evaluations_ordered"], spec, gt, declared_infeasible=res["llm_declared_infeasible"],
                   selected=res["selected"])
    keys = [r["key"] for r in res["evaluations_ordered"]]
    return {"res": res, "score": sc, "keys": keys,
            "inputs_identical": bool(calls) and all(c["system"] == c["recorded_system"] and c["user"] == c["recorded_user"]
                                                    for c in calls),
            "all_recorded_calls_consumed": arch.served == len(arch.calls)}


def compare(row: dict[str, Any], rep: dict[str, Any]) -> dict[str, Any]:
    """Field-by-field comparison of a replay with its recording."""
    res, sc = rep["res"], rep["score"]
    checks = {
        "decisions": res["decisions"] == row["decisions"],
        "status": res["status"] == row["status"],
        "rounds": res["rounds"] == row["rounds"],
        "coverage_rounds": res["coverage_rounds"] == row["coverage_rounds"],
        "n_evals": sc["n_evals"] == row["n_evals"],
        "evaluations": rep["keys"] == recorded_keys(row["_trace_dir"]),
        "hv_frac": sc["hv_frac"] == row["hv_frac"],
        "select_regret": sc["select_regret"] == row["select_regret"],
        "selected_key": sc["selected_key"] == row["selected_key"],
        "architect_inputs": rep["inputs_identical"],  # every system/user prompt byte-identical to the recording
        "all_recorded_calls_consumed": rep["all_recorded_calls_consumed"],
    }
    return {"spec": row["spec"], "seed": row["seed"], "model": row["model_requested"], "run_dir": row["run_dir"],
            "identical": all(checks.values()), "checks": checks,
            "l2_status": (res.get("l2") or {}).get("status"),
            "back_annotation_winner_changed": bool((res.get("back_annotation") or {}).get("winner_changed")),
            "l5_status": (res.get("l5") or {}).get("status")}
