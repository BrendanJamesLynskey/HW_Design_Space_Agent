"""The whole-curve levers, offline: replays of recorded LLM runs and scripted decisions.

No live model is called. ``ReplayArchitect`` replays the decisions a real
LLM made in a recorded milestone-1 run (``eval/data/traces``), so these
tests check what the *code* levers do with real LLM behaviour.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from hw_dse.agent.graph import LEVERS_M1, LEVERS_M2, coverage_plan
from hw_dse.agent.llm import ReplayArchitect, ScriptedLLM
from hw_dse.agent.runner import run_agent
from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange
from hw_dse.benchmark import score_run
from hw_dse.explore import run_family_study
from hw_dse.families import full_box
from hw_dse.spec import Budget, load_spec

ROOT = Path(__file__).resolve().parents[1]
GT = json.loads((ROOT / "eval/data/ground_truth.json").read_text())


def _recorded(model_dir: str, spec: str, seed: int) -> tuple[dict, Path]:
    row = json.loads((ROOT / "eval/data/agent" / model_dir / f"{spec}_seed{seed}.json").read_text())
    trace = ROOT / "eval/data/traces" / Path(row["run_dir"]).relative_to("runs/eval") / "llm_trace.jsonl"
    return row, trace


def _replay(model_dir: str, spec_name: str, seed: int, levers: dict, tmp: Path) -> tuple[dict, dict]:
    row, trace = _recorded(model_dir, spec_name, seed)
    spec = load_spec(ROOT / "specs" / f"{spec_name}.yaml")
    res = run_agent(spec, llm=ReplayArchitect(str(trace)), seed=seed, run_root=tmp, levers=levers)
    sc = score_run(res["evaluations_ordered"], spec, GT[spec_name], declared_infeasible=res["llm_declared_infeasible"],
                   selected=res["selected"])
    return row, {**res, **sc}


def test_replay_with_levers_off_reproduces_the_recorded_m1_run(tmp_path: Path) -> None:
    row, res = _replay("anthropic__claude-sonnet-5.5", "dds_250msps", 0, LEVERS_M1, tmp_path)
    assert res["decisions"] == row["decisions"]
    assert res["n_evals"] == row["n_evals"]
    assert res["hv_frac"] == pytest.approx(row["hv_frac"], rel=1e-12)
    assert res["select_regret"] == pytest.approx(row["select_regret"], rel=1e-12)


def test_m2_levers_map_the_front_for_the_same_llm_decisions(tmp_path: Path) -> None:
    """Same recorded Sonnet decisions; the code's front-mapping round closes the HV gap."""
    row, res = _replay("anthropic__claude-sonnet-5.5", "dds_250msps", 0, LEVERS_M2, tmp_path)
    assert res["coverage_rounds"] == 1 and res["n_evals"] == 400
    assert row["hv_frac"] < 0.25 and res["hv_frac"] > 0.8  # NSGA-II baseline: 0.80
    assert res["select_regret"] <= row["select_regret"] + 1e-12  # selection not hurt
    assert any("front-mapping round" in o for o in res["overrides"])


def test_infeasible_spec_keeps_the_whole_budget_for_the_llm(tmp_path: Path) -> None:
    row, res = _replay("anthropic__claude-sonnet-5.5", "infeasible_dds_400msps", 0, LEVERS_M2, tmp_path)
    assert res["status"] == "infeasible" and res["coverage_rounds"] == 0
    assert res["n_evals"] == row["n_evals"]


def _small(name: str, total: int, per_round: int, rounds: int = 4):
    s = load_spec(ROOT / "specs" / f"{name}.yaml")
    return s.model_copy(update={"budget": Budget(total_evals=total, evals_per_round=per_round, max_rounds=rounds,
                                                 hv_epsilon=0.01)})


def _plan(fam: str, **r: tuple[int, int]) -> ExplorationPlan:
    return ExplorationPlan(families=[FamilyPlan(family=fam, why="t", ranges=[ParamRange(param=k, low=v[0], high=v[1])
                                                                            for k, v in r.items()])], rationale="t")  # type: ignore[arg-type]


def test_llm_map_front_decision_runs_a_coverage_round(tmp_path: Path) -> None:
    spec = _small("low_area_control", 100, 40)
    llm = ScriptedLLM([_plan("iterative", data_width=(14, 16), n_iter=(11, 13)),
                       AnalysisDecision(decision="map_front", rationale="front is narrow"),
                       AnalysisDecision(decision="stop", rationale="done")])
    res = run_agent(spec, llm=llm, run_root=tmp_path)
    # the LLM's map_front round, then (at stop) the code's final round with the leftover budget
    assert res["decisions"] == ["map_front", "stop"] and res["coverage_rounds"] == 2
    assert len(res["evaluations_ordered"]) == 100
    r2 = [r for r in res["evaluations_ordered"] if r["round"] == 2]
    assert r2 and max(r["data_width"] for r in r2) > 16  # explored beyond the LLM's narrow box
    report = (Path(res["run_dir"]) / "report.md").read_text()
    assert "front-mapping" in report


def test_reserve_caps_the_llm_rounds_then_maps(tmp_path: Path) -> None:
    spec = _small("low_area_control", 100, 50, rounds=4)
    llm = ScriptedLLM([_plan("iterative", data_width=(14, 16)),
                       AnalysisDecision(decision="refine", rationale="r", next_plan=_plan("iterative", data_width=(14, 15))),
                       AnalysisDecision(decision="refine", rationale="r", next_plan=_plan("iterative", data_width=(14, 15)))])
    res = run_agent(spec, llm=llm, run_root=tmp_path, levers={**LEVERS_M2, "coverage_reserve": 0.4})
    by_round = {}
    for r in res["evaluations_ordered"]:
        by_round[r["round"]] = by_round.get(r["round"], 0) + 1
    # LLM rounds share 60 evaluations (50 + 10); then the LLM's next 'refine' hits its budget
    # and code spends the 40 reserved evaluations on mapping the front.
    assert by_round == {1: 50, 2: 10, 3: 40} and res["coverage_rounds"] == 1
    assert res["status"] == "budget"


def test_coverage_plan_box_and_seeds() -> None:
    spec = _small("low_area_control", 400, 100)
    recs = run_family_study("iterative", {**full_box("iterative"), "data_width": (15, 17), "n_iter": (12, 14)}, spec, 30, 0)
    plan = coverage_plan(spec, recs, 100, {**LEVERS_M2, "warm_start": True, "warm_start_max": 3})
    job = plan["jobs"][0]
    assert job["family"] == "iterative" and job["n_trials"] == 100
    assert job["box"]["data_width"][1] == 28 and job["box"]["data_width"][0] >= 14
    assert 1 <= len(job["seeds"]) <= 3
    # seeds warm-start NSGA-II but are not new evaluations
    out = run_family_study("iterative", {k: tuple(v) for k, v in job["box"].items()}, spec, 20, 1,
                           seed_designs=job["seeds"])
    assert len(out) == 20
