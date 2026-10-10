"""Cycle-accurate Python model of every family's ready/valid interface.

Why a cycle model at all
------------------------
L1 knows a design's *latency* and *results per cycle* as two numbers. A
system cares about more: when exactly is the next request accepted, what
happens to a request offered while the unit is busy, how long does the
k-th request of a burst wait. Those follow from the interface contract,
which the generated RTL implements and the formal checks
(``formal/latency_*.sv``) prove at W = 8:

* ``ready`` is high when the unit can take an angle this cycle: always for
  the pipelined families, only in the IDLE state for the FSM families;
* an angle is *accepted* at a rising edge where ``valid_in && ready``; an
  angle offered while ``ready`` is low is ignored (the producer holds it);
* the result appears on ``valid_out`` (a one-cycle pulse) ``latency`` edges
  after the accepting edge, counting both edges, with ``cos_out`` /
  ``sin_out`` equal to the golden model's codes;
* after an accept the unit is ready again ``ii`` (initiation interval)
  edges later: 1 for the pipelined families, ``latency`` for the FSM ones
  (it raises ``ready`` in the cycle after the OUT state).

This module models that edge by edge, as a state machine per family, with
no reference to the RTL's internals beyond the documented states. The test
``tests/test_l2.py`` drives the generated RTL and this model with the same
bursty input trace and compares ``ready``, ``valid_out``, ``cos_out`` and
``sin_out`` on every cycle (Verilator and Icarus).

Cycle conventions (the same as ``rtl_harness/tb_generated.sv``)
---------------------------------------------------------------
Edge 0 is the first rising edge after reset is released. For each edge
``t`` the inputs are ``valid_in[t]`` and ``theta[t]`` (what the unit samples
at that edge); ``ready[t]`` is what the unit presents *before* edge ``t``;
``valid_out[t]``, ``cos[t]``, ``sin[t]`` are what it presents *after* edge
``t``. So a design with latency L accepting at edge ``a`` has
``valid_out[a + L - 1] == 1``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from hw_dse.families import ArchConfig
from hw_dse.models.cordic_bitexact import cordic_sincos


@dataclass(frozen=True)
class Contract:
    """The interface timing of one design: all a system model needs.

    ``latency``: edges from the accepting edge to the edge that raises
    ``valid_out``, both inclusive (= :attr:`ArchConfig.latency_cycles`).
    ``ii``: edges between consecutive accepts at full rate.
    """

    family: str
    latency: int
    ii: int

    @staticmethod
    def of(arch: ArchConfig) -> Contract:
        lat = arch.latency_cycles
        return Contract(arch.family, lat, 1 if arch.is_pipelined else lat)

    @staticmethod
    def from_record(rec: dict) -> Contract:
        fam = rec["family"]
        lat = int(rec["latency_cycles"])
        return Contract(fam, lat, 1 if fam in ("pipelined", "pipelined_m") else lat)


@dataclass
class CycleTrace:
    """Per-edge signals of one run (arrays of equal length, one entry per edge)."""

    valid_in: np.ndarray
    theta: np.ndarray
    ready: np.ndarray
    accepted: np.ndarray
    valid_out: np.ndarray
    cos: np.ndarray
    sin: np.ndarray

    def __len__(self) -> int:
        return int(self.valid_in.size)


class CycleModel:
    """Edge-by-edge model of one design's interface.

    The FSM families walk the RTL's documented states
    (IDLE -> PRE -> ITER x steps -> OUT -> IDLE); the pipelined families
    shift a valid bit (and the angle) down a chain of ``latency`` registers.
    Output codes come from :func:`cordic_sincos`, the golden model, so the
    model's job here is purely *when*, never *what*.
    """

    def __init__(self, arch: ArchConfig) -> None:
        self.arch = arch
        self.contract = Contract.of(arch)

    def run(self, valid_in: np.ndarray, theta: np.ndarray) -> CycleTrace:
        valid_in = np.asarray(valid_in, dtype=bool)
        theta = np.asarray(theta, dtype=np.int64)
        n = valid_in.size
        ready = np.zeros(n, dtype=bool)
        acc = np.zeros(n, dtype=bool)
        vout = np.zeros(n, dtype=bool)
        cos = np.zeros(n, dtype=np.int64)
        sin = np.zeros(n, dtype=np.int64)
        out_theta = np.zeros(n, dtype=np.int64)
        if self.arch.is_pipelined:
            self._run_pipelined(valid_in, theta, ready, acc, vout, out_theta)
        else:
            self._run_fsm(valid_in, theta, ready, acc, vout, out_theta)
        if vout.any():
            c, s = cordic_sincos(out_theta[vout], self.arch.numerics)
            cos[vout], sin[vout] = c, s
        return CycleTrace(valid_in, theta, ready, acc, vout, cos, sin)

    def _run_pipelined(self, valid_in: np.ndarray, theta: np.ndarray, ready: np.ndarray, acc: np.ndarray,
                       vout: np.ndarray, out_theta: np.ndarray) -> None:
        # valid_pipe[0] is stage 0 (input register); valid_pipe[L-1] drives
        # valid_out. Reset clears the valid chain only (datapath registers
        # have no reset, which is invisible because valid gates them).
        lat = self.contract.latency
        vpipe = [False] * lat
        tpipe = [0] * lat
        for t in range(valid_in.size):
            ready[t] = True  # tied high: a new angle every cycle
            acc[t] = bool(valid_in[t])
            vpipe = [acc[t], *vpipe[:-1]]
            tpipe = [int(theta[t]), *tpipe[:-1]]
            vout[t] = vpipe[-1]
            out_theta[t] = tpipe[-1]

    def _run_fsm(self, valid_in: np.ndarray, theta: np.ndarray, ready: np.ndarray, acc: np.ndarray,
                 vout: np.ndarray, out_theta: np.ndarray) -> None:
        steps = self.arch.steps
        state, left, held = "IDLE", 0, 0
        for t in range(valid_in.size):
            ready[t] = state == "IDLE"
            if state == "IDLE":
                if valid_in[t]:
                    acc[t] = True
                    held = int(theta[t])
                    state = "PRE"
            elif state == "PRE":
                state, left = "ITER", steps
            elif state == "ITER":
                left -= 1
                if left == 0:
                    state = "OUT"
            else:  # OUT: present the result for one cycle, back to IDLE
                vout[t] = True
                out_theta[t] = held
                state = "IDLE"


def accept_edges(contract: Contract, offer_edges: np.ndarray) -> np.ndarray:
    """Accepting edge of each request, given the edge it is first offered.

    The contract in one line (a queue in front of the unit, first come first
    served): request i is accepted at the first edge that is both at or after
    its offer edge and at least ``ii`` edges after the previous accept. This
    is the arithmetic the SimPy models and the vectorised simulator use; the
    test suite checks it against :class:`CycleModel` (and so, transitively,
    against the RTL).
    """
    out = np.empty(len(offer_edges), dtype=np.int64)
    nxt = -(1 << 62)
    for i, e in enumerate(np.asarray(offer_edges, dtype=np.int64)):
        a = max(int(e), nxt)
        out[i] = a
        nxt = a + contract.ii
    return out


def drive_queue(arch: ArchConfig, offer_edges: np.ndarray, thetas: np.ndarray, extra: int = 4) -> CycleTrace:
    """Run :class:`CycleModel` the way a producer with a queue drives it.

    Request i becomes available at edge ``offer_edges[i]`` (non-decreasing);
    the producer offers the oldest waiting request on ``valid_in`` until it is
    accepted. Returns the trace (long enough for every result to appear).
    """
    offer_edges = np.asarray(offer_edges, dtype=np.int64)
    c = Contract.of(arch)
    n_edges = int(offer_edges.max(initial=0)) + c.ii * len(offer_edges) + c.latency + extra
    vin = np.zeros(n_edges, dtype=bool)
    th = np.zeros(n_edges, dtype=np.int64)
    model = CycleModel(arch)
    # Closed loop: the producer needs the model's ready to know when to move on.
    # The model is causal, so we can find each accept edge from the contract
    # and then replay the whole trace once to get the signals.
    acc = accept_edges(c, offer_edges)
    i = 0
    for t in range(n_edges):
        while i < len(acc) and acc[i] < t:
            i += 1
        if i < len(acc) and offer_edges[i] <= t:
            vin[t] = True
            th[t] = thetas[i]
    return model.run(vin, th)
