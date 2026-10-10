"""M1/M2 comparability: today's graph replays the committed M2 runs exactly.

Given the same architect outputs (the recorded LLM decisions), a spec with no
system scenario must produce the same decisions, the same evaluations (every
design key, in order) and the same scores as in M2. This is what lets the M3
A/B reuse the M2 live runs on the four M2 specs.

A sample runs every time (one run per model, chosen to cover the blind-spot
seed, a front-mapping run, an infeasible spec and a run whose selection the
recorded L4 data flags at L5, which exercises the new L5 loop). All 60 runs
replay when ``HW_DSE_REPLAY_FULL=1`` (CI).
"""

from __future__ import annotations

import os

import pytest

from hw_dse.agent.replay import compare, m2_runs, replay_run

RUNS = m2_runs()
SAMPLE = {
    ("qwen/qwen3.8-27b", "high_precision", 1),        # the M2 blind-spot run (+71.7% regret)
    ("deepseek/deepseek-v4.1-flash", "dds_250msps", 0),  # map_front x3
    ("anthropic/claude-sonnet-5.5", "infeasible_dds_400msps", 0),
    ("anthropic/claude-sonnet-5.5", "low_area_control", 0),
}


def _id(r: dict) -> str:
    return f"{r['model_requested'].split('/')[-1]}-{r['spec']}-s{r['seed']}"


def test_all_60_m2_runs_are_committed() -> None:
    assert len(RUNS) == 60


@pytest.mark.parametrize("row", [r for r in RUNS if (r["model_requested"], r["spec"], r["seed"]) in SAMPLE
                                 or os.environ.get("HW_DSE_REPLAY_FULL") == "1"], ids=_id)
def test_replay_reproduces_the_m2_run(row: dict) -> None:
    out = compare(row, replay_run(row))
    assert out["identical"], out["checks"]
    # No system scenario: L2 only attaches facts (and is not reached when nothing was selected).
    assert out["l2_status"] == ("facts_only" if row["selected_key"] else None)


def test_a_replay_that_triggers_the_l5_loop_still_matches() -> None:
    """Find a recorded run whose selection the committed L4 data flags (the
    dds_250msps optimum measures 4.4% short of 250 MSPS in nextpnr): the L5 loop
    re-explores, but the run's L1 evaluations and selection stay as recorded."""
    flagged = [r for r in RUNS if r["spec"] == "dds_250msps" and r["select_regret"] == 0.0]
    if not flagged:
        pytest.skip("no recorded M2 run selected the dds_250msps optimum")
    row = flagged[0]
    rep = replay_run(row)
    out = compare(row, rep)
    assert out["identical"], out["checks"]
    assert out["back_annotation_winner_changed"] and out["l5_status"] == "reexplored"
    l5 = rep["res"]["l5"]
    assert l5["n_evals"] == 60 and l5["calibration"].startswith("artix7")
    assert len(rep["res"]["evaluations_ordered"]) == row["n_evals"]  # L5 evaluations kept apart


# ---------------------------------------------------------------------------
# Milestone 4: the FPGA path is untouched (M3 replays, ground truth, calibration)
# ---------------------------------------------------------------------------
# M4 adds an ASIC target that changes evaluate(), the architect's prompts, the
# summaries and the grid. None of it may move an FPGA number. Proven three ways:
# the M3 structured runs replay exactly (as the M2 ones above), the committed
# ground truth re-evaluates to the same records, and the default calibration
# file is byte-identical to the one M1-M3 used.

import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402

from hw_dse.agent.replay import DATA, m3_runs  # noqa: E402

M3_RUNS = m3_runs()
M3_SAMPLE = {("qwen/qwen3.8-27b", "multiaxis_control", 0), ("anthropic/claude-sonnet-5.5", "bursty_offload", 1)}
CALIBRATION_SHA256 = "f743d1f95eb86cb772766ebdba56728b03716958d02f2ecaa0c20ec2fd5d9b3c"  # M1 two-anchor model


def test_all_30_m3_structured_runs_are_committed() -> None:
    assert len(M3_RUNS) == 30


@pytest.mark.parametrize("row", [r for r in M3_RUNS if (r["model_requested"], r["spec"], r["seed"]) in M3_SAMPLE
                                 or os.environ.get("HW_DSE_REPLAY_FULL") == "1"], ids=_id)
def test_replay_reproduces_the_m3_structured_run(row: dict) -> None:
    out = compare(row, replay_run(row))
    assert out["identical"], out["checks"]
    assert out["checks"]["l2_winner_changed"] and out["checks"]["l1_selected_key"]


def test_default_fpga_calibration_is_byte_identical() -> None:
    from hw_dse.models.cost_fpga import CALIBRATION_FILE

    assert hashlib.sha256(CALIBRATION_FILE.read_bytes()).hexdigest() == CALIBRATION_SHA256


def _same(a: object, b: object) -> bool:
    if isinstance(a, float) and isinstance(b, float):
        return a == b or (math.isnan(a) and math.isnan(b)) or (math.isinf(a) and a == b)
    return a == b


@pytest.mark.parametrize("gt_file", ["ground_truth.json", "ground_truth_m3.json"])
def test_committed_fpga_ground_truth_reevaluates_identically(gt_file: str) -> None:
    """Every committed front design and selection of the M1-M3 ground truth, re-evaluated
    by today's code with each spec's default (target) cost model, gives the same numbers
    and the same hypervolume."""
    from hw_dse import accuracy_table
    from hw_dse.campaign.tools import spec_path
    from hw_dse.evaluate import evaluate, objective_vector, reference_point
    from hw_dse.families import ArchConfig
    from hw_dse.l2.node import simulate_record
    from hw_dse.pareto import hypervolume
    from hw_dse.spec import load_spec

    accuracy_table.preload()
    gts = json.loads((DATA / gt_file).read_text())
    for name, gt in gts.items():
        spec = load_spec(spec_path(name))
        assert spec.target == "fpga-artix7"
        recs = []
        for slim in gt["front"] + ([gt["selected"]] if gt["selected"] else []):
            r = evaluate(ArchConfig.from_key(slim["key"]), spec)
            if spec.system is not None:
                r = simulate_record(r, spec)
            for k, v in slim.items():
                assert _same(r[k], v), (name, slim["key"], k, r[k], v)
            recs.append(r)
        if gt["front"]:
            hv = hypervolume([objective_vector(r, spec) for r in recs[: len(gt["front"])]], reference_point(spec))
            assert hv == pytest.approx(gt["hv_true"], rel=1e-12)


@pytest.mark.skipif(os.environ.get("HW_DSE_GT_FULL") != "1", reason="full FPGA grid rebuild (~7 min): HW_DSE_GT_FULL=1")
def test_full_fpga_ground_truth_is_unchanged() -> None:
    """Rebuild the 635,040-design FPGA grid and recompute the M1/M2 ground truth from scratch."""
    from hw_dse import accuracy_table
    from hw_dse.benchmark import build_grid, ground_truth
    from hw_dse.spec import load_spec
    from hw_dse.rtl.generator import REPO_ROOT

    accuracy_table.preload()
    grid = build_grid()
    gts = json.loads((DATA / "ground_truth.json").read_text())
    for name, gt in gts.items():
        now = ground_truth(grid, load_spec(REPO_ROOT / "specs" / f"{name}.yaml"))
        assert now["n_feasible"] == gt["n_feasible"] and now.get("hv_true", 0.0) == gt["hv_true"]
        assert (now["selected"] or {}).get("key") == (gt["selected"] or {}).get("key")
        assert [r["key"] for r in now["front"]] == [r["key"] for r in gt["front"]]
