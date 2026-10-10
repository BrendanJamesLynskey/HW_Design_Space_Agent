"""Milestone-3 graph behaviour with scripted architects (no LLM output needed):
the L2 node in a run, the L5 re-exploration loop, the map_front fix lever."""

from __future__ import annotations

from pathlib import Path

from hw_dse.agent.graph import LEVERS_M2, LEVERS_M3, coverage_plan, default_levers
from hw_dse.agent.llm import HeuristicArchitect, ScriptedLLM
from hw_dse.agent.runner import run_agent
from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange
from hw_dse.evaluate import evaluate
from hw_dse.explore import run_family_study
from hw_dse.families import ArchConfig, full_box
from hw_dse.spec import Budget, load_spec


def _small(path: str, total: int, per_round: int, rounds: int = 3):
    s = load_spec(path)
    return s.model_copy(update={"budget": Budget(total_evals=total, evals_per_round=per_round, max_rounds=rounds, hv_epsilon=0.0)})


def _plan(fam: str, **r: tuple[int, int]) -> ExplorationPlan:
    return ExplorationPlan(families=[FamilyPlan(family=fam, why="t", ranges=[ParamRange(param=k, low=v[0], high=v[1])
                                                                            for k, v in r.items()])], rationale="t")  # type: ignore[arg-type]


def test_default_levers_by_spec() -> None:
    assert default_levers(load_spec("specs/dds_250msps.yaml")) == LEVERS_M2
    assert default_levers(load_spec("specs/system/bursty_offload.yaml")) == LEVERS_M3


def test_system_spec_run_goes_through_l2_and_reports_it(tmp_path: Path) -> None:
    spec = _small("specs/system/multiaxis_control.yaml", 120, 60)
    llm = ScriptedLLM([_plan("pipelined_m", data_width=(16, 18), n_iter=(13, 15), m=(4, 6)),
                       AnalysisDecision(decision="stop", rationale="done")])
    res = run_agent(spec, llm=llm, run_root=tmp_path)
    l2 = res["l2"]
    assert l2["status"] == "simulated" and l2["shortlist"]
    sel = res["selected"]
    assert sel is not None and sel["feasible"] and sel["provenance"]["sys_p99_batch_us"].startswith("simulated")
    assert sel["sys_p99_batch_us"] <= 0.44
    if l2["winner_changed"]:
        assert res["selected_l1"]["key"] != sel["key"]
    report = (Path(res["run_dir"]) / "report.md").read_text()
    assert "## L2: cycle-level contract and system simulation" in report and "bound → simulated" in report


def test_heuristic_architect_on_both_eval_system_specs(tmp_path: Path) -> None:
    for p in ("specs/system/bursty_offload.yaml", "specs/system/multiaxis_control.yaml"):
        res = run_agent(_small(p, 80, 40), llm=HeuristicArchitect(), run_root=tmp_path)
        assert res["status"] in ("stopped", "converged", "l2_no_feasible", "infeasible", "no_feasible")
        assert res["l2"] is None or res["l2"]["status"] in ("simulated", "skipped")


def test_l5_loop_reexplores_with_the_refit_when_the_winner_changes(tmp_path: Path) -> None:
    """Recorded data: the dds_250msps optimum measures 4.4% short of 250 MSPS in
    nextpnr (eval/data/l4_synthesis.csv), so back_annotate flags it and the L5
    loop re-explores around it under the vivado-2025.2 refit."""
    spec = _small("specs/dds_250msps.yaml", 40, 40, rounds=1)
    llm = ScriptedLLM([_plan("pipelined", data_width=(18, 18), n_iter=(15, 15), angle_guard=(1, 1), frac_guard=(0, 0)),
                       AnalysisDecision(decision="stop", rationale="done")])
    res = run_agent(spec, llm=llm, run_root=tmp_path, levers={**LEVERS_M2, "coverage_reserve": 0.0},
                    options={"back_annotate": {"reexplore_evals": 30}})
    assert res["back_annotation"]["winner_changed"]
    l5 = res["l5"]
    assert l5["status"] == "reexplored" and l5["n_evals"] == 30
    assert l5["calibration"] == "artix7-xc7a35t-refit-vivado-2025.2"
    assert "refit-vivado-2025.2" in (l5["selected"] or {}).get("provenance", {}).get("luts", "refit-vivado-2025.2")
    assert len(res["evaluations_ordered"]) == 40  # the L1 budget is untouched
    assert "## L5 loop: re-exploration after a winner change" in (Path(res["run_dir"]) / "report.md").read_text()


def test_l5_loop_can_be_switched_off(tmp_path: Path) -> None:
    spec = _small("specs/dds_250msps.yaml", 40, 40, rounds=1)
    llm = ScriptedLLM([_plan("pipelined", data_width=(18, 18), n_iter=(15, 15), angle_guard=(1, 1), frac_guard=(0, 0)),
                       AnalysisDecision(decision="stop", rationale="done")])
    res = run_agent(spec, llm=llm, run_root=tmp_path, levers={**LEVERS_M2, "coverage_reserve": 0.0},
                    options={"back_annotate": {"reexplore": False}})
    assert res["back_annotation"]["winner_changed"] and res["l5"] is None


def test_map_front_fix_maps_a_family_whose_box_missed_the_accuracy_target() -> None:
    """The M2 blind spot: pipelined_m searched at W=20-24 never reaches 2^-20,
    the front is pipelined only. With the M3 lever the mapping round gives
    pipelined_m a full-box share; with the M2 levers it does not."""
    spec = load_spec("specs/high_precision.yaml")
    recs = run_family_study("pipelined", {**full_box("pipelined"), "data_width": (24, 28), "n_iter": (20, 26)}, spec, 30, 0)
    recs += run_family_study("pipelined_m", {**full_box("pipelined_m"), "data_width": (20, 24)}, spec, 30, 1)
    recs += run_family_study("iterative", {**full_box("iterative"), "data_width": (24, 28)}, spec, 10, 2)
    assert not any(r["feasible"] for r in recs if r["family"] == "pipelined_m")
    m2 = coverage_plan(spec, recs, 100, LEVERS_M2)
    m3 = coverage_plan(spec, recs, 100, LEVERS_M3)
    assert [j["family"] for j in m2["jobs"]] == ["pipelined"]
    fams = {j["family"]: j for j in m3["jobs"]}
    # iterative never reached 50 MSPS (structural): not mapped. pipelined_m only missed accuracy: mapped.
    assert set(fams) == {"pipelined", "pipelined_m"}
    assert fams["pipelined_m"]["box"]["data_width"] == [8, 28] and sum(j["n_trials"] for j in m3["jobs"]) == 100
    allf = coverage_plan(spec, recs, 100, {**LEVERS_M2, "map_unfeasible_families": True})
    assert {j["family"] for j in allf["jobs"]} == {"pipelined", "pipelined_m", "iterative"}


def test_l1_records_of_system_specs_carry_bounds() -> None:
    spec = load_spec("specs/system/bursty_offload.yaml")
    rec = evaluate(ArchConfig.from_params("iterative", {"data_width": 15, "n_iter": 12, "angle_guard": 1, "rounding": "round"}), spec)
    assert rec["l2_fidelity"] == "L1 bound" and not rec["feasible"]  # 8 queued requests x 15 cycles > 0.4 us even alone
