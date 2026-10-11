"""Milestone 4: the L2 -> L1 feedback (no LLM output needed).

The correction envelope is optimistic at every observed design; the node
fires only when L2 rejects a run's whole L1-feasible set; on the constructed
spec (``specs/m4/l2_feedback_bursty.yaml``) a scripted architect that only
explores ``pipelined_m`` triggers it, and the feedback finds a passing design
with its own budget, leaving the L1 evaluations untouched.
"""

from __future__ import annotations

import random
from pathlib import Path

from hw_dse.agent.llm import ScriptedLLM
from hw_dse.agent.runner import run_agent
from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange
from hw_dse.explore import run_family_study
from hw_dse.families import full_box
from hw_dse.l2 import feedback as fb
from hw_dse.l2.node import simulate_record
from hw_dse.spec import Budget, load_spec

SPEC = "specs/m4/l2_feedback_bursty.yaml"


def test_envelope_is_monotone_and_below_every_observation() -> None:
    rng = random.Random(1)
    pts = [(rng.uniform(0.2, 1.4), rng.uniform(1.0, 50.0)) for _ in range(60)]
    env = fb.envelope(pts, "<=")
    ks = [k for _, k in env]
    assert ks == sorted(ks)
    for rho, r in pts:
        assert fb.kappa_at(env, rho) <= r + 1e-12
    assert fb.kappa_at(env, 0.1) == 1.0  # below every observation: the analytic bound
    up = fb.envelope([(0.5, 0.9), (0.7, 0.8), (0.6, 0.95)], ">=")
    assert [k for _, k in up] == [0.95, 0.95, 0.8]
    ties = fb.envelope([(0.5, 3.0), (0.5, 2.0), (0.6, 4.0)], "<=")
    assert ties == [(0.5, 2.0), (0.6, 4.0)] and fb.kappa_at(ties, 0.5) == 2.0


def test_corrected_bound_never_exceeds_the_simulation_at_observed_designs() -> None:
    spec = load_spec(SPEC)
    recs = [r for r in run_family_study("pipelined_m", full_box("pipelined_m"), spec, 40, 3) if r["feasible"]]
    recs += [r for r in run_family_study("pipelined", full_box("pipelined"), spec, 40, 4) if r["feasible"]]
    pairs = [(r, simulate_record(r, spec)) for r in recs]
    corr = fb.corrections(pairs, spec)
    assert corr["sys_p99_latency_us"]["pipelined"]["n"] == len(pairs)  # both families are ii = 1
    for r, s in pairs:
        c = fb.corrected(r, spec, corr)
        assert r["sys_p99_latency_us"] <= c["sys_p99_latency_us"] <= s["sys_p99_latency_us"] + 1e-12
        assert c["provenance"]["sys_p99_latency_us"] == fb.CORRECTED_PROVENANCE


def test_fires_only_when_l2_rejects_everything() -> None:
    assert not fb.fires(None)
    assert not fb.fires({"status": "facts_only"})
    assert not fb.fires({"status": "simulated", "n_l1_feasible": 10, "n_simulated_feasible": 1})
    assert fb.fires({"status": "simulated", "n_l1_feasible": 10, "n_simulated_feasible": 0})


def test_graph_runs_the_feedback_and_recovers(tmp_path: Path) -> None:
    spec = load_spec(SPEC).model_copy(update={"budget": Budget(total_evals=60, evals_per_round=60, max_rounds=1,
                                                               hv_epsilon=0.0)})
    plan = ExplorationPlan(families=[FamilyPlan(family="pipelined_m", why="t", ranges=[
        ParamRange(param="data_width", low=14, high=18), ParamRange(param="n_iter", low=11, high=15)])],
        rationale="t")  # type: ignore[arg-type]
    llm = ScriptedLLM([plan, AnalysisDecision(decision="stop", rationale="done")])
    res = run_agent(spec, llm=llm, run_root=tmp_path)
    assert res["l2"]["n_l1_feasible"] > 0 and res["l2"]["n_simulated_feasible"] == 0
    out = res["l2_feedback"]
    assert out is not None and out["status"] == "recovered", out
    assert res["status"] == "l2_feedback_recovered"
    sel = res["selected"]
    assert sel["feasible"] and sel["sys_p99_latency_us"] <= 0.4 and sel["l2_fidelity"] == "L2 simulated"
    assert len(res["evaluations_ordered"]) == 60  # L1 untouched; the feedback's are kept apart
    assert 0 < len(res["l2_feedback_evaluations"]) <= fb.DEFAULT_ROUNDS * fb.DEFAULT_EVALS_PER_ROUND
    assert "## L2 -> L1 feedback" in (Path(res["run_dir"]) / "report.md").read_text()


def test_feedback_can_be_switched_off(tmp_path: Path) -> None:
    spec = load_spec(SPEC).model_copy(update={"budget": Budget(total_evals=60, evals_per_round=60, max_rounds=1,
                                                               hv_epsilon=0.0)})
    plan = ExplorationPlan(families=[FamilyPlan(family="pipelined_m", why="t", ranges=[
        ParamRange(param="data_width", low=14, high=18), ParamRange(param="n_iter", low=11, high=15)])],
        rationale="t")  # type: ignore[arg-type]
    res = run_agent(spec, llm=ScriptedLLM([plan, AnalysisDecision(decision="stop", rationale="done")]),
                    run_root=tmp_path, options={"l2_feedback": {"enabled": False}})
    assert res["l2_feedback"] is None and res["status"] == "l2_no_feasible"
