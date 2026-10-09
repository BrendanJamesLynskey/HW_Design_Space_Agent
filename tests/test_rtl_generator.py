"""L3: the RTL generator, its golden examples and its verification.

Tool-free tests (always run): golden-example drift, module naming and the
documented latency. Simulator tests skip without Verilator/Icarus locally and
are mandatory in CI (``HW_DSE_REQUIRE_SIM=1``); see ``tests/tooling.py``.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

from hw_dse.families import ArchConfig
from hw_dse.models import rtl_reference
from hw_dse.models.cordic_bitexact import REFERENCE, cordic_sincos
from hw_dse.rtl import sweep
from hw_dse.rtl.generator import GOLDEN_DIR, GOLDEN_EXAMPLES, generate, module_name
from hw_dse.rtl.sim import compare, simulate, tool_status, verify_rtl
from tests.tooling import full_sweep_requested, tool_mark

VERILATOR, ICARUS = tool_status("verilator"), tool_status("icarus")
BOTH = (VERILATOR[0] and ICARUS[0], "; ".join(r for ok, r in (VERILATOR, ICARUS) if not ok))
needs_sims = tool_mark("HW_DSE_REQUIRE_SIM", *BOTH)
needs_icarus = tool_mark("HW_DSE_REQUIRE_SIM", *ICARUS)


# ---------------------------------------------------------------------------
# Tool-free
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("family", list(GOLDEN_EXAMPLES))
def test_golden_examples_do_not_drift(family: str) -> None:
    """The committed examples are exactly what the generator emits today.

    If this fails after an intentional generator change, regenerate with
    ``python -m hw_dse.rtl.generator`` and review the diff.
    """
    committed = (GOLDEN_DIR / f"cordic_golden_{family}.sv").read_text()
    assert generate(GOLDEN_EXAMPLES[family], module=f"cordic_golden_{family}").text == committed


def test_module_names_are_unique_and_latency_documented() -> None:
    cfgs = sweep.sweep_configs()
    names = [module_name(a) for a in cfgs]
    assert len(set(names)) == len(names)
    for a in cfgs:
        d = generate(a)
        assert d.latency == a.latency_cycles
        assert f"localparam int LATENCY = {a.latency_cycles};" in d.text
        assert d.initiation_interval == (1 if a.is_pipelined else a.latency_cycles)


def test_constants_come_from_the_golden_model() -> None:
    """The atan LUT and gain in the RTL are the golden model's functions' values."""
    from hw_dse.models.cordic_bitexact import atan_lut, init_x

    a = ArchConfig.from_params("pipelined", {"data_width": 12, "n_iter": 9, "angle_guard": 3, "frac_guard": 2})
    text = generate(a).text
    assert f"{list(atan_lut(9, 15))}" in text
    assert f"16'h{init_x(9, 12):04x}" in text  # WX = 12 + 2 + 2 = 16
    for v in atan_lut(9, 15)[1:-1]:  # the last rotation's z has no consumer, so no adder
        assert f"17'h{v:05x}" in text  # WZ = 15 + 2


# ---------------------------------------------------------------------------
# Simulation (Verilator + Icarus)
# ---------------------------------------------------------------------------

@needs_sims
@pytest.mark.parametrize("arch", sweep.QUICK, ids=lambda a: a.family)
@pytest.mark.parametrize("simulator", ["verilator", "icarus"])
def test_quick_l3_sweep(arch: ArchConfig, simulator: str) -> None:
    v = verify_rtl(arch, simulator)
    assert v.n_angles == 256 and v.sweep.startswith("exhaustive")
    assert v.passed, v


@needs_icarus
@pytest.mark.parametrize("family", ["iterative", "pipelined"])
def test_generated_rtl_is_bit_identical_to_reference_rtl(family: str, tmp_path: Path) -> None:
    """At the reference default (W=16, N=14) generated == vendored reference, all 65,536 angles."""
    angles = np.arange(-(1 << 15), 1 << 15, dtype=np.int64)
    _, cos_ref, sin_ref = rtl_reference.simulate(angles, family)
    arch = ArchConfig.from_params(family, {"data_width": 16, "n_iter": 14})
    assert arch.numerics == REFERENCE
    d = generate(arch)
    sim = "verilator" if VERILATOR[0] else "icarus"
    res = simulate([d.write(tmp_path)], d.module, 16, angles, sim)
    assert np.array_equal(res.theta, angles)
    assert np.array_equal(res.cos, cos_ref) and np.array_equal(res.sin, sin_ref)
    # ...and therefore also equal to the golden model (transitively; checked directly too).
    assert compare(arch, res, angles, "exhaustive", sim).passed
    cos_m, sin_m = cordic_sincos(angles, REFERENCE)
    assert np.array_equal(cos_m, cos_ref)


@pytest.mark.skipif(shutil.which("verilator") is None, reason="verilator not on PATH")
@pytest.mark.parametrize("family", list(GOLDEN_EXAMPLES))
def test_golden_examples_are_lint_clean(family: str) -> None:
    p = subprocess.run(["verilator", "--lint-only", "-Wall", str(GOLDEN_DIR / f"cordic_golden_{family}.sv")],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


@needs_sims
@pytest.mark.skipif(not full_sweep_requested(), reason="full L3 sweep: set HW_DSE_L3_FULL=1 (CI does)")
def test_full_l3_sweep() -> None:
    rows = sweep.run(sweep.sweep_configs(), log=False)
    failed = [r.key + "@" + r.simulator for r in rows if not r.passed]
    assert len(rows) == 2 * len(sweep.sweep_configs())
    assert not failed, failed


def test_committed_l3_table_is_all_green() -> None:
    """The committed table records zero mismatches and correct latency everywhere."""
    rows = sweep.read_csv()
    assert rows, "eval/data/l3_verification.csv missing"
    rtl = [r for r in rows if r["level"] == "rtl"]
    assert {r["simulator"] for r in rtl} == {"verilator", "icarus"}
    assert {r["family"] for r in rtl} == set(sweep.FAMILIES)
    assert all(r["passed"] == "True" and r["mismatches"] == "0" for r in rows)
