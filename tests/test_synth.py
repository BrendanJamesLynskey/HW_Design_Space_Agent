"""L4 synthesis flow and gate-level simulation.

Tool-free: Yosys ``stat`` and nextpnr log parsing (on recorded output), the
pin constraints. With tools: a Yosys-only smoke synthesis
(``HW_DSE_REQUIRE_SYNTH=1`` in CI) and a W=8 gate-level simulation of the
mapped netlist against the golden model (``HW_DSE_REQUIRE_GATE=1``).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from hw_dse.families import ArchConfig
from hw_dse.rtl.sim import tool_status
from hw_dse.synth import flow
from hw_dse.synth.gatesim import verify_gate
from tests.tooling import tool_mark

DATA = Path(__file__).with_name("data")
RUNNER = flow.Runner.from_env()
needs_yosys = tool_mark("HW_DSE_REQUIRE_SYNTH", *RUNNER.available(pnr=False))
_ic = tool_status("icarus")
_y = RUNNER.available(pnr=False)
needs_gate = tool_mark("HW_DSE_REQUIRE_GATE", _ic[0] and _y[0], "; ".join(r for ok, r in (_ic, _y) if not ok))


def test_parse_yosys_stat() -> None:
    cells = flow.parse_stat((DATA / "yosys_stat_iterative_w8.txt").read_text())
    assert cells["CARRY4"] == 14 and cells["FDRE"] == 52 and cells["FDSE"] == 4 and cells["LUT5"] == 42
    luts = sum(v for k, v in cells.items() if flow.LUT_CELLS.match(k))
    assert luts == 13 + 11 + 7 + 17 + 42 + 12  # INV counts as a LUT1
    assert sum(v for k, v in cells.items() if flow.FF_CELLS.match(k)) == 56
    # the older Yosys layout ("<cell> <count>") parses too
    assert flow.parse_stat("     LUT4    17\n     FDRE  3\n") == {"LUT4": 17, "FDRE": 3}


def test_parse_nextpnr_log_takes_the_post_route_figure() -> None:
    fmax, util = flow.parse_pnr_log((DATA / "nextpnr_log_excerpt.txt").read_text())
    lines = [ln for ln in (DATA / "nextpnr_log_excerpt.txt").read_text().splitlines() if "Max frequency" in ln]
    assert len(lines) >= 2 and fmax == float(lines[-1].split(":")[-1].split("MHz")[0])
    assert util["CARRY4"] == 14


def test_pin_constraints_cover_every_port_bit() -> None:
    for w in (8, 16, 28):
        xdc = flow.xdc_for(w)
        assert xdc.count("set_property LOC") == 1 + len(flow.port_bits(w))
        assert "LOC W5 [get_ports clk]" in xdc and "create_clock -period 10.000" in xdc
    with pytest.raises(ValueError):
        flow.xdc_for(40)
    bits, clk = flow.reference_port_bits("cordic_rotation_pipelined", 16)
    assert clk == "CLK" and len(bits) == 4 + 48


@needs_yosys
def test_yosys_smoke_synthesis(tmp_path: Path) -> None:
    a = ArchConfig.from_params("pipelined", {"data_width": 8, "n_iter": 6})
    r = flow.synthesize_arch(a, pnr=False, root=tmp_path)
    assert r.luts > 50 and r.ffs > 50 and r.carry4 > 0 and r.fmax_mhz is None
    assert (Path(r.workdir) / f"{r.top}_netlist.v").exists()


@needs_gate
@pytest.mark.parametrize("family,extra", [("iterative", {}), ("pipelined_m", {"m": 3, "rounding": "round", "frac_guard": 1})])
def test_gate_level_w8_matches_golden_model(family: str, extra: dict[str, object], tmp_path: Path) -> None:
    a = ArchConfig.from_params(family, {"data_width": 8, "n_iter": 7, **extra})
    v = verify_gate(a, "icarus", root=tmp_path)
    assert v.level == "gate" and v.n_angles == 256 and v.passed, v
    assert "cells_sim.v" in v.netlist
