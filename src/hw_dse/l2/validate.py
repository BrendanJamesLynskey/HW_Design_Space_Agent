"""Validate the L2 cycle model against the generated RTL, cycle for cycle.

The L3 harness (``rtl_harness/tb_generated.sv``) can insert idle cycles
before each angle (``+gaps=``) and log every rising edge (``+cycles=``).
That turns the L3 back-to-back stream into a short *bursty* trace with
bubbles, back-to-back runs and angles offered while an FSM design is busy.

:func:`validate_cycles` runs one design through Verilator or Icarus with
such a trace, then feeds the *same per-edge inputs the RTL saw*
(``valid_in``, ``theta``, from the log) into :class:`CycleModel` and
compares, on every edge:

* ``ready`` (what the unit presented before the edge),
* ``valid_out`` (what it presented after the edge),
* ``cos_out`` / ``sin_out`` whenever ``valid_out`` is high.

Driving the model with the logged inputs (rather than re-deriving them from
the gap list) keeps the check independent of the harness's own
producer logic. Every mismatch counts; the result is *exact*.
"""

from __future__ import annotations

import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from hw_dse.families import ArchConfig
from hw_dse.l2.cycle import CycleModel
from hw_dse.rtl.generator import generate
from hw_dse.rtl.sim import simulate, tool_version


@dataclass
class CycleCheck:
    simulator: str
    simulator_version: str
    key: str
    family: str
    n_angles: int
    n_edges: int
    n_accepts: int
    n_results: int
    ready_mismatches: int
    valid_mismatches: int
    data_mismatches: int

    @property
    def passed(self) -> bool:
        return (self.ready_mismatches == 0 and self.valid_mismatches == 0 and self.data_mismatches == 0
                and self.n_results == self.n_angles and self.n_accepts == self.n_angles)

    def row(self) -> dict[str, object]:
        return {**asdict(self), "passed": self.passed}


def bursty_trace(n: int, seed: int, max_gap: int = 24) -> tuple[np.ndarray, np.ndarray]:
    """``n`` random angle codes in [-2^(W-1), 2^(W-1)) scaled later, and gaps:
    half the angles back to back (gap 0), the rest after 1..max_gap idle cycles."""
    rng = np.random.default_rng(seed)
    gaps = np.where(rng.random(n) < 0.5, 0, rng.integers(1, max_gap + 1, size=n))
    return rng.random(n), gaps.astype(np.int64)


def validate_cycles(arch: ArchConfig, simulator: str = "icarus", n: int = 40, seed: int = 1) -> CycleCheck:
    w = arch.numerics.data_width
    u, gaps = bursty_trace(n, seed)
    angles = (np.floor(u * (1 << w)) - (1 << (w - 1))).astype(np.int64)
    design = generate(arch)
    with tempfile.TemporaryDirectory(prefix="hw_dse_l2_") as tmp:
        src = design.write(Path(tmp))
        res = simulate([src], design.module, w, angles, simulator, gaps=gaps, log_cycles=True)
    log = res.cycles
    assert log is not None and log.shape[0] > 1, "no cycle log"
    vin, th, rdy_rtl, vout_rtl = log[:, 1].astype(bool), log[:, 2], log[:, 3].astype(bool), log[:, 4].astype(bool)
    cos_rtl, sin_rtl = log[:, 5], log[:, 6]
    model = CycleModel(arch).run(vin, th)
    # Log row e: inputs and ready at edge e; outputs produced by edge e-1.
    ready_mm = int(np.count_nonzero(model.ready != rdy_rtl))
    m_vout, r_vout = model.valid_out[:-1], vout_rtl[1:]
    valid_mm = int(np.count_nonzero(m_vout != r_vout))
    both = m_vout & r_vout
    data_mm = int(np.count_nonzero((model.cos[:-1][both] != cos_rtl[1:][both]) | (model.sin[:-1][both] != sin_rtl[1:][both])))
    return CycleCheck(simulator, tool_version(simulator), arch.key(), arch.family, n, int(log.shape[0]),
                      int(np.count_nonzero(vin & rdy_rtl)), int(np.count_nonzero(r_vout)), ready_mm, valid_mm, data_mm)


# Short traces, one design per family and both rounding modes, N not a
# multiple of k or m, negative and positive angle guard: the configurations
# the CI check runs.
CYCLE_CHECK_DESIGNS: list[ArchConfig] = [
    ArchConfig.from_params("iterative", {"data_width": 8, "n_iter": 6}),
    ArchConfig.from_params("iterative", {"data_width": 10, "n_iter": 9, "angle_guard": 1, "frac_guard": 1, "rounding": "round"}),
    ArchConfig.from_params("unrolled_k", {"data_width": 8, "n_iter": 7, "k": 3}),
    ArchConfig.from_params("unrolled_k", {"data_width": 9, "n_iter": 8, "angle_guard": -1, "rounding": "round", "k": 2}),
    ArchConfig.from_params("pipelined", {"data_width": 8, "n_iter": 6}),
    ArchConfig.from_params("pipelined", {"data_width": 10, "n_iter": 9, "frac_guard": 2, "rounding": "round"}),
    ArchConfig.from_params("pipelined_m", {"data_width": 8, "n_iter": 7, "m": 3}),
    ArchConfig.from_params("pipelined_m", {"data_width": 12, "n_iter": 11, "angle_guard": 2, "frac_guard": 1, "m": 4}),
]


def main() -> None:  # pragma: no cover - writes eval/data/l2_cycle_validation.csv
    import csv

    from hw_dse.rtl.generator import REPO_ROOT

    rows = []
    for sim in ("verilator", "icarus"):
        for a in CYCLE_CHECK_DESIGNS:
            for seed in (1, 2, 3):
                r = validate_cycles(a, sim, n=60, seed=seed)
                rows.append({**r.row(), "seed": seed})
                print(sim, a.key(), seed, "PASS" if r.passed else "FAIL", r.row())
    out = REPO_ROOT / "eval" / "data" / "l2_cycle_validation.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("wrote", out)


if __name__ == "__main__":  # pragma: no cover
    main()
