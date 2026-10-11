"""Milestone 4: the exports for the local Vivado runs and the path that ingests them.

Vivado is not run here. The exports are checked for what they ask Vivado to
do; the collectors are run on the committed batch-2 reports (real Vivado
output, re-labelled as if synthesised at 20 ns, to exercise the parser and
the 1000 / (T - WNS) formula only) and on a power report written in Vivado's
``report_power`` layout (a format sample, not a measurement), with the
indented breakdown rows Vivado prints under Slice Logic, which must not be
counted twice.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import vivado_m4  # noqa: E402

from hw_dse.synth import measured, vivado_power  # noqa: E402

POWER_SAMPLE = """\
1. Summary
----------

+--------------------------+--------------+
| Total On-Chip Power (W)  | 0.0{tot}        |
| Design Power Budget (W)  | Unspecified* |
| Dynamic (W)              | 0.0{dyn}        |
| Device Static (W)        | 0.072        |
| Confidence Level         | Low          |
+--------------------------+--------------+

1.1 On-Chip Components
----------------------

+----------------+-----------+----------+-----------+-----------------+
| On-Chip        | Power (W) | Used     | Available | Utilization (%) |
+----------------+-----------+----------+-----------+-----------------+
| Clocks         |     0.{clk} |        3 |       --- |             --- |
| Slice Logic    |     0.{logic} |      300 |       --- |             --- |
|   LUT as Logic |     0.{logic} |      120 |     63400 |            0.19 |
|   Register     |    <0.001 |      180 |    126800 |            0.14 |
|   CARRY4       |    <0.001 |       30 |     15850 |            0.19 |
| Signals        |     0.{sig} |      500 |       --- |             --- |
| I/O            |     0.009 |       52 |       106 |           49.06 |
| Static Power   |     0.072 |          |           |                 |
| Total          |     0.0{tot} |          |           |                 |
+----------------+-----------+----------+-----------+-----------------+
"""


def test_exports_ask_for_the_right_runs(tmp_path: Path) -> None:
    vivado_m4.export(tmp_path / "a", vivado_m4.POINTS_20NS, 20.0, power=False)
    dirs = sorted(p for p in (tmp_path / "a").iterdir() if p.is_dir())
    assert [d.name for d in dirs] == ["cordic_pipelined_m_m6_w26_n22_ap0_g0_round", "cordic_pipelined_m_m8_w26_n22_ap0_g0_round"]
    for d in dirs:
        assert (d / "clock.xdc").read_text().startswith("create_clock -period 20.000")
        tcl = (d / "run.tcl").read_text()
        assert "synth_design" in tcl and "route_design" in tcl and "report_power" not in tcl
    pts = vivado_m4.power_points()
    assert len(pts) == 14
    vivado_m4.export(tmp_path / "p", pts, 10.0, power=True)
    tcl = (tmp_path / "p" / "cordic_iterative_w16_n14_ap0_g0_trunc" / "run.tcl").read_text()
    assert tcl.count("\nreport_power -file") == 4 and tcl.index("power_synth_10ns") < tcl.index("route_design")
    # the 1 ns clock is for the power report only; timing-driven implementation runs at 10 ns
    assert tcl.index("create_clock -period 10.000") < tcl.index("opt_design")
    assert (tmp_path / "p" / "run_all.sh").read_text().count("vivado -mode batch") == 14


def test_collect_20ns_uses_the_designs_own_period(tmp_path: Path) -> None:
    src = ROOT / "eval/data/vivado_logs_2/cordic_pipelined_m_m8_w26_n22_ap0_g0_round"
    dst = tmp_path / "logs" / src.name
    shutil.copytree(src, dst)
    (dst / "period_ns.txt").write_text("20\n")
    pts = vivado_m4.collect_20ns(tmp_path / "logs", tmp_path / "out.csv")
    wns = vivado_m4.vp.parse_wns((src / "timing.rpt").read_text())
    syn = next(p for p in pts if p.extra["fmax_kind"].startswith("post-synthesis"))
    assert syn.fmax_mhz == pytest.approx(round(1000 / (20 - wns), 2)) and syn.tool_version == vivado_m4.VERSION_20NS
    assert len(measured.load(tmp_path / "out.csv")) == 2


def test_power_report_parser_and_compare(tmp_path: Path) -> None:
    r = vivado_power.parse_report_power(POWER_SAMPLE.format(tot="93", dyn="21", clk="003", logic="004", sig="005"))
    assert r["dynamic_w"] == 0.021 and r["static_w"] == 0.072 and r["io_w"] == 0.009
    assert r["core_w"] == pytest.approx(0.012) and r["confidence"] == "Low"  # sub-rows not double-counted
    assert r["slice_logic_w"] == 0.004
    assert vivado_power._w("<0.001") == 0.0005
    logs = tmp_path / "logs"
    for i, key in enumerate([vivado_power.REFERENCE_KEY,
                             "pipelined:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc"]):
        d = logs / f"d{i}"
        d.mkdir(parents=True)
        (d / "design_key.txt").write_text(key + "\n")
        scale = 1 + 4 * i
        (d / "power_routed_1ns.rpt").write_text(POWER_SAMPLE.format(
            tot="93", dyn="21", clk=f"{30 * scale:03d}", logic=f"{40 * scale:03d}", sig=f"{50 * scale:03d}"))
    rows = vivado_m4.collect_power(logs, tmp_path / "power.csv")
    assert len(vivado_power.load(tmp_path / "power.csv")) == len(rows) == 2
    c = vivado_power.compare(rows, "post-route")
    ref = next(d for d in c["designs"] if d["key"] == vivado_power.REFERENCE_KEY)
    assert ref["power_index_100mhz"] == pytest.approx(1.0) and ref["measured_relative"] == 1.0
    assert ref["measured_core_mw_100mhz"] == pytest.approx(12.0)  # 0.120 W at 1 GHz -> 12 mW at 100 MHz
    assert c["n"] == 2 and c["rms_log_ratio_pct"] is not None


def test_compare_without_data_says_so(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(vivado_m4, "CSV_20NS", tmp_path / "none.csv")
    monkeypatch.setattr(vivado_m4, "CSV_POWER", tmp_path / "none2.csv")
    monkeypatch.setattr(vivado_m4, "COMPARE", tmp_path / "cmp")
    assert vivado_m4.compare() == {}
    assert "Neither" in (tmp_path / "cmp.md").read_text()


def test_power_parser_rounds_to_the_printed_precision(tmp_path: Path) -> None:
    """``core_w`` is a sum of printed values; it carries their precision, not binary float noise."""
    r = vivado_power.parse_report_power(POWER_SAMPLE.format(tot="93", dyn="21", clk="001", logic="001", sig="007"))
    assert repr(r["core_w"]) == "0.009"  # 0.001 + 0.001 + 0.007 = 0.009000000000000001 unrounded
    sample = POWER_SAMPLE.format(tot="93", dyn="21", clk="003", logic="001", sig="000").replace("|     0.000 |", "|    <0.001 |")
    # 0.003 + 0.001 + 0.0005 = 0.0045000000000000005 unrounded; "<0.001" counts 0.0005, so 4 places
    assert repr(vivado_power.parse_report_power(sample)["core_w"]) == "0.0045"
    # the committed CSV re-collects byte for byte from the committed reports, with no noisy digits
    out = tmp_path / "power.csv"
    vivado_m4.collect_power(ROOT / "eval/data/vivado_logs_m4_power", out)
    assert out.read_bytes() == (ROOT / "eval/data/vivado_power.csv").read_bytes()
    for row in vivado_power.load(out):
        assert len(row["core_w"].split(".")[-1]) <= 4


def test_power_activity_fit_is_a_separate_calibration() -> None:
    import yaml

    from hw_dse.evaluate import evaluate

    act = vivado_power.fit_activity(vivado_power.load(ROOT / "eval/data/vivado_power.csv"))
    assert act["parameters"] == 4 and act["n"] == 14
    r = act["rms_log_pct"]
    assert r["per_family_in"] <= r["per_family_loo"] and r["per_family_in"] < r["global_scale_in"]
    cal = yaml.safe_load((ROOT / "src/hw_dse/models/power_activity_artix7_vivado-2025.2-m4.yaml").read_text())
    assert cal["default"] is False and cal["mw_per_index_unit"] == act["mw_per_index_unit"]
    # the default power index is unchanged: the reference design is 1.0 at 100 MHz
    ref = evaluate(vivado_power.ArchConfig.from_key(vivado_power.REFERENCE_KEY))
    assert ref["power_index"] * 100.0 / ref["f_op_mhz"] == pytest.approx(1.0)


def test_post_route_ratios_cover_every_design_measured_both_ways() -> None:
    pr = vivado_m4.post_route_ratios()
    assert len(pr["designs"]) == 16 and set(pr["by_family"]) == {"iterative", "pipelined", "pipelined_m", "unrolled_k"}
    m6 = next(d for d in pr["designs"] if d["key"].endswith("m=6") and d["period_ns"] == 20.0)
    assert (m6["synth_mhz"], m6["route_mhz"]) == (65.39, 53.96)
    assert pr["by_family"]["pipelined"]["max"] < 0.75 < pr["by_family"]["unrolled_k"]["min"]
