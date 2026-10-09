"""Gate-level simulation of the synthesised netlist against the golden model.

RTL simulation (L3) shows the *source* is right. Gate-level simulation shows
the *synthesis result* is still right: that Yosys's optimisation and
technology mapping (LUT packing, CARRY4 chains, constant propagation, FSM
re-encoding) did not change what the circuit computes.

What netlist, exactly
---------------------
The netlist is Yosys's own output after ``synth_xilinx -flatten -abc9 -arch
xc7`` (``write_verilog -noattr``), i.e. the same mapped netlist that
nextpnr-xilinx places and routes in L4. It instantiates 7-series primitives
(``LUT1``..``LUT6``, ``CARRY4``, ``FDRE``, ``FDSE``, ``MUXF7``, ``INV``,
``IBUF``/``OBUF``/``BUFG``), which are simulated with the behavioural models
in Yosys's ``share/xilinx/cells_sim.v`` **from the same Yosys build** that
produced the netlist. It is a *functional* (zero-delay) gate-level
simulation: it is not the post-place-and-route netlist and carries no
timing (timing is covered by nextpnr's static timing analysis in L4).

The harness, the angle sets and the comparison are exactly those of L3
(``rtl_harness/tb_generated.sv``, :mod:`hw_dse.rtl.sim`), so a gate-level row
in ``eval/data/l3_verification.csv`` (level ``gate``) means: every output
code of the mapped netlist equals the golden model's, and the latency is the
documented one.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from hw_dse.families import ArchConfig
from hw_dse.models.cordic_bitexact import sweep_angles
from hw_dse.rtl.generator import REPO_ROOT, generate
from hw_dse.rtl.sim import Verification, compare, simulate
from hw_dse.synth.flow import Runner, synthesize

GATE_BUILD = REPO_ROOT / "build" / "gate"


def _a(family: str, w: int, n: int, ag: int = 0, g: int = 0, rnd: str = "trunc", k: int = 1, m: int = 1) -> ArchConfig:
    return ArchConfig.from_params(family, {"data_width": w, "n_iter": n, "angle_guard": ag, "frac_guard": g,
                                           "rounding": rnd, "k": k, "m": m})


GATE_CONFIGS: list[ArchConfig] = [
    # W = 8, exhaustive (256 angles): every family, both rounding modes
    _a("iterative", 8, 6), _a("iterative", 8, 9, -1, 2, "round"),
    _a("unrolled_k", 8, 6, k=2), _a("unrolled_k", 8, 9, -1, 2, "round", k=4),
    _a("pipelined", 8, 6), _a("pipelined", 8, 9, 2, 1, "round"),
    _a("pipelined_m", 8, 7, m=3), _a("pipelined_m", 8, 9, -1, 2, "round", m=2),
    # W = 16, exhaustive (65,536 angles): every family
    _a("iterative", 16, 14), _a("unrolled_k", 16, 14, 2, 2, "round", k=4),
    _a("pipelined", 16, 14), _a("pipelined_m", 16, 14, m=4),
]


def netlist_for(arch: ArchConfig, runner: Runner | None = None, root: Path = GATE_BUILD) -> tuple[Path, Path, str]:
    """Synthesise ``arch`` with Yosys only; return (netlist, cells_sim.v, description)."""
    runner = runner or Runner.from_env()
    d = generate(arch)
    wd = root / d.module
    src = d.write(wd)
    res = synthesize([src], d.module, arch.numerics.data_width, wd, runner, pnr=False)
    cells = runner.cells_sim(wd)
    ver = runner.versions(wd)["yosys"]
    desc = f"yosys {ver} synth_xilinx -flatten -abc9 netlist (write_verilog) + its xilinx/cells_sim.v; zero-delay; " \
           f"{res.luts} LUT, {res.ffs} FF, {res.carry4} CARRY4 cells"
    return wd / f"{d.module}_netlist.v", cells, desc


def verify_gate(arch: ArchConfig, simulator: str, runner: Runner | None = None, angles: np.ndarray | None = None,
                root: Path = GATE_BUILD, netlist: tuple[Path, Path, str] | None = None) -> Verification:
    codes, sweep = sweep_angles(arch.numerics.data_width)
    if angles is None:
        angles = np.asarray(codes)
    else:
        sweep = f"subset ({len(angles)} angles)"
    net, cells, desc = netlist or netlist_for(arch, runner, root)
    d = generate(arch)
    res = simulate([net, cells], d.module, arch.numerics.data_width, np.asarray(angles), simulator, workdir=None)
    return compare(arch, res, np.asarray(angles), sweep, simulator, level="gate", netlist=desc)
