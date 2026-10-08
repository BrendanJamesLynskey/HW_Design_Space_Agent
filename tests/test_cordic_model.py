"""Unit tests of the bit-accurate model that need no simulator."""

from __future__ import annotations

import math

import numpy as np
import pytest

from hw_dse.models.cordic_bitexact import (
    REFERENCE,
    CordicNumerics,
    accuracy,
    atan_lut,
    cordic_sincos,
    init_x,
    sweep_angles,
    wrap,
)


def test_constants_match_reference_rtl() -> None:
    # The literal tables from cordic_rotation_iterative.sv.
    assert atan_lut(14, 16) == (8192, 4836, 2555, 1297, 651, 326, 163, 81, 41, 20, 10, 5, 3, 1)
    assert init_x(14, 14) == 9949


def test_wrap_is_twos_complement() -> None:
    v = np.array([0, 127, 128, 255, 256, -129, -128], dtype=np.int64)
    assert wrap(v, 8).tolist() == [0, 127, -128, -1, 0, 127, -128]


def test_known_angles() -> None:
    # 0, +pi/2, -pi/2, pi/4 in the 16-bit angle format (2^15 == pi).
    th = np.array([0, 1 << 14, -(1 << 14), 1 << 13], dtype=np.int64)
    c, s = cordic_sincos(th, REFERENCE)
    one = 1 << 14
    exp_c = [one, 0, 0, one * math.cos(math.pi / 4)]
    exp_s = [0, one, -one, one * math.sin(math.pi / 4)]
    assert np.all(np.abs(c - np.array(exp_c)) <= 11)
    assert np.all(np.abs(s - np.array(exp_s)) <= 11)


def test_sweep_is_exhaustive_up_to_16_bits_and_dense_above() -> None:
    codes, desc = sweep_angles(12)
    assert codes.size == 4096 and "exhaustive" in desc
    codes, desc = sweep_angles(20)
    assert codes.size > 100_000 and "dense" in desc
    assert codes.min() >= -(1 << 19) and codes.max() < (1 << 19)


def test_reference_accuracy_is_stable() -> None:
    # Pinned so a model change that alters numerics is caught here, not in
    # an eval table. Error is dominated by truncation in the x/y shifts,
    # dominates for the reference (no fractional guard bits on x/y).
    acc = accuracy(REFERENCE)
    assert acc.n_angles == 65536
    assert acc.max_abs_lsb == pytest.approx(10.5355, abs=1e-3)
    assert acc.rms_lsb == pytest.approx(2.2585, abs=1e-3)


def test_guard_bits_and_rounding_improve_accuracy() -> None:
    # Two error sources compete: x/y shift truncation (fixed by fractional
    # guard bits) and atan-LUT quantisation (fixed by a wider angle path).
    # Fixing only one leaves the other dominant; fixing both pays off.
    base = accuracy(CordicNumerics(16, 16))
    guarded = accuracy(CordicNumerics(16, 16, frac_guard=3))
    wide_angle = accuracy(CordicNumerics(16, 16, angle_width=20, frac_guard=3))
    better_both = accuracy(CordicNumerics(16, 16, angle_width=20, frac_guard=3, rounding="round"))
    assert guarded.max_abs_lsb < base.max_abs_lsb
    assert wide_angle.max_abs_lsb < guarded.max_abs_lsb / 2
    assert better_both.max_abs_lsb < wide_angle.max_abs_lsb
    # Output quantisation alone costs up to 0.5 LSB; a well-configured
    # datapath should get close to it.
    assert better_both.max_abs_lsb < 2.0


def test_too_few_iterations_is_inaccurate() -> None:
    assert accuracy(CordicNumerics(12, 4)).max_abs_lsb > accuracy(CordicNumerics(12, 12)).max_abs_lsb * 4


def test_invalid_config_rejected() -> None:
    with pytest.raises(ValueError):
        CordicNumerics(data_width=2)
    with pytest.raises(ValueError):
        CordicNumerics(rounding="nearest")  # type: ignore[arg-type]
