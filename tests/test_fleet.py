"""Milestone 4: the code-orchestrated fleet (no LLM output needed).

Scripted architects drive every member. Checked: the total budget is never
exceeded and is split as documented; members are held to their families
(a plan naming other families is cut by code, with a note); every evaluation
reaches the shared Store; the lessons are code-written facts with no free
text; the merged selection is the spec's rule over the union; a system spec
goes through L2 once, on the merged set; parallel and sequential execution
give identical results.
"""

from __future__ import annotations

from pathlib import Path

from hw_dse.agent.llm import HeuristicArchitect, ScriptedLLM
from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange
from hw_dse.agent.summary import merged_front
from hw_dse.benchmark import select_design
from hw_dse.fleet import coordinator as fc
from hw_dse.fleet import store as fstore
from hw_dse.spec import load_spec


def _plan(*fams: str) -> ExplorationPlan:
    return ExplorationPlan(families=[FamilyPlan(family=f, why="t", ranges=[ParamRange(param="data_width", low=12, high=18)])
                                     for f in fams], rationale="t")  # type: ignore[arg-type]


def scripted(member: str, phase: int) -> ScriptedLLM:
    # Each member asks for *every* family; code must cut the plan to its own.
    return ScriptedLLM([_plan("iterative", "pipelined", "pipelined_m", "unrolled_k"),
                        AnalysisDecision(decision="stop", rationale="t"), AnalysisDecision(decision="stop", rationale="t")])


def test_split_is_exact_and_drops_tiny_shares() -> None:
    assert fc.split(200, [1, 1]) == [100, 100]
    assert sum(fc.split(201, [3, 1, 1])) == 201
    assert fc.split(200, [0, 5]) == [0, 200]
    assert fc.split(100, [97, 3]) == [100, 0]  # 3 evaluations is below a member's minimum budget
    assert fc.split(50, [0, 0]) == [0, 0]
    # Review S4: no budget is lost when every positive share is below the minimum
    assert fc.split(30, [1, 1, 1]) == [30, 0, 0]
    assert fc.split(45, [1, 1, 1]) == [23, 22, 0]
    for total in range(fc.MIN_MEMBER_BUDGET, 120):
        for w in ([1, 1], [5, 1], [1, 1, 1, 1], [7, 0, 2]):
            out = fc.split(total, [float(x) for x in w])
            assert sum(out) == total and all(n == 0 or n >= fc.MIN_MEMBER_BUDGET for n in out), (total, w, out)
    assert fc.split(fc.MIN_MEMBER_BUDGET - 1, [1, 1]) == [0, 0]  # nobody could spend it


def test_the_minimum_member_budget_is_spent_in_full(tmp_path: Path) -> None:
    """Review S4: a budget of 10 left 4 evaluations below the 5-trial minimum."""
    from hw_dse.agent.runner import run_agent

    spec = load_spec("specs/low_area_control.yaml")
    for budget in range(fc.MIN_MEMBER_BUDGET, fc.MIN_MEMBER_BUDGET + 6):
        res = run_agent(fc.member_spec(spec, budget), llm=HeuristicArchitect(), seed=budget, run_root=tmp_path / str(budget),
                        options={**fc.MEMBER_OPTIONS, "fleet": {"member": "fsm", "families": ["iterative", "unrolled_k"]}})
        assert len(res["evaluations_ordered"]) == budget, budget


def test_phase2_studies_are_warm_started_from_the_store(tmp_path: Path, monkeypatch) -> None:
    """Review S3: the Store is read back, not only written."""
    import hw_dse.agent.graph as g

    seen: list[tuple[str, int]] = []
    real = g.run_family_study

    def spy(family, box, spec, n, seed, tag=None, seed_designs=None):  # type: ignore[no-untyped-def]
        seen.append((family, len(seed_designs or [])))
        return real(family, box, spec, n, seed, tag=tag, seed_designs=seed_designs)

    monkeypatch.setattr(g, "run_family_study", spy)
    spec = load_spec("specs/low_area_control.yaml")
    res = fc.run_fleet(spec, scripted, seed=1, run_root=tmp_path)
    p1_calls = sum(m["rounds"] for m in res["members"] if m["phase"] == 1)
    assert res["warm_start"] and len(seen) > p1_calls
    assert any(n > 0 for _, n in seen[-4:])  # phase-2 studies got seeds from the Store
    store = fstore.new_store()
    from hw_dse.explore import run_family_study
    from hw_dse.families import full_box

    recs = run_family_study("iterative", full_box("iterative"), spec, 30, 0)
    fstore.put_evaluations(store, spec.name, "fsm", recs)
    seeds = fstore.front_designs(store, spec, "iterative")
    assert 0 < len(seeds) <= fstore.WARM_START_MAX
    assert fstore.front_designs(store, spec, "pipelined") == []
    cold = fc.run_fleet(spec, scripted, seed=1, run_root=tmp_path / "cold", warm_start=False)
    assert not cold["warm_start"]


def test_fleet_budget_families_store_and_selection(tmp_path: Path) -> None:
    spec = load_spec("specs/low_area_control.yaml")
    res = fc.run_fleet(spec, scripted, seed=1, run_root=tmp_path)
    recs = res["evaluations_ordered"]
    assert len(recs) == spec.budget.total_evals == sum(m["n_evals"] for m in res["members"])
    p1 = [m for m in res["members"] if m["phase"] == 1]
    assert [m["budget"] for m in p1] == [100, 100]
    assert sum(m["budget"] for m in res["members"] if m["phase"] == 2) == 200
    owner = {f: m for m, fams in fc.SPLIT_BY_CLASS for f in fams}
    for m in res["members"]:
        mine = [r for r in recs if owner[r["family"]] == m["member"]]
        assert mine, m
    # every member's report shows code cutting the plan to its families
    reports = [Path(m["run_dir"]) / "report.md" for m in res["members"]]
    assert all("fleet member: dropped families outside its assignment" in p.read_text() for p in reports)
    assert res["store_evaluations_by_member"] == {m: sum(owner[r["family"]] == m for r in recs) for m in ("fsm", "pipelined")}
    assert res["selected"] == select_design(merged_front(recs, spec), spec)
    assert res["selected"]["family"] == "iterative"  # this spec's winner family on the FPGA


def test_lessons_are_code_facts_without_free_text() -> None:
    spec = load_spec("specs/low_area_control.yaml")
    store = fstore.new_store()
    les = fc.compute_lessons([], spec, fc.SPLIT_BY_CLASS)
    assert les == {}
    from hw_dse.explore import run_family_study
    from hw_dse.families import full_box

    recs = run_family_study("iterative", full_box("iterative"), spec, 20, 0)
    les = fc.compute_lessons(recs, spec, fc.SPLIT_BY_CLASS)
    fstore.put_lessons(store, spec.name, les)
    got = fstore.lessons(store, spec.name)
    allowed = {"member", "evaluations", "feasible", "best_luts_plus_ffs", "on_merged_front", "merged_front_size",
               "provenance"}
    for fam, v in got.items():
        assert set(v) == allowed and v["provenance"].startswith("code:")
        assert all(isinstance(v[k], (int, float, type(None))) for k in allowed - {"member", "provenance"})
    assert "iterative (member fsm): 20 evaluations" in fc.lessons_text(got, spec)


def test_system_spec_fleet_runs_l2_once_on_the_merged_set(tmp_path: Path) -> None:
    spec = load_spec("specs/asic/asic_multiaxis_control.yaml")
    res = fc.run_fleet(spec, lambda m, p: HeuristicArchitect(), seed=0, run_root=tmp_path)
    assert res["l2"]["status"] == "simulated"
    assert res["l2"]["n_l1_feasible"] == len({r["key"] for r in res["evaluations_ordered"] if r["feasible"]})
    sel = res["selected"]
    assert sel["feasible"] and sel["l2_fidelity"] == "L2 simulated" and sel["sys_p99_batch_us"] <= 0.5
    assert "area_um2" in sel  # the ASIC target's cost model throughout
    assert all(m["status"] != "l2_no_feasible" for m in res["members"])  # members do not run L2 themselves


def test_parallel_and_sequential_fleets_are_identical(tmp_path: Path) -> None:
    spec = load_spec("specs/asic/asic_power_50msps.yaml")
    a = fc.run_fleet(spec, lambda m, p: HeuristicArchitect(), seed=2, run_root=tmp_path / "a", parallel=True)
    b = fc.run_fleet(spec, lambda m, p: HeuristicArchitect(), seed=2, run_root=tmp_path / "b", parallel=False)
    assert [r["key"] for r in a["evaluations_ordered"]] == [r["key"] for r in b["evaluations_ordered"]]
    assert a["selected"]["key"] == b["selected"]["key"]


def test_infeasible_spec_keeps_the_whole_budget_searching(tmp_path: Path) -> None:
    spec = load_spec("specs/infeasible_dds_400msps.yaml")
    res = fc.run_fleet(spec, lambda m, p: HeuristicArchitect(), seed=0, run_root=tmp_path)
    assert res["status"] == "infeasible" and res["selected"] is None and res["llm_declared_infeasible"]
    assert res["phase2_budgets"] == {"fsm": 100, "pipelined": 100}  # nothing feasible: equal shares


def test_store_reads_are_safe_while_another_member_writes() -> None:
    """Phase-2 warm starts read the Store while the other member's thread writes to it
    (a 'dictionary changed size during iteration' race before reads took the lock)."""
    import sys
    import threading

    spec = load_spec("specs/low_area_control.yaml")
    store = fstore.new_store()
    from hw_dse.explore import run_family_study
    from hw_dse.families import full_box

    recs = run_family_study("iterative", full_box("iterative"), spec, 20, 0)
    errors: list[BaseException] = []
    done = threading.Event()
    n_writes = 3000

    def writer() -> None:
        try:
            for i in range(n_writes):
                fstore.put_evaluations(store, spec.name, "pipelined", [{**recs[i % len(recs)], "key": f"k{i}"}])
        except BaseException as exc:  # noqa: BLE001
            errors.append(exc)
        finally:
            done.set()

    def reader() -> None:
        try:
            while not done.is_set():
                fstore.evaluation_counts(store, spec.name)
        except BaseException as exc:  # noqa: BLE001
            errors.append(exc)

    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)  # switch threads as often as possible
    try:
        threads = [threading.Thread(target=writer), threading.Thread(target=reader)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    finally:
        sys.setswitchinterval(old)
    assert not errors, errors
    assert fstore.evaluation_counts(store, spec.name) == {"pipelined": n_writes}
    assert fstore.front_designs(store, spec, "iterative")
