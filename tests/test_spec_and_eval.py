"""Specs, the evaluator's provenance, search plumbing and run scoring."""

from __future__ import annotations

import glob

import numpy as np
import pytest

from hw_dse.accuracy_table import DEFAULT_PATH, load
from hw_dse.benchmark import score_run, select_design
from hw_dse.evaluate import evaluate
from hw_dse.explore import box_size, enumerate_box, run_family_study, run_union_study
from hw_dse.families import ArchConfig
from hw_dse.models.cordic_bitexact import CordicNumerics, _accuracy
from hw_dse.spec import Spec, load_spec, parse_number, try_parse_spec_text

SPECS = sorted(glob.glob("specs/*.yaml"))
REF = dict(data_width=16, n_iter=14, angle_guard=0, frac_guard=0, rounding="trunc")


def test_parse_number() -> None:
    assert parse_number("2^-13") == 2.0**-13
    assert parse_number("2**10") == 1024.0
    assert parse_number(250) == 250.0


@pytest.mark.parametrize("path", SPECS)
def test_example_specs_validate(path: str) -> None:
    s = load_spec(path)
    assert s.objectives and s.constraints


def test_at_least_one_infeasible_example() -> None:
    assert any("infeasible" in p for p in SPECS)


def test_yaml_text_detection() -> None:
    text = open(SPECS[0]).read()
    assert isinstance(try_parse_spec_text(text), Spec)
    assert try_parse_spec_text("I need a fast sine generator") is None


def test_evaluate_provenance_and_feasibility() -> None:
    spec = load_spec("specs/low_area_control.yaml")
    rec = evaluate(ArchConfig.from_params("iterative", REF), spec)
    assert rec["provenance"]["luts"].startswith("estimate:")
    assert rec["provenance"]["max_abs_err"].startswith("exact:")
    assert rec["provenance"]["latency_cycles"] == "exact: schedule"
    assert rec["luts"] == pytest.approx(170, abs=0.1)
    # Reference max error is 10.5 LSB of 2^-14 ~ 2^-10.6 < 2^-10: feasible.
    assert rec["feasible"] is True
    dds = evaluate(ArchConfig.from_params("iterative", REF), load_spec("specs/dds_250msps.yaml"))
    assert dds["feasible"] is False


def test_power_index_reference_is_one() -> None:
    rec = evaluate(ArchConfig.from_params("iterative", REF))  # no spec: runs at Fmax
    assert rec["power_index"] == pytest.approx(rec["fmax_mhz"] / 100.0, rel=1e-6)


def test_family_study_respects_box() -> None:
    spec = load_spec("specs/dds_250msps.yaml")
    box = {"data_width": (10, 12), "n_iter": (8, 10), "angle_guard": (0, 1), "frac_guard": (0, 0),
           "rounding": ("trunc",), "m": (2, 3)}
    recs = run_family_study("pipelined_m", box, spec, n_trials=20, seed=1)
    assert len(recs) == 20
    for r in recs:
        assert r["family"] == "pipelined_m" and 10 <= r["data_width"] <= 12 and r["m"] in (2, 3)
    assert box_size("pipelined_m", box) == len(list(enumerate_box("pipelined_m", box))) == 3 * 3 * 2 * 1 * 1 * 2


def test_union_study_is_seeded() -> None:
    spec = load_spec("specs/low_area_control.yaml")
    a = [r["key"] for r in run_union_study(spec, 12, seed=3, sampler="random")]
    b = [r["key"] for r in run_union_study(spec, 12, seed=3, sampler="random")]
    assert a == b


def test_score_run_hand_case() -> None:
    spec = load_spec("specs/low_area_control.yaml")
    recs = [evaluate(ArchConfig.from_params("iterative", {**REF, "n_iter": n}), spec) for n in (14, 4, 16)]
    gt = {"feasible": True, "hv_true": 1e9}
    sc = score_run(recs, spec, gt)
    assert sc["n_evals"] == 3 and sc["evals_to_95"] is None and sc["selected_meets_spec"]
    assert select_design(recs, spec)["key"] == sc["selected_key"]
    sc_inf = score_run([r for r in recs if not r["feasible"]], spec, {"feasible": False, "hv_true": 0.0})
    assert sc_inf["declared_infeasible"] and sc_inf["infeasibility_correct"]


@pytest.mark.skipif(not DEFAULT_PATH.exists(), reason="accuracy table not built")
def test_accuracy_table_matches_model_spot_checks() -> None:
    table = load()
    assert len(table) == 21 * 27 * 7 * 5 * 2
    rng = np.random.default_rng(0)
    keys = list(table)
    for i in rng.choice(len(keys), size=6, replace=False):
        cfg: CordicNumerics = keys[int(i)]
        if cfg.data_width > 16:
            continue  # keep the test fast; exhaustive widths are checked
        assert table[cfg].max_abs_lsb == _accuracy(cfg).max_abs_lsb
        assert table[cfg].rms_lsb == pytest.approx(_accuracy(cfg).rms_lsb, rel=1e-12)
