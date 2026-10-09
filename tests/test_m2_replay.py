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
    ("qwen/qwen3.8-27b", "high_precision", 4),        # the M2 blind-spot run (+71.7% regret)
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
