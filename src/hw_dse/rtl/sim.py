"""Simulate generated RTL (or a gate-level netlist) and compare with the golden model.

This module is the L3 "verified" step: it turns "the generator emitted some
SystemVerilog" into "the SystemVerilog computes exactly what the golden
model computes, on every input angle". Every number it produces is *exact*:
a mismatch count from a complete comparison over a documented angle set.

Two independent simulators
--------------------------
* **Verilator** (primary): compiles the design and ``rtl_harness/tb_generated.sv``
  to C++ (``--binary --timing``), so even exhaustive sweeps of slow FSM
  designs take seconds.
* **Icarus Verilog** (second opinion): an event-driven interpreter with
  four-state logic, so X propagation from an uninitialised register would
  show up as a harness ``$fatal`` rather than an accidental match.

Both run the same harness and the same angle file, and their outputs are
checked against :func:`hw_dse.models.cordic_bitexact.cordic_sincos`
independently. Agreement between two simulators *and* the model is the bar.

Which angles
------------
:func:`hw_dse.models.cordic_bitexact.sweep_angles`, the same set the
accuracy metrics use: **all 2^W angles for W <= 16**, and for W > 16 a dense
documented set (2^16 evenly strided codes plus 2^16 seeded-random codes).

What is checked
---------------
* every (cos, sin) output code equals the model's, angle by angle;
* the harness saw exactly one result per angle, in order;
* the measured latency of every result equals the documented latency
  (:attr:`hw_dse.families.ArchConfig.latency_cycles`).

Tools that are missing make :func:`tool_status` say so; the tests use that
to skip cleanly locally, and CI sets ``HW_DSE_REQUIRE_SIM=1`` to turn a
skip into a failure.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from hw_dse.families import ArchConfig
from hw_dse.models.cordic_bitexact import cordic_sincos, sweep_angles
from hw_dse.rtl.generator import REPO_ROOT, generate

HARNESS = REPO_ROOT / "rtl_harness" / "tb_generated.sv"
SIMULATORS = ("verilator", "icarus")


def tool_status(simulator: str) -> tuple[bool, str]:
    """(available, reason-if-not) for ``simulator``."""
    need = {"verilator": ["verilator"], "icarus": ["iverilog", "vvp"]}[simulator]
    missing = [t for t in need if shutil.which(t) is None]
    return (not missing, f"{', '.join(missing)} not on PATH" if missing else "")


def tool_version(simulator: str) -> str:
    """One-line version string, recorded next to every result."""
    try:
        if simulator == "verilator":
            out = subprocess.run(["verilator", "--version"], capture_output=True, text=True).stdout
            return out.strip().split(" rev")[0]
        out = subprocess.run(["iverilog", "-V"], capture_output=True, text=True).stdout
        m = re.search(r"version\s+(\S+)", out)
        return f"Icarus Verilog {m.group(1) if m else '?'}"
    except OSError:
        return "unavailable"


@dataclass
class SimResult:
    theta: np.ndarray
    cos: np.ndarray
    sin: np.ndarray
    latency: np.ndarray
    seconds: float
    cycles: np.ndarray | None = None  # L2 per-cycle log (see tb_generated.sv), when requested


def simulate(sources: list[Path], top: str, width: int, angles: np.ndarray, simulator: str = "verilator",
             timeout_s: float = 1800.0, workdir: Path | None = None, gaps: np.ndarray | None = None,
             log_cycles: bool = False) -> SimResult:
    """Drive ``top`` (from ``sources``) with ``angles`` through the uniform harness.

    ``gaps`` (L2) holds the idle cycles the harness waits before offering
    each angle, which turns the L3 back-to-back stream into a bursty one;
    ``log_cycles`` (L2) also returns the harness's per-cycle log as an
    ``(n_cycles, 7)`` array: cycle, valid_in, theta, ready, valid_out, cos, sin.
    Both default to the L3 behaviour (no gaps, no log).
    """
    ok, why = tool_status(simulator)
    if not ok:
        raise RuntimeError(why)
    angles = np.asarray(angles, dtype=np.int64)
    maxn = max(1024, int(angles.size))
    with tempfile.TemporaryDirectory(prefix="hw_dse_sim_", dir=workdir) as tmp:
        t = Path(tmp)
        af, of = t / "angles.txt", t / "out.txt"
        af.write_text(f"{angles.size}\n" + "\n".join(str(int(a)) for a in angles) + "\n")
        extra: list[str] = []
        if gaps is not None:
            gf = t / "gaps.txt"
            gf.write_text("\n".join(str(int(g)) for g in np.asarray(gaps)) + "\n")
            extra.append(f"+gaps={gf}")
        cf = t / "cycles.txt"
        if log_cycles:
            extra.append(f"+cycles={cf}")
        defines = [f"HW_DUT={top}", f"HW_W={width}", f"HW_MAXN={maxn}"]
        t0 = time.time()
        if simulator == "icarus":
            exe = t / "sim.vvp"
            cmd = ["iverilog", "-g2012", "-o", str(exe), "-s", "tb_generated"]
            cmd += [f"-D{d}" for d in defines] + [str(HARNESS), *map(str, sources)]
            _run(cmd, timeout_s)
            _run(["vvp", "-n", str(exe), f"+angles={af}", f"+out={of}", *extra], timeout_s)
        else:
            obj = t / "obj"
            # HW_DSE_JOBS caps Verilator's build parallelism (default 0 = every core).
            jobs = os.environ.get("HW_DSE_JOBS", "0")
            cmd = ["verilator", "--binary", "--timing", "-j", jobs, "-O2", "--top-module", "tb_generated",
                   "-Wno-fatal", "-Wno-lint", "-Wno-style", "--Mdir", str(obj)]
            cmd += [f"+define+{d}" for d in defines] + [str(HARNESS), *map(str, sources)]
            _run(cmd, timeout_s)
            _run([str(obj / "Vtb_generated"), f"+angles={af}", f"+out={of}", *extra], timeout_s)
        secs = time.time() - t0
        data = np.loadtxt(of, dtype=np.int64, ndmin=2) if of.stat().st_size else np.zeros((0, 4), dtype=np.int64)
        cyc = None
        if log_cycles:
            cyc = np.loadtxt(cf, dtype=np.int64, ndmin=2) if cf.exists() and cf.stat().st_size else np.zeros((0, 7), dtype=np.int64)
    return SimResult(data[:, 0], data[:, 1], data[:, 2], data[:, 3], secs, cyc)


def _run(cmd: list[str], timeout_s: float) -> None:
    p = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout_s)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed ({p.returncode}):\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}")


@dataclass
class Verification:
    """One row of ``eval/data/l3_verification.csv``."""

    level: str  # "rtl" (generated SystemVerilog) or "gate" (synthesised netlist)
    simulator: str
    simulator_version: str
    family: str
    key: str
    data_width: int
    n_iter: int
    angle_guard: int
    frac_guard: int
    rounding: str
    k: int
    m: int
    sweep: str
    n_angles: int
    n_results: int
    mismatches: int
    latency_expected: int
    latency_measured: str  # "L" if all equal, else "min..max"
    latency_ok: bool
    seconds: float
    netlist: str = ""  # gate level: which netlist was simulated

    @property
    def passed(self) -> bool:
        return self.mismatches == 0 and self.latency_ok and self.n_results == self.n_angles

    def row(self) -> dict[str, object]:
        d = asdict(self)
        d["passed"] = self.passed
        return d


def compare(arch: ArchConfig, res: SimResult, angles: np.ndarray, sweep: str, simulator: str, level: str = "rtl",
            netlist: str = "") -> Verification:
    """Score a simulation against the golden model."""
    n = arch.numerics
    complete = res.theta.size == angles.size and np.array_equal(res.theta, angles)
    if complete:
        cos_m, sin_m = cordic_sincos(angles, n)
        mism = int(np.count_nonzero((cos_m != res.cos) | (sin_m != res.sin)))
    else:
        mism = int(angles.size)  # missing or out-of-order results count as wrong
    lat = res.latency
    lat_s = "none" if lat.size == 0 else (str(int(lat[0])) if lat.min() == lat.max() else f"{lat.min()}..{lat.max()}")
    return Verification(
        level=level, simulator=simulator, simulator_version=tool_version(simulator), family=arch.family, key=arch.key(),
        data_width=n.data_width, n_iter=n.n_iter, angle_guard=n.A - n.data_width, frac_guard=n.frac_guard,
        rounding=n.rounding, k=arch.k, m=arch.m, sweep=sweep, n_angles=int(angles.size), n_results=int(res.theta.size),
        mismatches=mism, latency_expected=arch.latency_cycles, latency_measured=lat_s,
        latency_ok=bool(lat.size and lat.min() == lat.max() == arch.latency_cycles), seconds=round(res.seconds, 2),
        netlist=netlist,
    )


def verify_rtl(arch: ArchConfig, simulator: str = "verilator", angles: np.ndarray | None = None,
               build_dir: Path | None = None) -> Verification:
    """Generate ``arch``, simulate it on the documented sweep, compare."""
    sweep_codes, sweep = sweep_angles(arch.numerics.data_width)
    if angles is None:
        angles = np.asarray(sweep_codes)
    else:
        sweep = f"subset ({len(angles)} angles)"
    design = generate(arch)
    with tempfile.TemporaryDirectory(prefix="hw_dse_gen_", dir=build_dir) as tmp:
        src = design.write(Path(tmp))
        res = simulate([src], design.module, design.data_width, angles, simulator)
    return compare(arch, res, np.asarray(angles), sweep, simulator)


def require_env(var: str) -> bool:
    """True if CI asked for this class of test to be mandatory."""
    return os.environ.get(var) == "1"
