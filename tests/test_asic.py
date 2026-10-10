"""Milestone 4: the ASIC target (sky130_fd_sc_hd, Yosys + OpenSTA).

Tool-free: the liberty filter, ``stat -liberty`` and OpenSTA log parsing on
recorded output, the committed CSV's schema, the calibration (stored
constants = what the fit produces from the committed CSV), the target in the
spec, and that an FPGA record is unchanged. With the tools
(``HW_DSE_REQUIRE_ASIC=1`` in CI): a one-design smoke synthesis and a
re-measurement of committed rows, which must match exactly (Yosys/ABC and
OpenSTA are deterministic).
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest
import yaml

from hw_dse.evaluate import cost_model_for, evaluate
from hw_dse.families import ArchConfig
from hw_dse.models import cost_asic
from hw_dse.spec import Spec
from hw_dse.synth import asic
from tests.tooling import tool_mark

DATA = Path(__file__).with_name("data")
TOOLS = asic.AsicTools.from_env()
needs_asic = tool_mark("HW_DSE_REQUIRE_ASIC", *TOOLS.available())


def _spec(**kw: object) -> Spec:
    base = {"name": "t", "target": "asic-sky130hd",
            "constraints": [{"metric": "throughput_msps", "op": ">=", "value": 5}],
            "objectives": [{"metric": "area_um2", "direction": "min", "ref": 200000},
                           {"metric": "accuracy_bits", "direction": "max", "ref": 6}],
            "select_by": "area_um2"}
    return Spec.model_validate({**base, **kw})


def test_strip_cells_removes_only_the_named_cell_groups() -> None:
    lib = ('library (x) {\n  cell ("a_lpflow_iso_1") {\n    area : 1;\n    pin (A) { dir : input; }\n  }\n'
           '  cell ("b_nand2_1") {\n    area : 3.75;\n  }\n  cell ("c_probe_p_8") { area : 2; }\n}\n')
    out, dropped = asic.strip_cells(lib)
    assert dropped == ["a_lpflow_iso_1", "c_probe_p_8"]
    assert "b_nand2_1" in out and "lpflow" not in out and "probe" not in out and out.count("{") == out.count("}")


def test_parse_recorded_tool_output() -> None:
    area, cells = asic.parse_stat_liberty((DATA / "asic_stat_iterative_w8.txt").read_text())
    assert area == pytest.approx(3688.5376) and cells["sky130_fd_sc_hd__dfxtp_1"] == 56
    assert sum(v for k, v in cells.items() if asic.FF_CELL.search(k)) == 56
    r = asic.parse_sta((DATA / "asic_sta_iterative_w8.log").read_text())
    assert r["slack_ns"] == pytest.approx(5.4613) and r["arrival_ns"] == pytest.approx(4.3134)
    assert r["power_mw"] == pytest.approx(0.3413677)
    assert r["power_internal_mw"] + r["power_switching_mw"] + r["power_leakage_mw"] == pytest.approx(r["power_mw"])


def test_committed_csv_is_complete_and_consistent() -> None:
    pts = asic.load_csv()
    assert len(pts) == 57 and {p.arch.family for p in pts} == {"iterative", "unrolled_k", "pipelined", "pipelined_m"}
    for p in pts:
        assert p.row["library"] == "sky130_fd_sc_hd" and p.row["corner"] == "tt_025C_1v80"
        assert p.gate_eq == pytest.approx(p.area_um2 / asic.NAND2_AREA_UM2, abs=0.01)
        assert p.fmax_mhz == pytest.approx(1000 / p.critical_path_ns, rel=1e-4)
        assert "yosys 0.33" in p.row["tool_version"] and "OpenSTA" in p.row["tool_version"]
        assert p.row["source_log"].startswith("eval/data/asic_logs/") and "/home/" not in p.row["command"]
        assert p.provenance.startswith("measured (yosys+opensta")


def test_stored_calibration_is_what_the_fit_produces() -> None:
    rep = cost_asic.calibrate()
    stored = yaml.safe_load(cost_asic.CALIBRATION_FILE.read_text())
    assert stored["fitted"] == rep["calibration"]["fitted"]
    assert stored["residuals_rms_pct"] == rep["calibration"]["residuals_rms_pct"]
    loo = stored["residuals_rms_pct"]["leave_one_out"]
    # The headline numbers the README quotes.
    assert loo["area_um2"] < 10 and loo["fmax_mhz"] < 12 and loo["ffs"] < 6


def test_asic_model_power_reference_and_provenance() -> None:
    cm = cost_asic.AsicCostModel()
    ref = ArchConfig.from_params("iterative", {"data_width": 16, "n_iter": 14})
    e = cm.estimate(ref)
    assert e.switching_resources * 100.0 * e.activity_factor / cm.power_norm == pytest.approx(1.0)
    assert e.area["gate_eq"] == pytest.approx(e.area["area_um2"] / 3.7536)
    assert e.provenance.startswith("estimate: cost_asic (sky130hd-")


def test_spec_target_selects_the_cost_model_and_guards_metrics() -> None:
    s = _spec()
    assert s.target_kind == "asic" and cost_model_for(s).target == "asic"
    rec = evaluate(ArchConfig.from_params("pipelined", {"data_width": 12, "n_iter": 10}), s)
    assert rec["area_um2"] > 0 and rec["gate_eq"] > 0 and math.isnan(rec["luts"]) and rec["feasible"]
    assert rec["provenance"]["area_um2"].startswith("estimate: cost_asic")
    with pytest.raises(ValueError, match="fpga target"):
        _spec(select_by="luts", objectives=[{"metric": "luts", "direction": "min", "ref": 1e4},
                                            {"metric": "accuracy_bits", "direction": "max", "ref": 6}])
    with pytest.raises(ValueError, match="asic target"):
        Spec.model_validate({"name": "f", "objectives": [{"metric": "area_um2", "direction": "min", "ref": 1}],
                             "select_by": "area_um2"})


def test_fpga_records_have_no_asic_fields() -> None:
    spec = Spec.model_validate({"name": "f", "objectives": [{"metric": "luts", "direction": "min", "ref": 1e4}],
                                "select_by": "luts"})
    rec = evaluate(ArchConfig.from_params("iterative", {"data_width": 16, "n_iter": 14}), spec)
    assert "area_um2" not in rec and "gate_eq" not in rec and rec["luts"] == pytest.approx(170.0, abs=0.1)


def test_asic_architect_prompt_and_fpga_prompt_are_separate() -> None:
    from hw_dse.agent import prompts

    assert "area_um2" not in prompts.SYSTEM and "Artix-7" in prompts.SYSTEM
    a = prompts.system_prompt(_spec())
    assert "sky130" in a and "area_um2" in a and "- luts:" not in a and "Artix-7" not in a


@needs_asic
def test_asic_smoke_synthesis(tmp_path: Path) -> None:
    a = ArchConfig.from_params("iterative", {"data_width": 8, "n_iter": 6})
    r = asic.synthesize_arch(a, root=tmp_path)
    assert r.area_um2 > 1000 and r.ffs > 40 and r.fmax_mhz and r.power["power_mw"] > 0


@needs_asic
def test_committed_rows_remeasure_identically(tmp_path: Path) -> None:
    """Yosys/ABC and OpenSTA are deterministic: the committed numbers are reproducible."""
    pts = [p for p in asic.load_csv() if p.arch.numerics.data_width <= 12][:2]
    for p in pts:
        r = asic.synthesize_arch(p.arch, root=tmp_path)
        assert round(r.area_um2, 4) == p.area_um2 and r.ffs == p.ffs
        assert round(r.critical_path_ns or 0, 4) == p.critical_path_ns
        assert round(r.power["power_mw"], 6) == p.power_mw


def test_asic_back_annotation_uses_sky130_measurements_and_flags_the_multiaxis_winner() -> None:
    """The ASIC model's asic_multiaxis_control optimum measures 72.2 MHz (model 82.5): with
    measured numbers it misses the 0.5 us batch deadline, so back-annotation flags it, and
    never compares an ASIC design against FPGA measurements."""
    import json

    from hw_dse.agent.backannotate import back_annotate
    from hw_dse.spec import load_spec

    spec = load_spec("specs/asic/asic_multiaxis_control.yaml")
    gt = json.loads(Path("eval/data/ground_truth_m4.json").read_text())[spec.name]
    sel = evaluate(ArchConfig.from_key(gt["selected"]["key"]), spec)
    ba = back_annotate(spec, [sel], sel)
    assert ba["target"] == "asic" and ba["status"] == "compared" and ba["reexplore_available"] is False
    assert all("luts" not in c for c in ba["comparisons"])
    assert ba["comparisons"][0]["fmax_mhz"]["diff_pct"] < -10
    assert ba["winner_changed"] and "sys_p99_batch_us" in ba["why"]
