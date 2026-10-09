"""L5: measured-points schema, the per-tool refit, and the back-annotation hook.

All offline, on recorded data: the committed L4 sweep
(``eval/data/l4_synthesis.csv``) and a small hand-made Vivado-style CSV.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from hw_dse.agent.backannotate import back_annotate
from hw_dse.evaluate import evaluate
from hw_dse.families import ArchConfig
from hw_dse.models.cost_fpga import FpgaCostModel, load_calibration
from hw_dse.spec import load_spec
from hw_dse.synth import measured, recalibrate
from hw_dse.synth.sweep import L4_CSV, VIVADO_POINTS

ROOT = Path(__file__).resolve().parents[1]


def _vivado_csv(path: Path, rows: list[dict[str, object]]) -> Path:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(measured.COLUMNS))
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in measured.COLUMNS})
    return path


def _row(arch: ArchConfig, luts: float, ffs: float, fmax: float | None, tool: str = "vivado",
         kind: str | None = None) -> dict[str, object]:
    """A measured row; Vivado rows default to post-synthesis (the anchors' flow), others to post-route."""
    p = arch.params()
    kind = kind or ("post-synthesis (1000/(10-WNS))" if tool == "vivado" else "post-route")
    return {"tool": tool, "tool_version": "2025.2", "part": "xc7a35tcpg236-1", "rtl_source": "generated",
            "family": arch.family, "data_width": p["data_width"], "n_iter": p["n_iter"], "angle_guard": p["angle_guard"],
            "frac_guard": p["frac_guard"], "rounding": p["rounding"], "k": arch.k, "m": arch.m, "luts": luts, "ffs": ffs,
            "fmax_mhz": "" if fmax is None else fmax, "fmax_kind": kind, "source_log": "test"}


def test_committed_l4_csv_follows_the_schema() -> None:
    pts = measured.load(L4_CSV)
    assert len(pts) >= 30
    assert {p.arch.family for p in pts} == {"iterative", "unrolled_k", "pipelined", "pipelined_m"}
    keys = {p.arch.key() for p in pts if p.rtl_source == "generated"}
    assert all(a.key() in keys for a in VIVADO_POINTS)  # the six points the Vivado PR will re-run
    assert {p.rtl_source for p in pts} == {"generated", "reference"}
    for p in pts:
        assert p.provenance.startswith("measured (yosys")
        assert p.extra["command"] and p.extra["source_log"]
        assert (ROOT / p.extra["source_log"]).exists()


def test_schema_rejects_bad_rows(tmp_path: Path) -> None:
    a = ArchConfig.from_params("pipelined", {"data_width": 16, "n_iter": 14})
    bad = _row(a, 700, 700, 250)
    bad["family"] = "systolic"
    p = _vivado_csv(tmp_path / "bad.csv", [bad, {**_row(a, -1, 5, 250)}, {**_row(a, 700, 700, 250), "rtl_source": "x"}])
    with pytest.raises(measured.SchemaError) as e:
        measured.load(p)
    msg = str(e.value)
    assert "unknown family" in msg and "non-physical" in msg and "rtl_source" in msg
    extra = tmp_path / "extra.csv"
    extra.write_text(",".join(measured.COLUMNS) + ",bogus\n")
    with pytest.raises(measured.SchemaError):
        measured.load(extra)


def test_fit_recovers_known_constants_and_tool_factor() -> None:
    """Synthetic data generated from known constants and a known tool factor is fitted back."""
    base = load_calibration()
    truth = FpgaCostModel()
    pts = recalibrate.anchor_points(base)
    for fam, extra in (("iterative", {}), ("unrolled_k", {"k": 3}), ("pipelined", {}), ("pipelined_m", {"m": 3})):
        for w, n in ((10, 9), (14, 12), (18, 16), (22, 20), (26, 24)):
            a = ArchConfig.from_params(fam, {"data_width": w, "n_iter": n, **extra})
            e = truth.estimate(a)
            pts.append(measured.MeasuredPoint("toolx", "1", "p", "generated", a, 1.3 * e.area["luts"], 0.9 * e.area["ffs"],
                                              e.fmax_mhz / 1.2))
    f = recalibrate.fit(pts, base)
    assert f.tau["toolx"]["luts"] == pytest.approx(1.3, rel=1e-3)
    assert f.tau["toolx"]["ffs"] == pytest.approx(0.9, rel=1e-3)
    assert f.tau["toolx"]["path"] == pytest.approx(1.2, rel=1e-3)
    for k in ("c_arith", "c_ff", "t_logic_ns"):
        assert f.constants[k] == pytest.approx(base["fitted"][k], rel=1e-3)


def test_refit_on_recorded_l4_data_and_a_vivado_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The one-command Vivado path: schema -> refit -> new named calibration + residual report."""
    viv = _vivado_csv(tmp_path / "vivado.csv", [_row(VIVADO_POINTS[0], 230, 100, 120.0),
                                                _row(VIVADO_POINTS[2], 650, 420, 180.0)])
    cal_dir = tmp_path / "models"
    cal_dir.mkdir()
    base = cal_dir / "calibration_artix7.yaml"
    base.write_text((ROOT / "src/hw_dse/models/calibration_artix7.yaml").read_text())
    monkeypatch.setattr(recalibrate, "REPO_ROOT", tmp_path)
    rep = recalibrate.refit([L4_CSV, viv], "testfit", base_path=base, impact=False)
    out = cal_dir / "calibration_artix7_refit_testfit.yaml"
    assert out.exists() and base.read_text() == (ROOT / "src/hw_dse/models/calibration_artix7.yaml").read_text()
    cal = load_calibration(str(out))
    assert cal["id"].endswith("testfit") and cal["tool_corrections"]["vivado"]["luts"] == 1.0
    assert set(cal["tool_corrections"]) == {"vivado", "yosys+nextpnr-xilinx"}
    # residuals reported before and after at every point, for both tools
    assert len(rep["residuals_before"]) == len(rep["residuals_after"]) == 2 + len(measured.load(L4_CSV)) + 2
    after = rep["summary_after"]
    assert any(k.startswith("vivado") for k in after) and any(k.startswith("yosys") for k in after)
    # the refit model loads and estimates with the new provenance
    m = FpgaCostModel(str(out))
    assert "measured points" in m.provenance and m.estimate(VIVADO_POINTS[1]).fmax_mhz > 0
    md = recalibrate.markdown(rep)
    assert "Residuals at every measured point" in md


def _front(spec_name: str, keys: list[ArchConfig]) -> list[dict[str, object]]:
    s = load_spec(ROOT / "specs" / f"{spec_name}.yaml")
    return [evaluate(a, s) for a in keys]


def test_back_annotation_compares_and_flags_winner_change(tmp_path: Path) -> None:
    spec = load_spec(ROOT / "specs" / "low_area_control.yaml")
    sel_arch = ArchConfig.from_params("iterative", {"data_width": 16, "n_iter": 14})
    other = ArchConfig.from_params("iterative", {"data_width": 15, "n_iter": 12, "angle_guard": 1, "rounding": "round"})
    front = _front("low_area_control", [other, sel_arch])
    selected = front[1]
    # Recorded measurements: the selected design measures much larger than the other one.
    csvp = _vivado_csv(tmp_path / "m.csv", [_row(sel_arch, 400, 150, 150.0), _row(other, 160, 90, 150.0)])
    ba = back_annotate(spec, front, selected, {"measured_csvs": [csvp], "calibration": None})
    assert ba["status"] == "compared" and ba["winner_changed"]
    assert ba["comparisons"][0]["luts"]["measured"] == 400
    assert "prefers" in ba["why"] and other.key() in ba["why"]
    # No data for the selected design -> says so, flags nothing.
    ba2 = back_annotate(spec, front, front[0], {"measured_csvs": [tmp_path / "missing.csv"]})
    assert ba2["status"] == "no_measured_data" and not ba2["winner_changed"]


def test_back_annotation_infeasible_under_measurement(tmp_path: Path) -> None:
    spec = load_spec(ROOT / "specs" / "dds_250msps.yaml")
    a = ArchConfig.from_params("pipelined", {"data_width": 18, "n_iter": 15, "angle_guard": 1, "rounding": "round"})
    front = _front("dds_250msps", [a])
    csvp = _vivado_csv(tmp_path / "m.csv", [_row(a, 900, 900, 200.0)])  # 200 MHz < 250 MSPS
    ba = back_annotate(spec, front, front[0], {"measured_csvs": [csvp], "calibration": None})
    assert ba["winner_changed"] and "violates" in ba["why"] and "throughput" in ba["why"]


def test_back_annotate_node_runs_in_the_graph(tmp_path: Path) -> None:
    from hw_dse.agent.llm import ScriptedLLM
    from hw_dse.agent.runner import run_agent
    from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange
    from hw_dse.spec import Budget

    spec = load_spec(ROOT / "specs" / "low_area_control.yaml").model_copy(
        update={"budget": Budget(total_evals=30, evals_per_round=30, max_rounds=1, hv_epsilon=0.0)})
    plan = ExplorationPlan(families=[FamilyPlan(family="iterative", why="t", ranges=[
        ParamRange(param="data_width", low=16, high=16), ParamRange(param="n_iter", low=14, high=14),
        ParamRange(param="angle_guard", low=0, high=0), ParamRange(param="frac_guard", low=0, high=0),
        ParamRange(param="rounding", choices=["trunc"])])], rationale="t")
    from hw_dse.agent.graph import LEVERS_M1

    res = run_agent(spec, llm=ScriptedLLM([plan, AnalysisDecision(decision="stop", rationale="t")]), run_root=tmp_path,
                    levers=LEVERS_M1)
    assert res["selected"]["key"] == "iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc"
    report = (Path(res["run_dir"]) / "report.md").read_text()
    assert "L5 back-annotation" in report and "measured (yosys" in report


def test_vivado_points_export_and_collect(tmp_path: Path) -> None:
    """The Vivado PR path, offline: export the 8 designs, fake Vivado's reports from
    excerpts of the anchors' real reports, collect into a schema-valid CSV."""
    import importlib.util

    spec_ = importlib.util.spec_from_file_location("vivado_points", ROOT / "scripts" / "vivado_points.py")
    vp = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(vp)  # type: ignore[union-attr]
    data = ROOT / "tests" / "data" / "vivado"
    util = (data / "utilization_excerpt.rpt").read_text()
    timing = (data / "timing_excerpt.rpt").read_text()
    assert vp.parse_utilization(util) == {"luts": 745, "ffs": 784, "carry4": 201}
    assert vp.parse_wns(timing) == 6.336
    vp.export(tmp_path / "vp", route=False)
    dirs = [d for d in (tmp_path / "vp").iterdir() if d.is_dir()]
    assert len(dirs) == 8 and (tmp_path / "vp" / "run_all.sh").exists()
    tcl = (dirs[0] / "run.tcl").read_text()
    assert "synth_design -top" in tcl and "xc7a35tcpg236-1" in tcl and "route_design" not in tcl
    for d in dirs:  # pretend Vivado ran
        (d / "utilization.rpt").write_text(util)
        (d / "timing.rpt").write_text(timing)
    out = tmp_path / "vivado.csv"
    vp.collect(tmp_path / "vp", out, "2025.2")
    pts = measured.load(out)
    assert len(pts) == 8 and all(p.tool == "vivado" and p.fmax_mhz == round(1000 / (10 - 6.336), 2) for p in pts)


def test_each_tool_carries_equal_weight_and_generated_vivado_rows_replace_anchors(tmp_path: Path,
                                                                                   monkeypatch: pytest.MonkeyPatch) -> None:
    pts = measured.load(L4_CSV)
    w = recalibrate.tool_weights(recalibrate.anchor_points(load_calibration()) + pts)
    n_v = 2
    assert sum(w[:n_v]) == pytest.approx(sum(w[n_v:]))  # 2 Vivado points weigh as much as all Yosys points
    viv = _vivado_csv(tmp_path / "v.csv", [_row(ArchConfig.from_params("pipelined", {"data_width": 16, "n_iter": 14}),
                                               720, 751, 327.4)])
    cal_dir = tmp_path / "models"
    cal_dir.mkdir()
    base = cal_dir / "calibration_artix7.yaml"
    base.write_text((ROOT / "src/hw_dse/models/calibration_artix7.yaml").read_text())
    monkeypatch.setattr(recalibrate, "REPO_ROOT", tmp_path)
    rep = recalibrate.refit([L4_CSV, viv], "t", base_path=base, impact=False)
    assert rep["anchors_used"] == ["iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc"]
    viv_rows = [r for r in rep["residuals_after"] if r["tool"] == "vivado"]
    assert all(abs(r["luts_err_pct"]) < 10 for r in viv_rows)  # the reference tool stays on its own scale
    assert rep["loo_summary"]["all"]["n"] == 38 and "leave-one-out" in recalibrate.markdown(rep)
    # per-family overrides never touch the shared shifter constants
    assert all(set(d) <= set(recalibrate.PER_FAMILY_CONSTANTS) for d in rep["per_family"].values())


def test_back_annotation_scaled_diff_and_per_tool_winner_check(tmp_path: Path) -> None:
    spec = load_spec(ROOT / "specs" / "low_area_control.yaml")
    sel_arch = ArchConfig.from_params("iterative", {"data_width": 16, "n_iter": 14})
    other = ArchConfig.from_params("iterative", {"data_width": 15, "n_iter": 12, "angle_guard": 1, "rounding": "round"})
    front = _front("low_area_control", [other, sel_arch])
    # Vivado says the selected design is best; the open-source tool says the other one is.
    csvp = _vivado_csv(tmp_path / "m.csv", [
        _row(sel_arch, 150, 90, 200.0), _row(other, 170, 95, 200.0),
        _row(sel_arch, 400, 150, 150.0, tool="yosys+nextpnr-xilinx"), _row(other, 160, 90, 150.0, tool="yosys+nextpnr-xilinx")])
    cal = tmp_path / "cal.yaml"
    cal.write_text("tool_corrections:\n  yosys+nextpnr-xilinx: {luts: 2.0, ffs: 1.0, path: 1.5}\n")
    ba = back_annotate(spec, front, front[1], {"measured_csvs": [csvp], "calibration": str(cal)})
    assert [c["tool"] for c in ba["winner_checks"]] == ["vivado", "yosys+nextpnr-xilinx"]
    assert ba["winner_changed"] is False and ba["why"].startswith("vivado:")  # reference tool decides the headline
    assert ba["winner_checks"][1]["winner_changed"] is True and any("disagree" in n for n in ba["notes"])
    ys = next(c for c in ba["comparisons"] if c["tool"].startswith("yosys"))
    assert ys["luts"]["measured_scaled"] == 200.0  # 400 / LUT factor 2.0
    assert ys["fmax_mhz"]["measured_scaled"] == 225.0  # 150 * path factor 1.5
    assert ys["luts"]["diff_pct"] != ys["luts"]["diff_pct_scaled"]


def test_post_route_vivado_rows_are_reported_not_fitted_and_duplicates_count_once(tmp_path: Path,
                                                                                    monkeypatch: pytest.MonkeyPatch) -> None:
    pipe = ArchConfig.from_params("pipelined", {"data_width": 16, "n_iter": 14})
    it = ArchConfig.from_params("iterative", {"data_width": 16, "n_iter": 14})
    full = _vivado_csv(tmp_path / "full.csv", [_row(pipe, 720, 751, 327.4), _row(pipe, 706, 751, 232.2, kind="post-route"),
                                               _row(it, 175, 96, 172.8), _row(it, 164, 96, 158.1, kind="post-route")])
    spot = _vivado_csv(tmp_path / "spot.csv", [_row(pipe, 720, 751, 327.4)])
    fit_rows, report_only, dropped = recalibrate.split_rows([full, L4_CSV, spot])
    viv = [p for p in fit_rows if p.tool == "vivado"]
    assert sorted(p.arch.family for p in viv) == ["iterative", "pipelined"]  # spot-check counted once
    assert dropped == [{"tool": "vivado", "key": pipe.key(), "csv": "spot.csv", "kept_from": "full.csv"}]
    assert {p.tool for p in report_only} == {"vivado post-route"} and len(report_only) == 2
    cal_dir = tmp_path / "models"
    cal_dir.mkdir()
    base = cal_dir / "calibration_artix7.yaml"
    base.write_text((ROOT / "src/hw_dse/models/calibration_artix7.yaml").read_text())
    monkeypatch.setattr(recalibrate, "REPO_ROOT", tmp_path)
    rep = recalibrate.refit([full, L4_CSV, spot], "t", base_path=base, impact=False)
    assert rep["anchors_used"] == []  # both reference anchors superseded by generated-RTL Vivado rows
    assert rep["n_fit_points"] == 2 + sum(p.rtl_source == "generated" for p in measured.load(L4_CSV))
    assert "vivado post-route (generated RTL)" in rep["summary_after"]
    assert "vivado (reference RTL)" in rep["summary_after"]  # still reported
    md = recalibrate.markdown(rep)
    assert "Reported, not fitted: 2 Vivado post-route rows" in md and "Counted once" in md


def test_ground_truth_re_evaluates_with_the_grids_cost_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """The front and the selected design must carry the refit model's numbers, not the default's."""
    from hw_dse import benchmark

    designs = [ArchConfig.from_params("iterative", {"data_width": w, "n_iter": n}) for w, n in ((12, 10), (14, 12), (16, 14))]
    monkeypatch.setattr(benchmark, "all_designs", lambda: designs)
    refit_cm = FpgaCostModel(str(ROOT / "src/hw_dse/models/calibration_artix7_refit_vivado-2025.2.yaml"))
    spec = load_spec(ROOT / "specs" / "low_area_control.yaml")
    gt = benchmark.ground_truth(benchmark.build_grid(cost_model=refit_cm), spec, refit_cm)
    sel = ArchConfig.from_key(gt["selected"]["key"])
    assert gt["selected"]["luts"] == pytest.approx(refit_cm.estimate(sel).area["luts"])
    assert gt["selected"]["luts"] != pytest.approx(FpgaCostModel().estimate(sel).area["luts"])


def test_committed_vivado_measurements_and_refit() -> None:
    pts = measured.load(ROOT / "eval/data/vivado_measured.csv")
    synth = [p for p in pts if not recalibrate.is_post_route(p)]
    keys = {p.arch.key() for p in synth}
    assert len(pts) == 16 and len(synth) == 8 and len(keys) == 8
    assert {a.key() for a in VIVADO_POINTS} < keys
    assert all(p.tool == "vivado" and p.rtl_source == "generated" and p.fmax_mhz for p in pts)
    for p in pts:  # every row's reports are committed
        for f in p.extra["source_log"].split(", "):
            assert (ROOT / "eval/data/vivado_logs" / f).exists()
    spot = measured.load(ROOT / "eval/data/vivado_spotcheck.csv")[0]
    same = next(p for p in synth if p.arch.key() == spot.arch.key())
    assert (same.luts, same.ffs) == (spot.luts, spot.ffs) and same.fmax_mhz == pytest.approx(spot.fmax_mhz, abs=0.05)
    cal = load_calibration(str(ROOT / "src/hw_dse/models/calibration_artix7_refit_vivado-2025.2.yaml"))
    assert cal["tool_corrections"]["vivado"] == {"luts": 1.0, "ffs": 1.0, "path": 1.0}
    assert cal["refit"]["points_by_tool"] == {"vivado": 8, "yosys+nextpnr-xilinx": 37}
    assert (ROOT / "eval/data/l5_refit_vivado-2025.2.md").exists()  # not truncated at the version's dot
    assert load_calibration()["id"] == "artix7-xc7a35t-vivado2025.2-2anchor-v1"  # the default is untouched
