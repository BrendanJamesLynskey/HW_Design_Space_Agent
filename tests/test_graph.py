"""Full graph runs with a scripted LLM: no real model output is ever needed.

Each test scripts the LLM's answers (plans and decisions) and checks what
the *code* does with them: fan-out, reducers, hard stopping rules,
overrides, reports, and interrupt/resume through the SQLite checkpointer.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from langgraph.types import Command

from hw_dse.agent.graph import LEVERS_M1, build_graph, validate_plan
from hw_dse.agent.llm import ScriptedLLM
from hw_dse.agent.runner import run_agent, sqlite_checkpointer
from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange, SpecDraft
from hw_dse.agent.trace import Tracer
from hw_dse.spec import Budget, load_spec


def small(spec_path: str, total: int = 60, per_round: int = 30, rounds: int = 4, eps: float = 0.0):
    s = load_spec(spec_path)
    return s.model_copy(update={"budget": Budget(total_evals=total, evals_per_round=per_round, max_rounds=rounds, hv_epsilon=eps)})


def plan(*fams: str, **ranges: tuple[int, int]) -> ExplorationPlan:
    rs = [ParamRange(param=k, low=v[0], high=v[1]) for k, v in ranges.items()]
    return ExplorationPlan(families=[FamilyPlan(family=f, ranges=rs, why="test") for f in fams], rationale="scripted")  # type: ignore[arg-type]


def decide(d: str, nxt: ExplorationPlan | None = None) -> AnalysisDecision:
    return AnalysisDecision(decision=d, rationale=f"scripted {d}", next_plan=nxt)  # type: ignore[arg-type]


def test_feasible_run_refines_then_stops(tmp_path: Path) -> None:
    spec = small("specs/dds_250msps.yaml")
    llm = ScriptedLLM([
        plan("pipelined", "pipelined_m", data_width=(16, 20), n_iter=(13, 17)),
        decide("refine", plan("pipelined", data_width=(17, 19), n_iter=(14, 16))),
        decide("stop"),
    ])
    res = run_agent(spec, llm=llm, run_root=tmp_path)
    assert res["status"] == "stopped"
    assert res["decisions"] == ["refine", "stop"]
    assert len(res["evaluations_ordered"]) == 60
    assert res["selected"] is not None and res["selected"]["feasible"]
    run = Path(res["run_dir"])
    for f in ("report.md", "pareto.png", "evaluations.csv", "llm_trace.jsonl", "checkpoints.sqlite"):
        assert (run / f).exists(), f
    trace = [json.loads(line) for line in (run / "llm_trace.jsonl").read_text().splitlines()]
    assert [t["node"] for t in trace] == ["propose", "analyse", "analyse"]
    report = (run / "report.md").read_text()
    assert "scripted refine" in report and "estimate: cost_fpga" in report and "exact: bit-accurate" in report
    # Round 2 searched only the refined box.
    r2 = [r for r in res["evaluations_ordered"] if r["round"] == 2]
    assert r2 and all(r["family"] == "pipelined" and 17 <= r["data_width"] <= 19 for r in r2)


def test_infeasible_declared(tmp_path: Path) -> None:
    spec = small("specs/infeasible_dds_400msps.yaml")
    llm = ScriptedLLM([
        plan("pipelined"),
        decide("widen", plan("pipelined", "pipelined_m", data_width=(8, 12))),
        decide("infeasible"),
    ])
    res = run_agent(spec, llm=llm, run_root=tmp_path)
    assert res["status"] == "infeasible"
    assert res["llm_declared_infeasible"] is True
    assert res["selected"] is None
    report = (Path(res["run_dir"]) / "report.md").read_text()
    assert "INFEASIBLE" in report and "best throughput seen" in report


def test_infeasible_rejected_when_feasible_designs_exist(tmp_path: Path) -> None:
    spec = small("specs/low_area_control.yaml", total=30, per_round=30)
    res = run_agent(spec, llm=ScriptedLLM([plan("iterative", data_width=(12, 16)), decide("infeasible")]), run_root=tmp_path)
    assert res["status"] == "stopped" and res["llm_declared_infeasible"] is False
    assert res["selected"] is not None


def test_round_cap_overrides_continue(tmp_path: Path) -> None:
    spec = small("specs/low_area_control.yaml", total=200, per_round=20, rounds=2)
    llm = ScriptedLLM([
        plan("iterative", data_width=(12, 16)),
        decide("refine", plan("iterative", data_width=(13, 15))),
        decide("refine", plan("iterative", data_width=(14, 15))),  # round 2 == cap
    ])
    res = run_agent(spec, llm=llm, run_root=tmp_path, levers=LEVERS_M1)
    assert res["status"] == "round_cap" and res["rounds"] == 2
    assert len(res["evaluations_ordered"]) == 40


def test_hv_epsilon_rule_and_missing_plan_fallback(tmp_path: Path) -> None:
    # Huge epsilon: any continue after round 1 is stopped by the HV rule.
    spec = small("specs/low_area_control.yaml", total=90, per_round=30, eps=10.0)
    llm = ScriptedLLM([plan("iterative", data_width=(12, 16)), decide("refine"), decide("widen")])
    res = run_agent(spec, llm=llm, run_root=tmp_path, levers=LEVERS_M1)
    assert res["status"] == "converged" and res["rounds"] == 2
    report = (Path(res["run_dir"]) / "report.md").read_text()
    assert "deterministic fallback" in report and "HV gain" in report


def test_no_feasible_without_declaration(tmp_path: Path) -> None:
    spec = small("specs/infeasible_dds_400msps.yaml", total=30, per_round=30)
    res = run_agent(spec, llm=ScriptedLLM([plan("pipelined"), decide("stop")]), run_root=tmp_path)
    assert res["status"] == "no_feasible" and not res["llm_declared_infeasible"]


def test_validate_plan_budget_split_and_clamp() -> None:
    p = ExplorationPlan(families=[
        FamilyPlan(family="pipelined", ranges=[ParamRange(param="data_width", low=4, high=40)], budget_share=3, why=""),
        FamilyPlan(family="pipelined", why="dup"),
        FamilyPlan(family="iterative", budget_share=1, why=""),
    ], rationale="")
    vp = validate_plan(p, 40)
    assert [j["n_trials"] for j in vp["jobs"]] == [30, 10]
    assert vp["jobs"][0]["box"]["data_width"] == [8, 28]
    assert any("duplicate" in n for n in vp["notes"]) and any("clamped" in n for n in vp["notes"])


def test_interrupt_and_resume_through_sqlite(tmp_path: Path) -> None:
    spec = small("specs/low_area_control.yaml", total=40, per_round=20, rounds=2)
    db = tmp_path / "ck.sqlite"
    cfg = {"configurable": {"thread_id": "t1", "levers": LEVERS_M1}, "recursion_limit": 50}
    run_dir = tmp_path / "run"

    # Process 1: starts, pauses for spec confirmation.
    g1 = build_graph(ScriptedLLM([], tracer=Tracer()), sqlite_checkpointer(db))
    out = g1.invoke({"spec": spec.model_dump(), "run_dir": str(run_dir), "seed": 0}, cfg)
    assert out["__interrupt__"][0].value["type"] == "confirm_spec"
    del g1  # "crash"

    # Process 2: a fresh graph on the same database resumes the same thread.
    llm = ScriptedLLM([plan("iterative", data_width=(12, 16)), decide("refine", plan("iterative", data_width=(13, 15))), decide("stop")])
    g2 = build_graph(llm, sqlite_checkpointer(db))
    out = g2.invoke(Command(resume={"approve": True}), cfg)
    intr = out["__interrupt__"][0].value
    assert intr["type"] == "select" and len(intr["front"]) >= 1

    # Process 3: pick a design by index.
    g3 = build_graph(ScriptedLLM([]), sqlite_checkpointer(db))
    choice = len(intr["front"]) - 1
    final = g3.invoke(Command(resume={"choice": choice}), cfg)
    assert final["status"] == "stopped"
    assert final["selected"]["key"] == intr["front"][choice]["key"]
    assert final["selection_mode"] == f"human picked front index {choice}"
    assert (run_dir / "report.md").exists()


def test_rejected_spec_explores_nothing(tmp_path: Path) -> None:
    spec = small("specs/low_area_control.yaml")
    cfg = {"configurable": {"thread_id": "r"}}
    g = build_graph(ScriptedLLM([]), sqlite_checkpointer(tmp_path / "ck.sqlite"))
    g.invoke({"spec": spec.model_dump(), "run_dir": str(tmp_path / "run"), "seed": 0}, cfg)
    final = g.invoke(Command(resume={"approve": False}), cfg)
    assert final["status"] == "rejected" and not final.get("evaluations")


def test_natural_language_intake(tmp_path: Path) -> None:
    draft = SpecDraft(name="Tiny NCO", description="small nco", min_throughput_msps=5, max_abs_err=2.0**-9, minimise=["luts"])
    llm = ScriptedLLM([draft, plan("iterative", data_width=(10, 14)), decide("stop")])
    g = build_graph(llm, sqlite_checkpointer(tmp_path / "ck.sqlite"))
    cfg = {"configurable": {"thread_id": "nl", "auto_approve": True, "auto_select": True}}
    final = g.invoke({"spec_text": "I need a tiny NCO, 5 MSPS, 9 bits", "run_dir": str(tmp_path / "run"), "seed": 0}, cfg)
    assert final["intake_mode"] == "llm"
    assert final["spec"]["name"] == "tiny_nco"
    assert [o["metric"] for o in final["spec"]["objectives"]] == ["luts", "accuracy_bits"]
    assert final["status"] == "stopped"


@pytest.mark.parametrize("spec_path", ["specs/dds_250msps.yaml", "specs/infeasible_dds_400msps.yaml"])
def test_heuristic_fake_runs(tmp_path: Path, spec_path: str) -> None:
    from hw_dse.agent.llm import HeuristicArchitect

    res = run_agent(small(spec_path, total=80, per_round=40), llm=HeuristicArchitect(), run_root=tmp_path)
    assert res["status"] in ("stopped", "infeasible")


def test_int_param_with_stray_choices_uses_bounds() -> None:
    # A live model once sent choices=['trunc','round'] on angle_guard along
    # with its bounds; the bounds must win for integer parameters.
    p = ExplorationPlan(families=[FamilyPlan(family="pipelined", why="", ranges=[
        ParamRange(param="angle_guard", low=-1, high=3, choices=["trunc", "round"]),
        ParamRange(param="rounding", choices=["round"]),
    ])], rationale="")
    box = validate_plan(p, 20)["jobs"][0]["box"]
    assert box["angle_guard"] == [-1, 3] and box["rounding"] == ["round"]


def test_zero_budget_shares_and_propose_fallback(tmp_path: Path) -> None:
    p = ExplorationPlan(families=[FamilyPlan(family="pipelined", budget_share=0, why=""),
                                  FamilyPlan(family="iterative", budget_share=0, why="")], rationale="")
    assert [j["n_trials"] for j in validate_plan(p, 20)["jobs"]] == [10, 10]

    def bad(schema: type, ctx: dict) -> object:  # wrong type -> StructuredOutputError
        return decide("stop")

    spec = small("specs/low_area_control.yaml", total=40, per_round=40)
    res = run_agent(spec, llm=ScriptedLLM([bad, decide("stop")]), run_root=tmp_path)
    assert res["status"] == "stopped" and len(res["evaluations_ordered"]) == 40
    assert "deterministic fallback" in (Path(res["run_dir"]) / "report.md").read_text()
