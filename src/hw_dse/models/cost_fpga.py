"""Analytical FPGA cost model for the CORDIC families (provenance: estimate).

This model answers "roughly how many LUTs and flip-flops, and roughly how
fast?" in microseconds, so an optimiser can afford thousands of queries.
It is *structural*: it counts the hardware each family must contain (adder
bits, register bits, multiplexer LUTs) from the parameters, then converts
those counts to Artix-7 resources and delay with a handful of constants.

**Read this before trusting any number it produces.** The free constants
are calibrated to exactly two real synthesis results (the reference
iterative and pipelined CORDICs at W=16, N=14, Vivado 2025.2,
xc7a35tcpg236-1). Two anchor points is a weak calibration: it pins the
model at the defaults and makes it *plausible* elsewhere, but every point
away from W=16/N=14, and the two families that have no anchor at all
(``unrolled_k``, ``pipelined_m``), are extrapolations. Milestone 2 adds
real synthesis runs across the space and recalibrates (milestone 2's L5
back-annotation step exists precisely to measure and correct this).

Structure of the model
----------------------
Notation: W data width, N iterations, A angle width, g fractional guard
bits, WX = W+2+g (x/y register width), WZ = A+2 (z register width).

**LUTs** = c_arith * arith_bits + c_mux * mux_luts

* ``arith_bits``: one LUT per adder/subtractor bit (7-series adders are a
  LUT per bit feeding the CARRY4 chain). Each micro-rotation needs two
  WX-bit add/subs (x, y) and one WZ-bit add/sub (z). The FSM families add
  a small control term (iteration counter + FSM). The pipelined families
  get two constant-propagation trims synthesis reliably performs: the
  first micro-rotation sees y=0, so its x/y adders vanish, and the last
  stage's z adder has no consumer.
* ``mux_luts``: the FSM families shift by a *different* amount each cycle,
  so x and y each need a barrel shifter: per output bit, a mux over the
  distinct source bits it can select (counted exactly from the shift set,
  including the sign-fill for arithmetic shift), built as a tree of 4:1
  LUT6 muxes. The atan LUT becomes a small ROM (one LUT per non-constant
  bit for <= 64 entries). Pipelined families shift by constants (wiring)
  and read constant LUT entries: zero mux LUTs.
* Rounding (``rounding="round"``) is folded into each adder's carry-in, so
  it is free for fixed shifts; variable shifters need one more mux output
  bit per shifter. Rounding the guard bits off at the output adds two W-bit
  adders.

``c_arith`` and ``c_mux`` absorb what the structure ignores (LUT
combining, logic sharing). They are solved *exactly* from the two anchors:
the pipelined anchor has no mux LUTs so it fixes ``c_arith``; the iterative
anchor then fixes ``c_mux``.

**FFs** = c_ff * register_bits, counted from the RTL structure (x, y, z,
counter, FSM, quadrant, valid chain, outputs, minus bits synthesis trims).
For the iterative anchor the raw count is exactly Vivado's 95; one scale
``c_ff`` is least-squares fitted over both anchors (relative error).

**Critical path** (ns) = t_ovh + levels * per-level delays + carry chains:

* ``t_ovh`` = clock-to-Q + clock overhead (skew, uncertainty, setup);
* carry chain for a B-bit adder: first CARRY4 + (ceil(B/4)-2) middle
  CARRY4s + the last CARRY4's sum output;
* ``t_logic``: one LUT level plus its input net (add/sub select etc.);
* ``t_mux``: one barrel-shifter mux level plus its (high-fanout) net.

Family paths:

* ``iterative``/``unrolled_k``: k chained micro-rotations per cycle, each
  ``n_mux * t_mux + t_logic + carry(B)`` with ``n_mux = ceil(log4(shifts))``
  for that stage's set of shift amounts.
* ``pipelined``/``pipelined_m``: m chained fixed-shift stages per register,
  each ``t_logic + carry(B)``, plus one output-side LUT level.

All primitive delays (clock-to-Q, CARRY4 delays, clock overhead) are read
straight off the two Vivado timing reports and *not fitted*.
``t_logic`` and ``t_mux`` are solved exactly from the two Fmax anchors
(pipelined has no mux levels, so it fixes ``t_logic``). The fitted values
come out physically sensible (0.88 ns and 1.13 ns per level), which is a
sanity check on the structure rather than proof of it.

**Power index**: (LUTs + FFs) * f_op * activity, normalised so the
reference iterative design at 100 MHz scores 1.0. It is a *relative*
ranking aid with no unit, never watts (see :mod:`hw_dse.evaluate`).

Everything numeric lives in ``calibration_artix7.yaml`` beside this file:
the anchors with their sources, the primitive delays read from the
reports, and the fitted constants. ``python -m hw_dse.models.cost_fpga``
re-runs the fit and prints it; ``tests/test_cost_model.py`` checks the
stored constants are what the fit produces and that the anchors are
reproduced.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from hw_dse.families import ArchConfig
from hw_dse.models.cordic_bitexact import atan_lut
from hw_dse.models.cost_base import CostEstimate

CALIBRATION_FILE = Path(__file__).with_name("calibration_artix7.yaml")


# ---------------------------------------------------------------------------
# Structural counts (no calibration constants in here)
# ---------------------------------------------------------------------------

def mux_tree_luts(n_inputs: int) -> int:
    """LUT6 count for an n:1 mux built from 4:1 mux LUTs (0 for n <= 1)."""
    if n_inputs <= 1:
        return 0
    total, level = 0, n_inputs
    while level > 1:
        level = math.ceil(level / 4)
        total += level
    return total


def mux_levels(n_inputs: int) -> int:
    """Logic levels of that mux tree: ceil(log4(n))."""
    return 0 if n_inputs <= 1 else math.ceil(math.log(n_inputs, 4) - 1e-9)


@lru_cache(maxsize=None)
def shifter_luts(width: int, shifts: tuple[int, ...]) -> int:
    """LUTs for one ``width``-bit arithmetic barrel shifter over ``shifts``.

    Output bit b of ``v >>> s`` is v[b+s] when b+s < width, else the sign
    bit v[width-1]. The mux for bit b only needs the *distinct* sources.
    """
    total = 0
    for b in range(width):
        sources = {min(b + s, width - 1) for s in shifts}
        total += mux_tree_luts(len(sources))
    return total


@lru_cache(maxsize=None)
def rom_luts(entries: tuple[int, ...]) -> int:
    """LUTs for a small constant ROM read by a counter: one LUT6 per
    non-constant output bit for <= 64 entries."""
    if len(set(entries)) <= 1:
        return 0
    bits = max(entries).bit_length()
    nonconst = sum(1 for b in range(bits) if len({(e >> b) & 1 for e in entries}) > 1)
    return nonconst * math.ceil(len(entries) / 64)


@dataclass(frozen=True)
class Structure:
    """Raw structural counts for one design (pre-calibration)."""

    arith_bits: int
    mux_luts: int
    reg_bits: int
    n_mux_levels: int  # mux levels per chained micro-rotation (FSM families)
    chain: int  # micro-rotations chained combinationally per cycle
    adder_bits: int  # widest carry chain in the datapath


def stage_shift_sets(arch: ArchConfig) -> list[tuple[int, ...]]:
    """For FSM families: the shift amounts each of the k stages must support."""
    n, k = arch.numerics.n_iter, arch.rotations_per_step
    return [tuple(range(j, n, k)) for j in range(k)]


def structure(arch: ArchConfig) -> Structure:
    num = arch.numerics
    w, n, g = num.data_width, num.n_iter, num.frac_guard
    wx, wz = num.xy_width, num.z_width
    rnd = num.rounding == "round"
    out_round_bits = 2 * w if (rnd and g > 0) else 0
    lut = atan_lut(n, num.A)
    rot_bits = 2 * wx + wz

    if not arch.is_pipelined:
        k, steps = arch.rotations_per_step, arch.steps
        cbits = max(1, math.ceil(math.log2(steps))) if steps > 1 else 1
        arith = k * rot_bits + (cbits + 6) + out_round_bits
        mux = 0
        n_mux = 0
        for shifts in stage_shift_sets(arch):
            per_shifter = shifter_luts(wx, shifts)
            if rnd:  # one extra output bit (the rounding bit) per shifter
                per_shifter += mux_tree_luts(len(shifts))
            mux += 2 * per_shifter
            mux += rom_luts(tuple(lut[i] for i in shifts))
            n_mux = max(n_mux, mux_levels(len(shifts)))
        # x, y, z state; counter; quadrant (2); FSM state (2); done (1); outputs.
        regs = rot_bits + cbits + 2 + 2 + 1 + 2 * w
        return Structure(arith, mux, regs, n_mux, k, max(wx, wz))

    m, stages = arch.rotations_per_step, arch.steps
    # Every micro-rotation has its own x/y/z add/subs, minus the two trims:
    # rotation 0 sees y = 0 (x/y adders collapse), the last z is unused.
    arith = n * rot_bits - 2 * wx - wz
    arith += 5  # pre-rotation: z +/- pi touches the top bits; x0 select
    arith += out_round_bits
    out_bits = w + (1 if (rnd and g > 0) else 0)
    regs = 2 + wz + 1  # stage 0: x0 in {0, +K, -K} (~2 FFs), z0, valid
    for r in range(1, stages + 1):
        last = r == stages
        if last:
            regs += 2 * out_bits + 1  # only the bits the output uses; z unused
        elif r == 1 and m == 1:
            regs += 2 + 2 + wz + 1  # after rotation 0: x1, y1 are +/-x0 (~constant)
        else:
            regs += 2 * wx + wz + 1
    regs += 2 * w + 1  # output registers + valid
    return Structure(arith, 0, regs, 0, m, max(wx, wz))


# ---------------------------------------------------------------------------
# Calibration data
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def load_calibration(path: str | None = None) -> dict[str, Any]:
    with open(path or CALIBRATION_FILE, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def carry_delay(bits: int, src: dict[str, float]) -> float:
    n4 = max(1, math.ceil(bits / 4))
    if n4 == 1:
        return src["t_carry_first_ns"]
    return src["t_carry_first_ns"] + (n4 - 2) * src["t_carry_mid_ns"] + src["t_carry_last_ns"]


def _path_terms(s: Structure, arch: ArchConfig, src: dict[str, float]) -> tuple[float, float, float]:
    """Critical path as (fixed_ns, n_logic_levels, n_mux_levels)."""
    t_ovh = src["t_clk2q_ns"] + src["t_clk_overhead_ns"]
    carry = carry_delay(s.adder_bits, src)
    if arch.is_pipelined:
        return t_ovh + s.chain * carry, s.chain + 1, 0.0
    return t_ovh + s.chain * carry, float(s.chain), float(s.chain * s.n_mux_levels)


def anchor_arch(anchor: dict[str, Any]) -> ArchConfig:
    return ArchConfig.from_params(anchor["family"], anchor["params"])


def calibrate(cal: dict[str, Any] | None = None) -> dict[str, float]:
    """Solve the free constants from the anchors. Returns the fitted dict.

    * c_arith from the pipelined anchor (no mux LUTs), then c_mux from the
      iterative anchor.
    * c_ff: least squares on relative error over both anchors.
    * t_logic from the pipelined Fmax (no mux levels), then t_mux from the
      iterative Fmax.
    """
    cal = cal or load_calibration()
    src = cal["source_constants"]
    by_family = {a["family"]: a for a in cal["anchors"]}
    pa, ia = by_family["pipelined"], by_family["iterative"]
    ps, is_ = structure(anchor_arch(pa)), structure(anchor_arch(ia))

    c_arith = pa["luts"] / ps.arith_bits
    c_mux = (ia["luts"] - c_arith * is_.arith_bits) / is_.mux_luts

    # minimise sum_i (c*r_i/t_i - 1)^2  ->  c = sum(r/t) / sum((r/t)^2)
    ratios = [ps.reg_bits / pa["ffs"], is_.reg_bits / ia["ffs"]]
    c_ff = sum(ratios) / sum(r * r for r in ratios)

    pf, pl, _ = _path_terms(ps, anchor_arch(pa), src)
    t_logic = (1000.0 / pa["fmax_mhz"] - pf) / pl
    if_, il, im = _path_terms(is_, anchor_arch(ia), src)
    t_mux = (1000.0 / ia["fmax_mhz"] - if_ - il * t_logic) / im
    return {"c_arith": c_arith, "c_mux": c_mux, "c_ff": c_ff, "t_logic_ns": t_logic, "t_mux_ns": t_mux}


# ---------------------------------------------------------------------------
# The cost model
# ---------------------------------------------------------------------------

class FpgaCostModel:
    """CostModel implementation for Artix-7-class FPGAs (LUT6 + CARRY4)."""

    name = "cost_fpga"
    target = "fpga"

    def __init__(self, calibration_path: str | None = None) -> None:
        self.cal = load_calibration(calibration_path)
        self.src: dict[str, float] = self.cal["source_constants"]
        self.fit: dict[str, float] = self.cal["fitted"]
        self.calibration_id: str = self.cal["id"]
        self.provenance = f"estimate: {self.name} ({self.calibration_id}, {len(self.cal['anchors'])} anchors)"
        ref = self.cal["power_reference"]
        ref_cost = self._raw(ArchConfig.from_params(ref["family"], ref["params"]))
        self.power_norm = (ref_cost[0] + ref_cost[1]) * ref["f_mhz"] * self.src["activity_factor"]

    def _raw(self, arch: ArchConfig) -> tuple[float, float, float, Structure]:
        s = structure(arch)
        luts = self.fit["c_arith"] * s.arith_bits + self.fit["c_mux"] * s.mux_luts
        ffs = self.fit["c_ff"] * s.reg_bits
        fixed, n_logic, n_mux = _path_terms(s, arch, self.src)
        path = fixed + n_logic * self.fit["t_logic_ns"] + n_mux * self.fit["t_mux_ns"]
        return luts, ffs, path, s

    def estimate(self, arch: ArchConfig) -> CostEstimate:
        luts, ffs, path, s = self._raw(arch)
        return CostEstimate(
            area={"luts": luts, "ffs": ffs},
            fmax_mhz=1000.0 / path,
            critical_path_ns=path,
            switching_resources=luts + ffs,
            activity_factor=self.src["activity_factor"],
            provenance=self.provenance,
            breakdown={
                "arith_bits": s.arith_bits,
                "mux_luts": s.mux_luts,
                "reg_bits": s.reg_bits,
                "chain": s.chain,
                "mux_levels_per_stage": s.n_mux_levels,
                "adder_bits": s.adder_bits,
            },
        )


def main() -> None:  # pragma: no cover - convenience CLI
    cal = load_calibration()
    fit = calibrate(cal)
    print("fitted constants (copy into calibration_artix7.yaml if they changed):")
    for k, v in fit.items():
        print(f"  {k}: {v:.6f}   (stored: {cal['fitted'].get(k)})")
    model = FpgaCostModel()
    print("\nanchor reproduction:")
    for a in cal["anchors"]:
        e = model.estimate(anchor_arch(a))
        print(
            f"  {a['family']:10s} LUT {e.area['luts']:7.1f} vs {a['luts']:4d}"
            f"  FF {e.area['ffs']:7.1f} vs {a['ffs']:4d}"
            f"  Fmax {e.fmax_mhz:6.1f} vs {a['fmax_mhz']}"
        )


if __name__ == "__main__":  # pragma: no cover
    main()
