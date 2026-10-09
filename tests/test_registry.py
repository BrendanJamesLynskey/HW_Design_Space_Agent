"""The family registry: clamping LLM-proposed ranges, and design schedules."""

from __future__ import annotations

import pytest

from hw_dse.families import REGISTRY, ArchConfig, clamp_ranges, full_box


def test_registry_has_the_four_families() -> None:
    assert set(REGISTRY) == {"iterative", "unrolled_k", "pipelined", "pipelined_m"}


def test_clamp_out_of_range_and_reversed() -> None:
    r = clamp_ranges("pipelined", {"data_width": [40, 4], "n_iter": [10, 12]})
    assert r.ranges["data_width"] == (8, 28)
    assert r.ranges["n_iter"] == (10, 12)
    assert any("swapped" in n for n in r.notes)
    assert any("clamped" in n for n in r.notes)


def test_clamp_entirely_outside_snaps_to_edge() -> None:
    r = clamp_ranges("iterative", {"frac_guard": [9, 12]})
    assert r.ranges["frac_guard"] == (4, 4)


def test_unknown_params_dropped_and_missing_filled() -> None:
    r = clamp_ranges("iterative", {"k": [2, 4], "voltage": 0.9})
    assert "k" not in r.ranges and "voltage" not in r.ranges
    assert r.ranges == full_box("iterative")
    assert len(r.notes) == 2


def test_categorical_filtered() -> None:
    r = clamp_ranges("pipelined_m", {"rounding": ["round", "stochastic"], "m": 3})
    assert r.ranges["rounding"] == ("round",)
    assert r.ranges["m"] == (3, 3)


def test_unknown_family_rejected() -> None:
    with pytest.raises(KeyError):
        clamp_ranges("systolic", {})


def test_unparseable_falls_back() -> None:
    r = clamp_ranges("iterative", {"n_iter": "lots"})
    assert r.ranges["n_iter"] == (4, 30)


def test_schedules_match_reference() -> None:
    p = dict(data_width=16, n_iter=14, angle_guard=0, frac_guard=0, rounding="trunc")
    it = ArchConfig.from_params("iterative", p)
    pl = ArchConfig.from_params("pipelined", p)
    assert it.latency_cycles == 17 and it.results_per_cycle == pytest.approx(1 / 17)
    assert pl.latency_cycles == 16 and pl.results_per_cycle == 1.0
    assert ArchConfig.from_params("unrolled_k", {**p, "k": 4}).latency_cycles == 4 + 3
    assert ArchConfig.from_params("pipelined_m", {**p, "m": 4}).latency_cycles == 4 + 2
    # k is ignored outside unrolled_k
    assert ArchConfig.from_params("iterative", {**p, "k": 4}).k == 1


def test_key_round_trips() -> None:
    from hw_dse.families import ArchConfig

    for a in (ArchConfig.from_params("unrolled_k", {"data_width": 12, "n_iter": 9, "angle_guard": -2, "rounding": "round", "k": 3}),
              ArchConfig.from_params("pipelined", {"data_width": 20, "n_iter": 18, "frac_guard": 2})):
        assert ArchConfig.from_key(a.key()) == a
