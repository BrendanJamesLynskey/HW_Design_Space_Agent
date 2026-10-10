"""L1 screening for system constraints: analytic bounds that never reject a good design.

A system constraint ("p99 latency <= 0.4 us with bursts of 8") is decided by
L2 simulation, but only the shortlist is simulated. The L1 explorer still
needs to know which designs are worth keeping, so each constrainable system
metric gets an analytic *bound* that is optimistic in the constraint's
direction:

=====================  =========================================================
metric (constraint)    L1 bound (from the contract: latency L, ii, period T)
=====================  =========================================================
``sys_p99_latency_us``  lower bound: every burst (tick) served alone, starting
``sys_p50_latency_us``  on a clock edge: request j of a burst waits for the j
(<=)                    before it, ``c_j = max(j*s, c_{j-1} + ii*T)``, latency
                        ``c_j - j*s + (L-1)*T``; the percentile is taken over
                        the same multiset of requests the simulation has
``sys_p99_batch_us``    lower bound: one tick's ``R`` requests alone,
(<=)                    ``(R-1)*ii*T + (L-1)*T``
``sys_throughput_msps`` upper bound: n results over the longer of the offered
(>=)                    traffic's span and ``((n-1)*ii + L-1)*T`` (DDS: the
                        emission time the device's rate forces past the FIFO)
``sys_stall_frac``      lower bound: the stall the device's rate forces once the
(<=)                    FIFO is full
``sys_sfdr_dbc``,       not bounds: the exact golden-model DDS spectrum
``sys_snr_db`` (>=)     (cheap, numerics only), the same at L1 and L2
=====================  =========================================================

Why these are bounds: in the simulation a request is accepted at the first
edge at or after its arrival that is ``ii`` edges past the previous accept,
so it can only wait *longer* than in the isolated, edge-aligned case
(clock alignment and backlog from earlier bursts only add), request by
request; percentiles are monotone under that element-wise ordering. So
"bound fails" implies "simulation fails", and L1 screening never discards
a design L2 would accept. ``tests/test_l2.py`` checks the inequality on
random designs for every scenario.
"""

from __future__ import annotations

import numpy as np

from hw_dse.l2.cycle import Contract
from hw_dse.l2.system import nearest_rank, nominal_span_ns
from hw_dse.spec import SystemScenario

BOUND_PROVENANCE = "estimate: L1 analytic bound of the system metric (optimistic; L2 simulates the shortlist)"


def _isolated_burst_latencies(n: int, spacing: float, contract: Contract, period: float) -> np.ndarray:
    c = np.zeros(n)
    for j in range(1, n):
        c[j] = max(j * spacing, c[j - 1] + contract.ii * period)
    return c - np.arange(n) * spacing + (contract.latency - 1) * period


def bound_metrics(scn: SystemScenario, contract: Contract, fmax_mhz: float) -> dict[str, float]:
    """Optimistic L1 values of the constrainable timing metrics (us, MS/s)."""
    t = 1000.0 / float(fmax_mhz)
    dev_rate = 1000.0 / (contract.ii * t)
    out: dict[str, float] = {}
    if scn.kind in ("bursty", "control_loop"):
        if scn.kind == "bursty":
            b, s, reps = int(scn.burst_size), float(scn.burst_spacing_ns), int(scn.n_bursts)  # type: ignore[arg-type]
        else:
            b, s, reps = int(scn.requests_per_tick), 0.0, int(scn.n_ticks)  # type: ignore[arg-type]
        lat_us = np.tile(_isolated_burst_latencies(b, s, contract, t), reps) / 1000.0
        out["sys_p50_latency_us"] = nearest_rank(lat_us, 50)
        out["sys_p99_latency_us"] = nearest_rank(lat_us, 99)
        # n results need at least (n-1)*ii edges plus one latency after the first arrival.
        n = b * reps
        out["sys_throughput_msps"] = n * 1000.0 / max(nominal_span_ns(scn), ((n - 1) * contract.ii + contract.latency - 1) * t)
        if scn.kind == "control_loop":
            out["sys_p99_batch_us"] = ((b - 1) * contract.ii * t + (contract.latency - 1) * t) / 1000.0
    else:  # dds_mixer
        n, d = int(scn.n_samples), int(scn.fifo_depth)
        ts = 1000.0 / float(scn.sample_rate_msps)  # type: ignore[arg-type]
        nominal = (n - 1) * ts
        forced = max(0, n - 1 - d) * contract.ii * t  # the device must have accepted n-1-d samples
        actual = max(nominal, forced)
        out["sys_throughput_msps"] = (n - 1) * 1000.0 / actual
        out["sys_stall_frac"] = max(0.0, 1.0 - nominal / actual)
        out["sys_p50_latency_us"] = out["sys_p99_latency_us"] = (contract.latency - 1) * t / 1000.0
    return out
