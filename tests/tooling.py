"""Skip-or-fail policy for tests that need external EDA tools.

Locally, a missing simulator / solver / synthesis tool skips its tests
cleanly, so ``pytest`` stays fast and offline. CI installs the tools and sets
one environment variable per class of tool, turning a skip into a hard
failure so a broken install can never pass silently:

=========================  ===================================================
``HW_DSE_REQUIRE_RTL=1``   Icarus (reference RTL vs golden model; M1)
``HW_DSE_REQUIRE_SIM=1``   Verilator *and* Icarus (L3 generated RTL)
``HW_DSE_REQUIRE_FORMAL=1`` SymbiYosys + Yosys + a solver (formal checks)
``HW_DSE_REQUIRE_GATE=1``  Yosys + Icarus (gate-level simulation)
=========================  ===================================================

``HW_DSE_L3_FULL=1`` additionally runs the full L3 sweep (minutes, CI only).
"""

from __future__ import annotations

import os

import pytest


def tool_mark(env_var: str, available: bool, reason: str) -> pytest.MarkDecorator:
    """A skipif marker, or an immediate error when ``env_var`` demands the tool."""
    if os.environ.get(env_var) == "1" and not available:
        raise RuntimeError(f"{env_var}=1 but the required tools are unavailable: {reason}")
    return pytest.mark.skipif(not available, reason=reason)


def full_sweep_requested() -> bool:
    return os.environ.get("HW_DSE_L3_FULL") == "1"
