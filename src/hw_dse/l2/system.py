"""SimPy models of the CORDIC inside a system, and the metrics they produce.

Three systems, one device
-------------------------
Every scenario (:class:`hw_dse.spec.SystemScenario`) is a producer, an input
FIFO and the same CORDIC *device* process:

``dds_mixer``
    An NCO (phase accumulator) produces one phase word every ``1/fs`` and
    pushes it into a FIFO of ``fifo_depth``. When the FIFO is full the NCO
    *stalls* until a slot frees: that is back-pressure, and it is how a
    design too slow for the sample rate shows up (sustained throughput below
    ``fs``, a non-zero stall fraction) instead of silently dropping samples.
``control_loop``
    A control tick every ``1/loop_rate`` issues ``requests_per_tick`` requests
    at the same instant (e.g. 16 motor axes, each needing a Park and an
    inverse-Park transform). The loop cares about the *batch*: the time from
    the tick to its last result.
``bursty``
    Bursts of ``burst_size`` requests arrive as a Poisson process (fixed
    seed, so every design sees the identical arrival trace: common random
    numbers make the comparison between designs fair).

The device
----------
The CORDIC runs on its own clock with period ``T = 1000 / Fmax`` ns (the
*estimated* Fmax, as every L1 throughput figure in the project). It follows
the interface contract (:class:`hw_dse.l2.cycle.Contract`), which the cycle
model implements and the RTL is checked against cycle for cycle:

* the oldest waiting request is accepted at the first clock edge at or after
  its arrival at which the device is ready (edges are at integer multiples
  of ``T``; the device is ready again ``ii`` edges after an accept);
* its result is valid ``latency - 1`` edges after the accepting edge.

Edges are kept as integers and converted to time only for reporting, so the
arithmetic is exact and repeatable.

Metrics (all labelled ``simulated``)
------------------------------------
``sys_throughput_msps``
    Results delivered per microsecond over the run: from the first arrival to
    the later of the last result and the end of the offered traffic (DDS: the
    NCO's actual emission rate, which back-pressure lowers).
``sys_p50_latency_us`` / ``sys_p99_latency_us``
    Request latency, arrival (or NCO emission) to result valid; nearest-rank
    percentiles, so the number is one of the simulated latencies.
``sys_p99_batch_us``
    (control loop) tick to the last result of that tick, p99 over ticks.
``sys_stall_frac``
    (DDS) 1 - nominal duration / actual duration of the NCO's run.
``sys_utilisation``
    Fraction of the run the device's input slots were taken (n * ii * T over
    the run's length).
``sys_max_queue``
    Deepest the input FIFO got (requests waiting, not yet accepted).
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

import numpy as np
import simpy

from hw_dse.l2 import L2_VERSION
from hw_dse.l2.cycle import Contract
from hw_dse.spec import SystemScenario

EDGE_EPS = 1e-9  # relative slack when snapping a time to the next clock edge


def ceil_edge(t_ns: float, period_ns: float) -> int:
    """Index of the first clock edge at or after ``t_ns`` (edges at k * period)."""
    return int(math.ceil(t_ns / period_ns - EDGE_EPS))


def nearest_rank(values: np.ndarray, q: float) -> float:
    """Nearest-rank percentile: always one of the values (no interpolation)."""
    v = np.sort(np.asarray(values, dtype=float))
    if v.size == 0:
        return float("nan")
    return float(v[max(0, math.ceil(q / 100.0 * v.size) - 1)])


def simpy_version() -> str:
    return f"SimPy {getattr(simpy, '__version__', '?')}"


def provenance(scn: SystemScenario, fmax_mhz: float, clock_source: str = "estimated Fmax") -> str:
    return (f"simulated (hw_dse.l2.system {scn.kind} {L2_VERSION}, {simpy_version()}; CORDIC clock "
            f"{fmax_mhz:.4g} MHz = {clock_source})")


# ---------------------------------------------------------------------------
# Arrival traces (shared by every design: common random numbers)
# ---------------------------------------------------------------------------

def arrivals(scn: SystemScenario) -> tuple[np.ndarray, np.ndarray]:
    """Arrival times (ns, non-decreasing) and a group id per request.

    Group = control tick or burst index (used for batch latency). The DDS
    scenario has no fixed arrival trace (back-pressure shapes it), so it is
    not handled here.
    """
    if scn.kind == "control_loop":
        period = 1000.0 / float(scn.loop_rate_mhz)  # type: ignore[arg-type]
        r = int(scn.requests_per_tick)  # type: ignore[arg-type]
        ticks = np.arange(scn.n_ticks, dtype=float) * period
        return np.repeat(ticks, r), np.repeat(np.arange(scn.n_ticks), r)
    if scn.kind == "bursty":
        b = int(scn.burst_size)  # type: ignore[arg-type]
        mean_gap = b / float(scn.mean_rate_msps) * 1000.0  # type: ignore[arg-type]
        rng = np.random.default_rng(scn.seed)
        starts = np.cumsum(rng.exponential(mean_gap, size=scn.n_bursts))
        offs = np.arange(b, dtype=float) * scn.burst_spacing_ns
        times = (starts[:, None] + offs[None, :]).ravel()
        groups = np.repeat(np.arange(scn.n_bursts), b)
        order = np.argsort(times, kind="stable")  # overlapping bursts interleave in time order
        return times[order], groups[order]
    raise ValueError(f"no fixed arrival trace for {scn.kind}")


def nominal_span_ns(scn: SystemScenario) -> float:
    """How long the offered traffic lasts, independent of the design: the run is
    at least this long. Control loop: ``n_ticks`` periods; bursty: the arrival
    trace's span plus one mean inter-burst gap."""
    if scn.kind == "control_loop":
        return scn.n_ticks * 1000.0 / float(scn.loop_rate_mhz)  # type: ignore[arg-type]
    if scn.kind == "bursty":
        a, _ = arrivals(scn)
        return float(a.max() - a.min()) + int(scn.burst_size) / float(scn.mean_rate_msps) * 1000.0  # type: ignore[arg-type]
    return (int(scn.n_samples) - 1) * 1000.0 / float(scn.sample_rate_msps)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# SimPy model
# ---------------------------------------------------------------------------

@dataclass
class _Req:
    idx: int
    t_arr: float


@dataclass
class _Fifo:
    """A FIFO with optional capacity, and wake-up events for both sides."""

    env: simpy.Environment
    capacity: int | None = None
    items: deque = field(default_factory=deque)
    max_depth: int = 0

    def __post_init__(self) -> None:
        self._nonempty = self.env.event()
        self._space = self.env.event()

    @property
    def full(self) -> bool:
        return self.capacity is not None and len(self.items) >= self.capacity

    def push(self, r: _Req) -> None:
        self.items.append(r)
        self.max_depth = max(self.max_depth, len(self.items))
        if not self._nonempty.triggered:
            self._nonempty.succeed()

    def pop(self) -> _Req:
        r = self.items.popleft()
        if not self._space.triggered:
            self._space.succeed()
        return r

    def wait_nonempty(self) -> simpy.Event:
        if self._nonempty.triggered:
            self._nonempty = self.env.event()
        return self._nonempty

    def wait_space(self) -> simpy.Event:
        if self._space.triggered:
            self._space = self.env.event()
        return self._space


@dataclass
class SimResult:
    """Raw per-request timings of one simulation (ns; edges are integers)."""

    arrival_ns: np.ndarray
    accept_edge: np.ndarray
    result_ns: np.ndarray
    group: np.ndarray
    period_ns: float
    contract: Contract
    max_queue: int
    nominal_ns: float = 0.0  # DDS: how long the NCO's run should have taken

    @property
    def latency_ns(self) -> np.ndarray:
        return self.result_ns - self.arrival_ns


def _device(env: simpy.Environment, fifo: _Fifo, contract: Contract, period: float, n: int,
            acc: np.ndarray, res: np.ndarray) -> Any:
    nxt = -(1 << 62)
    for _ in range(n):
        while not fifo.items:
            yield fifo.wait_nonempty()
        head = fifo.items[0]
        k = max(ceil_edge(head.t_arr, period), nxt)
        if k * period > env.now:
            yield env.timeout(k * period - env.now)
        r = fifo.pop()
        acc[r.idx] = k
        res[r.idx] = (k + contract.latency - 1) * period
        nxt = k + contract.ii


def simulate(scn: SystemScenario, contract: Contract, fmax_mhz: float) -> SimResult:
    """Run one scenario for one design; return per-request timings."""
    period = 1000.0 / float(fmax_mhz)
    env = simpy.Environment()
    if scn.kind == "dds_mixer":
        n = int(scn.n_samples)
        ts = 1000.0 / float(scn.sample_rate_msps)  # type: ignore[arg-type]
        fifo = _Fifo(env, capacity=int(scn.fifo_depth))
        arr = np.zeros(n)
        groups = np.arange(n)

        def nco() -> Any:
            for i in range(n):
                if i:
                    yield env.timeout(ts)
                while fifo.full:  # back-pressure: the NCO waits for a free slot
                    yield fifo.wait_space()
                arr[i] = env.now
                fifo.push(_Req(i, env.now))

        env.process(nco())
        nominal = (n - 1) * ts
    else:
        arr, groups = arrivals(scn)
        n = arr.size
        fifo = _Fifo(env)

        def source() -> Any:
            for i, t in enumerate(arr):
                if t > env.now:
                    yield env.timeout(t - env.now)
                fifo.push(_Req(i, float(t)))

        env.process(source())
        nominal = 0.0
    acc = np.zeros(n, dtype=np.int64)
    res = np.zeros(n)
    env.process(_device(env, fifo, contract, period, n, acc, res))
    env.run()
    return SimResult(np.asarray(arr, dtype=float), acc, res, np.asarray(groups), period, contract, fifo.max_depth, nominal)


def metrics(scn: SystemScenario, r: SimResult) -> dict[str, float]:
    """System metrics from one simulation (see the module docstring)."""
    lat_us = r.latency_ns / 1000.0
    n = lat_us.size
    # The run lasts from the first arrival until the last result, and at least
    # as long as the offered traffic itself.
    span_ns = max(float(r.result_ns.max() - r.arrival_ns.min()), nominal_span_ns(scn) if scn.kind != "dds_mixer" else 0.0)
    out: dict[str, float] = {
        "sys_throughput_msps": n * 1000.0 / span_ns if span_ns > 0 else float("inf"),
        "sys_p50_latency_us": nearest_rank(lat_us, 50),
        "sys_p99_latency_us": nearest_rank(lat_us, 99),
        "sys_utilisation": min(1.0, n * r.contract.ii * r.period_ns / span_ns) if span_ns > 0 else 1.0,
        "sys_max_queue": float(r.max_queue),
    }
    if scn.kind == "control_loop":
        period = 1000.0 / float(scn.loop_rate_mhz)  # type: ignore[arg-type]
        last = np.full(int(r.group.max()) + 1, -np.inf)
        np.maximum.at(last, r.group, r.result_ns)
        batch_us = (last - np.arange(last.size) * period) / 1000.0
        out["sys_p99_batch_us"] = nearest_rank(batch_us, 99)
    if scn.kind == "dds_mixer":
        actual = float(r.arrival_ns.max() - r.arrival_ns.min())
        out["sys_stall_frac"] = max(0.0, 1.0 - r.nominal_ns / actual) if actual > 0 else 0.0
        out["sys_throughput_msps"] = (n - 1) * 1000.0 / actual if actual > 0 else float("inf")
    return out


@lru_cache(maxsize=8192)
def _cached(scn_json: str, family: str, latency: int, ii: int, fmax_mhz: float) -> tuple[tuple[str, float], ...]:
    scn = SystemScenario.model_validate_json(scn_json)
    r = simulate(scn, Contract(family, latency, ii), fmax_mhz)
    return tuple(sorted(metrics(scn, r).items()))


def system_metrics(scn: SystemScenario, contract: Contract, fmax_mhz: float) -> dict[str, float]:
    """Cached :func:`metrics` of :func:`simulate`. The timing metrics depend only
    on (latency, ii, Fmax): 635,040 registry designs share 1,092 such tuples."""
    fam = "pipelined" if contract.ii == 1 else "iterative"  # the family only matters through ii
    return dict(_cached(scn.model_dump_json(), fam, contract.latency, contract.ii, float(fmax_mhz)))
