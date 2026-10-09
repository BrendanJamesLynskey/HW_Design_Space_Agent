"""L2: cycle model, SimPy system models, L1 bounds, DDS spectrum, the L2 node.

Offline and fast. The cycle-for-cycle comparison with the generated RTL
needs Icarus and/or Verilator: it skips cleanly without them and is
required in CI (``HW_DSE_REQUIRE_RTL=1`` makes the Icarus check mandatory,
``HW_DSE_REQUIRE_SIM=1`` both simulators).
"""

from __future__ import annotations

import numpy as np
import pytest

from hw_dse.evaluate import evaluate
from hw_dse.families import ArchConfig
from hw_dse.l2.bounds import bound_metrics
from hw_dse.l2.cycle import Contract, CycleModel, accept_edges, drive_queue
from hw_dse.l2.dds import dds_spectrum, phase_codes
from hw_dse.l2.node import l2_select, shortlist, simulate_record
from hw_dse.l2.system import arrivals, ceil_edge, nearest_rank, simulate, system_metrics
from hw_dse.models.cordic_bitexact import CordicNumerics, cordic_sincos
from hw_dse.rtl.sim import tool_status
from hw_dse.spec import Spec, SystemScenario, load_spec
from tests.tooling import tool_mark

FAMS = [
    ArchConfig.from_params("iterative", {"data_width": 10, "n_iter": 9}),
    ArchConfig.from_params("unrolled_k", {"data_width": 10, "n_iter": 9, "k": 4}),
    ArchConfig.from_params("pipelined", {"data_width": 10, "n_iter": 9, "rounding": "round"}),
    ArchConfig.from_params("pipelined_m", {"data_width": 10, "n_iter": 9, "m": 4}),
]


# ---------------------------------------------------------------------------
# Cycle model
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("arch", FAMS, ids=lambda a: a.family)
def test_cycle_model_obeys_its_contract(arch: ArchConfig) -> None:
    """Single request: valid_out exactly latency-1 edges after the accept; the
    FSM families are ready again exactly ii edges later."""
    c = Contract.of(arch)
    vin = np.zeros(80, dtype=bool)
    vin[3] = True
    tr = CycleModel(arch).run(vin, np.full(80, 17))
    assert np.flatnonzero(tr.accepted).tolist() == [3]
    assert np.flatnonzero(tr.valid_out).tolist() == [3 + c.latency - 1]
    not_ready = np.flatnonzero(~tr.ready)
    if arch.is_pipelined:
        assert not_ready.size == 0
    else:
        assert not_ready.tolist() == list(range(4, 3 + c.ii))  # busy from the edge after the accept
    cos, sin = cordic_sincos(np.array([17]), arch.numerics)
    assert tr.cos[tr.valid_out].tolist() == cos.tolist() and tr.sin[tr.valid_out].tolist() == sin.tolist()


@pytest.mark.parametrize("arch", FAMS, ids=lambda a: a.family)
def test_queue_arithmetic_matches_the_cycle_model(arch: ArchConfig) -> None:
    """The one-line contract the SimPy models use (accept_edges) agrees with the
    edge-by-edge model on a bursty queue, request by request."""
    rng = np.random.default_rng(3)
    offers = np.sort(rng.integers(0, 300, size=40))
    thetas = rng.integers(-512, 512, size=40)
    tr = drive_queue(arch, offers, thetas)
    acc = accept_edges(Contract.of(arch), offers)
    assert np.flatnonzero(tr.accepted).tolist() == acc.tolist()
    assert np.flatnonzero(tr.valid_out).tolist() == (acc + Contract.of(arch).latency - 1).tolist()


def test_a_wrong_cycle_model_is_caught() -> None:
    """Mutation: a model one cycle late disagrees with the contract (the check is not vacuous)."""
    arch = FAMS[0]
    late = ArchConfig.from_params("iterative", {"data_width": 10, "n_iter": 10})  # one more step
    vin = np.zeros(60, dtype=bool)
    vin[0] = True
    good, bad = CycleModel(arch).run(vin, np.zeros(60)), CycleModel(late).run(vin, np.zeros(60))
    assert not np.array_equal(good.valid_out, bad.valid_out)


SIM_REQUIRE = {"icarus": "HW_DSE_REQUIRE_RTL", "verilator": "HW_DSE_REQUIRE_SIM"}


@pytest.mark.parametrize("simulator", ["icarus", "verilator"])
def test_cycle_model_matches_generated_rtl_cycle_for_cycle(simulator: str) -> None:
    """Every family, short bursty traces: ready, valid_out and the output codes
    agree with the generated RTL on every edge."""
    ok, why = tool_status(simulator)
    mark = tool_mark(SIM_REQUIRE[simulator], ok, why)
    if mark.args and mark.args[0]:
        pytest.skip(why)
    from hw_dse.l2.validate import CYCLE_CHECK_DESIGNS, validate_cycles

    for arch in CYCLE_CHECK_DESIGNS:
        r = validate_cycles(arch, simulator, n=40, seed=1)
        assert r.passed, r.row()
        assert r.n_edges > r.n_angles  # bubbles and busy cycles were exercised


# ---------------------------------------------------------------------------
# System models and bounds
# ---------------------------------------------------------------------------

SCENARIOS = [
    SystemScenario(kind="bursty", mean_rate_msps=2.0, burst_size=8, n_bursts=300),
    SystemScenario(kind="bursty", mean_rate_msps=20.0, burst_size=4, burst_spacing_ns=3.0, n_bursts=300, seed=5),
    SystemScenario(kind="control_loop", loop_rate_mhz=1.0, requests_per_tick=32, n_ticks=100),
    SystemScenario(kind="dds_mixer", sample_rate_msps=100.0, fifo_depth=8, n_samples=800),
]


def test_simpy_device_follows_the_contract() -> None:
    scn = SCENARIOS[0]
    c = Contract("iterative", 15, 15)
    r = simulate(scn, c, 198.3)
    period = 1000.0 / 198.3
    expect = accept_edges(c, np.array([ceil_edge(t, period) for t in r.arrival_ns]))
    assert r.accept_edge.tolist() == expect.tolist()
    assert np.allclose(r.result_ns, (expect + c.latency - 1) * period)
    assert (r.latency_ns >= (c.latency - 1) * period - 1e-9).all()


@pytest.mark.parametrize("scn", SCENARIOS, ids=lambda s: s.kind)
def test_l1_bounds_are_optimistic(scn: SystemScenario) -> None:
    """For random contracts and clocks, the L1 bound never rejects what the
    simulation accepts: latency bounds <= simulated, throughput bound >= simulated."""
    rng = np.random.default_rng(0)
    for _ in range(25):
        lat = int(rng.integers(3, 33))
        c = Contract("pipelined", lat, 1) if rng.random() < 0.5 else Contract("iterative", lat, lat)
        f = float(rng.uniform(20, 300))
        sim, bnd = system_metrics(scn, c, f), bound_metrics(scn, c, f)
        for k, v in bnd.items():
            if k == "sys_throughput_msps":
                assert v >= sim[k] - 1e-9, (k, c, f)
            elif k == "sys_stall_frac":
                assert v <= sim[k] + 1e-9, (k, c, f)
            else:
                assert v <= sim[k] + 1e-9, (k, c, f)


def test_back_pressure_in_the_dds() -> None:
    scn = SCENARIOS[3]
    slow = system_metrics(scn, Contract("iterative", 15, 15), 198.3)  # 13 MS/s device, 100 MS/s NCO
    fast = system_metrics(scn, Contract("pipelined", 16, 1), 275.0)
    assert slow["sys_stall_frac"] > 0.8 and slow["sys_throughput_msps"] < 14 and slow["sys_max_queue"] == 8
    assert fast["sys_stall_frac"] == 0.0 and abs(fast["sys_throughput_msps"] - 100.0) < 1e-6


def test_arrival_traces_are_fixed_by_the_seed() -> None:
    a1, _ = arrivals(SCENARIOS[1])
    a2, _ = arrivals(SCENARIOS[1])
    assert np.array_equal(a1, a2) and (np.diff(a1) >= 0).all()
    assert nearest_rank(np.array([3.0, 1.0, 2.0]), 50) == 2.0


def test_dds_spectrum() -> None:
    th = phase_codes(16)
    assert th.min() >= -(1 << 15) and th.max() < (1 << 15) and np.unique(th).size == th.size
    low, _ = dds_spectrum(CordicNumerics(8, 6, 8, 0, "trunc"))
    hi, snr = dds_spectrum(CordicNumerics(16, 14, 16, 0, "trunc"))
    assert 35 < low < 55 and 85 < hi < 100 and snr < hi  # more bits, purer tone


# ---------------------------------------------------------------------------
# Specs and the L2 node
# ---------------------------------------------------------------------------

def test_system_spec_validation_and_msps_only_view() -> None:
    s = load_spec("specs/system/multiaxis_control.yaml")
    assert s.system is not None and [c.metric for c in s.system_constraints] == ["sys_p99_batch_us"]
    v = s.without_system()
    assert v.system is None and not v.system_constraints and v.min_throughput_msps == 32
    assert "system" in s.summary() and "system" not in load_spec("specs/dds_250msps.yaml").summary()
    bad = s.model_dump()
    bad["constraints"].append({"metric": "sys_p99_latency_us", "op": ">=", "value": 1})
    with pytest.raises(ValueError):
        Spec.model_validate(bad)
    nosys = s.model_dump()
    nosys["system"] = None
    with pytest.raises(ValueError):
        Spec.model_validate(nosys)


def test_l1_evaluate_carries_bounds_and_l2_replaces_them() -> None:
    spec = load_spec("specs/system/multiaxis_control.yaml")
    arch = ArchConfig.from_params("pipelined_m", {"data_width": 17, "n_iter": 14, "angle_guard": 1, "rounding": "round", "m": 5})
    rec = evaluate(arch, spec)
    assert rec["provenance"]["sys_p99_batch_us"].startswith("estimate: L1 analytic bound")
    assert rec["feasible"]  # the bound (0.434 us) passes the 0.44 us deadline
    sim = simulate_record(rec, spec)
    assert sim["provenance"]["sys_p99_batch_us"].startswith("simulated (hw_dse.l2.system control_loop")
    assert sim["sys_p99_batch_us"] > rec["sys_p99_batch_us"] and not sim["feasible"]  # clock alignment costs it


def test_l2_node_finds_a_winner_the_l1_front_has_pruned() -> None:
    """Regression (M3 review, B1): m=4 has m=5's numerics (same accuracy) and more
    area, so the L1 front holds m=5 alone; m=5 passes the L1 bound but fails the
    simulation. L2 must search every L1-feasible design, not just the front."""
    from hw_dse.agent.summary import merged_front

    spec = load_spec("specs/system/multiaxis_control.yaml")
    recs = [evaluate(ArchConfig.from_params("pipelined_m", {"data_width": 17, "n_iter": 14, "angle_guard": 1,
                                                            "rounding": "round", "m": m}), spec) for m in (3, 4, 5)]
    assert all(r["feasible"] for r in recs)
    front = merged_front(recs, spec)
    assert [r["m"] for r in front] == [5]
    out = l2_select(recs, front[0], spec)
    assert out["status"] == "simulated" and out["winner_changed"]
    assert out["n_l1_feasible"] == 3 and out["n_simulated_feasible"] == 2
    assert out["selected"]["m"] == 4 and out["selected"]["provenance"]["sys_p99_batch_us"].startswith("simulated")
    assert "fails the simulated system constraints" in out["why"]
    assert shortlist(recs, spec, 2)[0]["m"] == 5


def test_l2_node_on_a_spec_without_a_system_only_reports_facts() -> None:
    spec = load_spec("specs/dds_250msps.yaml")
    rec = evaluate(ArchConfig.from_params("pipelined", {"data_width": 18, "n_iter": 15, "angle_guard": 1, "rounding": "round"}), spec)
    out = l2_select([rec], rec, spec)
    assert out["status"] == "facts_only" and out["selected"] is rec and not out["winner_changed"]
    assert out["selected_facts"]["contract"] == {"family": "pipelined", "latency": 17, "ii": 1}
