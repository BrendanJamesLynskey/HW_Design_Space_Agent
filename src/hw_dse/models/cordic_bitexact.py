"""Bit-accurate golden model of circular-rotation CORDIC (sin/cos).

This module is the *source of truth for accuracy*. Every accuracy number the
project reports (max-abs error, RMS error, "accuracy bits") is computed here,
by running the exact integer arithmetic the hardware performs on a sweep of
input angles. Those numbers carry the provenance label ``exact``.

What "bit-accurate" means here
------------------------------
For the default configuration (``data_width=16, n_iter=14``) the model is
**bit-exact** against the reference RTL (``cordic_rotation_iterative.sv`` and
``cordic_rotation_pipelined.sv`` from the CORDIC repo): for every one of the
65,536 possible input angles it produces the same 16-bit ``COS_OUT`` and
``SIN_OUT`` codes as an Icarus simulation of the RTL. ``tests/test_bitexact_rtl.py``
proves this; see ``rtl_harness/`` for the testbench.

The reference datapath, step by step (W = DATA_WIDTH, N = NUM_ITERATIONS)::

    angle code  theta   : W-bit signed, full scale 2^(W-1) == pi
    registers   x, y, z : W+2 bits signed (2 bits of MSB headroom)
    LUT         atan[i] = round(atan(2^-i) / pi * 2^(W-1))
    gain        x0      = round(K_N * 2^(W-2)),  K_N = prod cos(atan 2^-i)

    1. quadrant pre-rotation, keyed on theta's top two bits:
         01 (pi/2..pi)   -> x0 = -x0, z0 = theta - pi
         10 (-pi..-pi/2) -> x0 = -x0, z0 = theta + pi
    2. for i in 0..N-1:          (sigma = +1 if z >= 0 else -1)
         x <- x - sigma * (y >>> i)
         y <- y + sigma * (x >>> i)
         z <- z - sigma * atan[i]
    3. COS_OUT = x[W-1:0], SIN_OUT = y[W-1:0]   (Q1.(W-2) format)

``>>>`` is an arithmetic right shift, i.e. *floor* division by 2^i: the bits
shifted out are simply dropped (truncation). All additions wrap modulo
2^(W+2), exactly like the Verilog registers do.

Generalisation (the design-space knobs)
---------------------------------------
The reference fixes several choices that a designer could make differently.
The model exposes them as parameters so the explorer can trade them off:

``data_width`` (W)
    Input angle width and output sin/cos width. Output format stays
    Q1.(W-2), so 1 output LSB = 2^-(W-2).
``n_iter`` (N)
    Number of micro-rotations. Too few -> residual angle error; more than
    about W+2 buys nothing because the shifted terms are all zero.
``angle_width`` (A)
    Width of the z datapath and the atan LUT entries (LUT quantum
    pi / 2^(A-1)). The reference uses A = W. A > W adds fractional angle
    bits (the input is left-aligned), A < W drops input LSBs.
``frac_guard`` (g)
    Extra *fractional* bits in x and y (the reference has 0: its 2 extra
    bits are MSB headroom, not precision). Each guard bit halves the
    truncation noise accumulated over N shifts; the result is reduced back
    to W bits at the output.
``rounding`` ("trunc" | "round")
    ``trunc`` is the reference behaviour (floor shifts, drop guard bits).
    ``round`` adds half an LSB before every shift and before the output
    reduction: round-half-up. In hardware this costs (almost) nothing for
    fixed shifts, because the rounding bit becomes the adder's carry-in.

With ``angle_width=W, frac_guard=0, rounding="trunc"`` the model reduces
exactly to the reference datapath, which is why the bit-exact test pins
those values.

Why NumPy, and why int64
------------------------
Accuracy is measured over an *exhaustive* sweep (all 2^W angles) for
W <= 16, so the model is vectorised: one NumPy array holds every angle and
each micro-rotation is a handful of whole-array integer operations. The
widest register in the supported space is W+2+g <= 40 bits, comfortably
inside int64, and NumPy's ``>>`` on signed integers is an arithmetic shift,
matching Verilog's ``>>>``.

Architecture families do not appear here
----------------------------------------
Iterative, unrolled, pipelined and partially pipelined CORDICs all perform
the *same sequence of integer operations*; they differ only in how many
operations happen per clock cycle. So accuracy depends on the numeric knobs
above and not on the family, which lets ``hw_dse.evaluate`` cache accuracy
per numeric configuration and share it across families.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

import numpy as np

Rounding = Literal["trunc", "round"]

HEADROOM_BITS = 2
"""MSB headroom on x, y and z, as in the reference (``[DATA_WIDTH+1:0]``)."""

EXHAUSTIVE_MAX_WIDTH = 16
"""Widths up to this are swept exhaustively (all 2^W input angles)."""

DENSE_STRIDED = 1 << 16
DENSE_RANDOM = 1 << 16
DENSE_SEED = 20260401
"""Above ``EXHAUSTIVE_MAX_WIDTH`` the sweep is *dense*, not exhaustive:
2^16 evenly strided angle codes (covering every quadrant boundary and the
full circle uniformly) plus 2^16 uniformly random codes from a fixed seed
(to hit low-order bit patterns the stride would miss). The resulting
max-abs error is exact *for those 131,072 angles*, and therefore a tight
lower bound on the true worst case rather than a proof of it."""


@dataclass(frozen=True)
class CordicNumerics:
    """The numeric (bit-level) configuration of a CORDIC datapath.

    Frozen and hashable so it can key the accuracy cache.
    """

    data_width: int = 16
    n_iter: int = 14
    angle_width: int | None = None  # None means "same as data_width" (reference)
    frac_guard: int = 0
    rounding: Rounding = "trunc"

    def __post_init__(self) -> None:
        if not 4 <= self.data_width <= 40:
            raise ValueError(f"data_width {self.data_width} outside 4..40")
        if not 1 <= self.n_iter <= 48:
            raise ValueError(f"n_iter {self.n_iter} outside 1..48")
        if self.frac_guard < 0 or self.frac_guard > 8:
            raise ValueError(f"frac_guard {self.frac_guard} outside 0..8")
        if self.rounding not in ("trunc", "round"):
            raise ValueError(f"rounding must be 'trunc' or 'round', got {self.rounding!r}")
        a = self.A
        if not 4 <= a <= 48:
            raise ValueError(f"angle_width {a} outside 4..48")

    # Short aliases used throughout the arithmetic below.
    @property
    def W(self) -> int:  # noqa: N802 - hardware-style names read better here
        return self.data_width

    @property
    def A(self) -> int:  # noqa: N802
        return self.data_width if self.angle_width is None else self.angle_width

    @property
    def xy_width(self) -> int:
        """Register width of x and y: W + 2 headroom + g fractional guard."""
        return self.data_width + HEADROOM_BITS + self.frac_guard

    @property
    def z_width(self) -> int:
        """Register width of the residual angle z: A + 2 headroom."""
        return self.A + HEADROOM_BITS

    @property
    def out_lsb(self) -> float:
        """Weight of one output LSB in absolute terms: 2^-(W-2)."""
        return 2.0 ** -(self.data_width - 2)


REFERENCE = CordicNumerics(data_width=16, n_iter=14)
"""The configuration of the reference RTL (bit-exact target)."""


# ---------------------------------------------------------------------------
# Constants: atan LUT and gain pre-compensation
# ---------------------------------------------------------------------------

def _round_half_up(v: float) -> int:
    # Python's round() is round-half-even; the reference values were
    # generated with ordinary rounding. No LUT entry here sits exactly on a
    # .5 boundary except trivially, but be explicit anyway.
    return int(math.floor(v + 0.5))


@lru_cache(maxsize=None)
def atan_lut(n_iter: int, angle_width: int) -> tuple[int, ...]:
    """atan(2^-i) for i in 0..n_iter-1, quantised to the angle format.

    Angle format: full scale 2^(A-1) == pi, so the code for angle phi is
    ``round(phi / pi * 2^(A-1))``. For A=16 this reproduces the reference
    table 8192, 4836, 2555, 1297, ..., 3, 1.
    """
    scale = float(1 << (angle_width - 1))
    return tuple(_round_half_up(math.atan(2.0**-i) / math.pi * scale) for i in range(n_iter))


def cordic_gain(n_iter: int) -> float:
    """K_N = prod_{i<N} cos(atan(2^-i)) = prod 1/sqrt(1 + 2^-2i)."""
    k = 1.0
    for i in range(n_iter):
        k /= math.sqrt(1.0 + 2.0 ** (-2 * i))
    return k


@lru_cache(maxsize=None)
def init_x(n_iter: int, frac_bits: int) -> int:
    """Gain pre-compensation constant: round(K_N * 2^frac_bits).

    With frac_bits = W-2 = 14 and N = 14 this is the reference's 9949.
    """
    return _round_half_up(cordic_gain(n_iter) * float(1 << frac_bits))


# ---------------------------------------------------------------------------
# Integer helpers
# ---------------------------------------------------------------------------

def wrap(v: np.ndarray, bits: int) -> np.ndarray:
    """Two's-complement wrap of int64 values to a ``bits``-wide register.

    This is what a Verilog assignment to a ``logic signed [bits-1:0]``
    register does with an over-wide expression: keep the low ``bits`` bits
    and reinterpret them as signed.
    """
    half = np.int64(1) << np.int64(bits - 1)
    mask = (np.int64(1) << np.int64(bits)) - np.int64(1)
    return ((v + half) & mask) - half


def _shift(v: np.ndarray, s: int, rounding: Rounding) -> np.ndarray:
    """Arithmetic right shift, optionally round-half-up instead of floor."""
    if s == 0:
        return v
    if rounding == "round":
        return (v + (np.int64(1) << np.int64(s - 1))) >> np.int64(s)
    return v >> np.int64(s)


# ---------------------------------------------------------------------------
# The datapath
# ---------------------------------------------------------------------------

def cordic_sincos(theta: np.ndarray, cfg: CordicNumerics = REFERENCE) -> tuple[np.ndarray, np.ndarray]:
    """Run the CORDIC datapath on a vector of input angle codes.

    Parameters
    ----------
    theta:
        Integer angle codes, each a W-bit signed value in
        [-2^(W-1), 2^(W-1)), full scale == pi.
    cfg:
        Numeric configuration.

    Returns
    -------
    (cos_code, sin_code):
        W-bit signed output codes in Q1.(W-2) format, exactly as the
        hardware's ``COS_OUT``/``SIN_OUT`` ports would present them.
    """
    W, A, g = cfg.W, cfg.A, cfg.frac_guard
    wx, wz = cfg.xy_width, cfg.z_width
    theta = np.asarray(theta, dtype=np.int64)
    if theta.size and (theta.min() < -(1 << (W - 1)) or theta.max() >= (1 << (W - 1))):
        raise ValueError("theta codes out of range for data_width")

    # -- Stage 0: align the input angle to the z format -----------------
    if A >= W:
        z = theta << np.int64(A - W)
    else:
        z = theta >> np.int64(W - A)  # dropped input LSBs (truncation)

    # Quadrant = the top two bits of the W-bit input code.
    quadrant = (theta >> np.int64(W - 2)) & np.int64(3)

    k = np.int64(init_x(cfg.n_iter, W - 2 + g))
    x = np.full(theta.shape, k, dtype=np.int64)
    y = np.zeros(theta.shape, dtype=np.int64)

    # -- Quadrant pre-rotation by +/- pi -----------------------------------
    pi_code = np.int64(1) << np.int64(A - 1)
    q2 = quadrant == 1  # (pi/2, pi): rotate by -pi
    q3 = quadrant == 2  # (-pi, -pi/2): rotate by +pi
    flip = q2 | q3
    x = np.where(flip, -x, x)
    z = np.where(q2, z - pi_code, np.where(q3, z + pi_code, z))
    x, z = wrap(x, wx), wrap(z, wz)

    # -- Micro-rotations ---------------------------------------------------
    lut = atan_lut(cfg.n_iter, A)
    for i in range(cfg.n_iter):
        pos = z >= 0
        sy = _shift(y, i, cfg.rounding)
        sx = _shift(x, i, cfg.rounding)
        a = np.int64(lut[i])
        x_new = np.where(pos, x - sy, x + sy)
        y_new = np.where(pos, y + sx, y - sx)
        z_new = np.where(pos, z - a, z + a)
        x, y, z = wrap(x_new, wx), wrap(y_new, wx), wrap(z_new, wz)

    # -- Output reduction: drop guard bits, keep the low W bits ------------
    x_out = _shift(x, g, cfg.rounding)
    y_out = _shift(y, g, cfg.rounding)
    return wrap(x_out, W), wrap(y_out, W)


# ---------------------------------------------------------------------------
# Accuracy metrics (provenance: exact)
# ---------------------------------------------------------------------------

def sweep_angles(data_width: int) -> tuple[np.ndarray, str]:
    """The angle set used for accuracy metrics, plus a description of it.

    Exhaustive for W <= 16, dense (strided + seeded random) above that.
    """
    lo, hi = -(1 << (data_width - 1)), 1 << (data_width - 1)
    if data_width <= EXHAUSTIVE_MAX_WIDTH:
        return np.arange(lo, hi, dtype=np.int64), f"exhaustive ({hi - lo} angles)"
    stride = (hi - lo) // DENSE_STRIDED
    strided = np.arange(lo, hi, stride, dtype=np.int64)
    rng = np.random.default_rng(DENSE_SEED + data_width)
    rand = rng.integers(lo, hi, size=DENSE_RANDOM, dtype=np.int64)
    codes = np.unique(np.concatenate([strided, rand]))
    return codes, f"dense ({codes.size} angles: {strided.size} strided + {DENSE_RANDOM} random, seed {DENSE_SEED}+W)"


@dataclass(frozen=True)
class Accuracy:
    """Error of the hardware outputs against ideal sin/cos.

    The ideal is the *unquantised* real value ``cos(theta) * 2^(W-2)``, so
    the error includes the unavoidable output quantisation (>= 0.5 LSB
    max) as well as CORDIC's truncation and residual-angle errors. Errors
    are taken over both outputs (cos and sin) jointly.
    """

    max_abs_lsb: float
    rms_lsb: float
    max_abs: float  # absolute, in units of the output (1.0 == full scale)
    rms: float
    accuracy_bits: float  # -log2(max_abs): "this many correct fractional bits"
    n_angles: int
    sweep: str

    def as_dict(self) -> dict[str, float | int | str]:
        return {
            "max_abs_err_lsb": self.max_abs_lsb,
            "rms_err_lsb": self.rms_lsb,
            "max_abs_err": self.max_abs,
            "rms_err": self.rms,
            "accuracy_bits": self.accuracy_bits,
            "n_angles": self.n_angles,
            "sweep": self.sweep,
        }


@lru_cache(maxsize=1 << 16)
def accuracy(cfg: CordicNumerics) -> Accuracy:
    """Exact accuracy metrics of ``cfg`` over the documented angle sweep.

    Cached: the same numeric configuration is shared by every architecture
    family, and the explorers revisit configurations often.
    """
    codes, sweep = sweep_angles(cfg.data_width)
    cos_c, sin_c = cordic_sincos(codes, cfg)
    phi = codes.astype(np.float64) * (math.pi / float(1 << (cfg.data_width - 1)))
    scale = float(1 << (cfg.data_width - 2))
    err = np.concatenate([cos_c - np.cos(phi) * scale, sin_c - np.sin(phi) * scale])
    max_lsb = float(np.max(np.abs(err)))
    rms_lsb = float(np.sqrt(np.mean(err * err)))
    max_abs = max_lsb * cfg.out_lsb
    return Accuracy(
        max_abs_lsb=max_lsb,
        rms_lsb=rms_lsb,
        max_abs=max_abs,
        rms=rms_lsb * cfg.out_lsb,
        accuracy_bits=-math.log2(max_abs) if max_abs > 0 else float("inf"),
        n_angles=int(codes.size),
        sweep=sweep,
    )
