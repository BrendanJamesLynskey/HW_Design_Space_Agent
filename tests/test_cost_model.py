"""Cost-model calibration: the anchors are reproduced and the fit is stable."""

from __future__ import annotations

import pytest

from hw_dse.families import ArchConfig
from hw_dse.models.cost_base import CostModel
from hw_dse.models.cost_fpga import (
    FpgaCostModel,
    anchor_arch,
    calibrate,
    load_calibration,
    mux_tree_luts,
    shifter_luts,
    structure,
)

CAL = load_calibration()
MODEL = FpgaCostModel()


def test_stored_constants_are_what_the_fit_produces() -> None:
    fit = calibrate(CAL)
    for k, v in fit.items():
        assert CAL["fitted"][k] == pytest.approx(v, abs=5e-6), k


@pytest.mark.parametrize("anchor", CAL["anchors"], ids=lambda a: a["family"])
def test_anchor_points_reproduced(anchor: dict) -> None:
    est = MODEL.estimate(anchor_arch(anchor))
    # LUTs and Fmax have as many free constants as anchors: exact.
    assert est.area["luts"] == pytest.approx(anchor["luts"], abs=0.05)
    assert est.fmax_mhz == pytest.approx(anchor["fmax_mhz"], abs=0.05)
    # FFs: one least-squares scale over two anchors; residual < 1%.
    assert est.area["ffs"] == pytest.approx(anchor["ffs"], rel=0.01)


def test_iterative_register_count_is_structurally_exact() -> None:
    # Vivado reports 95 registers (86 FDRE + 9 FDSE); the raw structural
    # count must agree before any scaling.
    ia = next(a for a in CAL["anchors"] if a["family"] == "iterative")
    assert structure(anchor_arch(ia)).reg_bits == 95


def test_fitted_delays_are_physically_plausible() -> None:
    # A LUT level plus its net on Artix-7 -1 is ~0.5-1.5 ns.
    assert 0.5 < CAL["fitted"]["t_logic_ns"] < 1.5
    assert 0.5 < CAL["fitted"]["t_mux_ns"] < 1.5
    assert 0.5 < CAL["fitted"]["c_mux"] <= 1.2
    assert 0.9 < CAL["fitted"]["c_arith"] < 1.2


def test_protocol_and_provenance() -> None:
    assert isinstance(MODEL, CostModel)
    est = MODEL.estimate(anchor_arch(CAL["anchors"][0]))
    assert est.provenance.startswith("estimate:")
    assert "2 anchors" in est.provenance


def test_mux_helpers() -> None:
    assert [mux_tree_luts(n) for n in (1, 2, 4, 5, 16, 17)] == [0, 1, 1, 3, 5, 8]
    # Shift-by-0 only: pure wiring.
    assert shifter_luts(18, (0,)) == 0


def _params(**kw: object) -> dict:
    base = dict(data_width=16, n_iter=14, angle_guard=0, frac_guard=0, rounding="trunc")
    base.update(kw)
    return base


def test_monotonic_trends() -> None:
    e = lambda fam, **kw: MODEL.estimate(ArchConfig.from_params(fam, _params(**kw)))  # noqa: E731
    # Wider datapaths cost more and clock no faster.
    assert e("pipelined", data_width=24).area["luts"] > e("pipelined").area["luts"]
    assert e("pipelined", data_width=24).fmax_mhz <= e("pipelined").fmax_mhz
    # More pipeline registers: more FFs and a faster clock.
    assert e("pipelined").area["ffs"] > e("pipelined_m", m=2).area["ffs"]
    assert e("pipelined").fmax_mhz > e("pipelined_m", m=2).fmax_mhz
    # Unrolling adds datapath copies and lengthens the cycle.
    assert e("unrolled_k", k=2).area["luts"] > e("iterative").area["luts"]
    assert e("unrolled_k", k=2).fmax_mhz < e("iterative").fmax_mhz
