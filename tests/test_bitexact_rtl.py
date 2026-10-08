"""Golden model vs reference RTL: bit-exact on every 16-bit input angle.

Skips cleanly when Icarus Verilog or the reference RTL is unavailable
(run ``scripts/fetch_reference_rtl.sh`` and install ``iverilog``). CI
installs both, so this runs on every push.
"""

from __future__ import annotations

import os

import numpy as np
import pytest

from hw_dse.models import rtl_reference
from hw_dse.models.cordic_bitexact import REFERENCE, cordic_sincos

available, reason = rtl_reference.rtl_available()
# CI sets HW_DSE_REQUIRE_RTL=1 so a missing simulator fails loudly instead
# of silently skipping the one test that ties the model to the hardware.
if os.environ.get("HW_DSE_REQUIRE_RTL") == "1" and not available:
    raise RuntimeError(f"HW_DSE_REQUIRE_RTL=1 but RTL simulation unavailable: {reason}")
pytestmark = pytest.mark.skipif(not available, reason=reason)

ALL_ANGLES = np.arange(-(1 << 15), 1 << 15, dtype=np.int64)


@pytest.mark.parametrize("dut", ["iterative", "pipelined"])
def test_model_matches_rtl_exhaustively(dut: str) -> None:
    theta, cos_rtl, sin_rtl = rtl_reference.simulate(ALL_ANGLES, dut)
    # The harness must have reported every angle, in order.
    assert np.array_equal(theta, ALL_ANGLES)
    cos_py, sin_py = cordic_sincos(theta, REFERENCE)
    bad = np.flatnonzero((cos_py != cos_rtl) | (sin_py != sin_rtl))
    assert bad.size == 0, (
        f"{bad.size} mismatches, first at theta={theta[bad[0]]}: "
        f"rtl=({cos_rtl[bad[0]]},{sin_rtl[bad[0]]}) model=({cos_py[bad[0]]},{sin_py[bad[0]]})"
    )
