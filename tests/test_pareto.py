"""Pareto dominance and hypervolume on hand-checked cases."""

from __future__ import annotations

import numpy as np
import pytest

from hw_dse.pareto import dominates, hv_progress, hypervolume, pareto_front_large, pareto_mask


def test_dominance() -> None:
    assert dominates((1, 1), (2, 2))
    assert dominates((1, 2), (1, 3))
    assert not dominates((1, 2), (1, 2))  # equal: no
    assert not dominates((1, 3), (2, 2))  # trade-off: no


def test_pareto_mask() -> None:
    pts = np.array([[1, 5], [2, 3], [3, 4], [4, 1], [2, 3], [5, 5]])
    assert pareto_mask(pts).tolist() == [True, True, False, True, True, False]
    assert sorted(pareto_front_large(pts).tolist()) == [0, 1, 3, 4]


def test_hv_2d_hand_computed() -> None:
    # Staircase (1,3), (2,2), (3,1) with ref (4,4):
    # columns x in [1,2): 4-3=1, [2,3): 2, [3,4): 3  -> 6
    assert hypervolume([(1, 3), (2, 2), (3, 1)], (4, 4)) == pytest.approx(6.0)
    # A dominated point and an out-of-reference point change nothing.
    assert hypervolume([(1, 3), (2, 2), (3, 1), (3, 3), (5, 0)], (4, 4)) == pytest.approx(6.0)
    # Single point: a rectangle.
    assert hypervolume([(1, 1)], (3, 4)) == pytest.approx(6.0)
    assert hypervolume([], (1, 1)) == 0.0
    # Point on the reference boundary contributes nothing.
    assert hypervolume([(4, 1)], (4, 4)) == 0.0


def test_hv_3d_hand_computed() -> None:
    # Single box: 1*2*3.
    assert hypervolume([(0, 0, 0)], (1, 2, 3)) == pytest.approx(6.0)
    # Two boxes of 2x2x2 offset by one in x: union = 8 + 8 - 1*2*2 = 12
    # with points (0,0,0) and (1,0,0) the second is dominated -> 8.
    assert hypervolume([(0, 0, 0), (1, 0, 0)], (2, 2, 2)) == pytest.approx(8.0)
    # (0,1,1) and (1,0,1) and (1,1,0) with ref (2,2,2):
    # each dominates a 2x1x1 box; pairwise overlaps 1x1x1; triple overlap 1.
    # inclusion-exclusion: 3*2 - 3*1 + 1 = 4
    assert hypervolume([(0, 1, 1), (1, 0, 1), (1, 1, 0)], (2, 2, 2)) == pytest.approx(4.0)


def test_hv_matches_monte_carlo_3d() -> None:
    rng = np.random.default_rng(0)
    pts = rng.random((12, 3))
    ref = np.array([1.0, 1.0, 1.0])
    exact = hypervolume(pts, ref)
    samples = rng.random((200_000, 3))
    dominated = np.zeros(len(samples), dtype=bool)
    for p in pts:
        dominated |= np.all(samples >= p, axis=1)
    assert exact == pytest.approx(dominated.mean(), abs=0.01)


def test_hv_progress_is_monotone_and_ignores_infeasible() -> None:
    pts = np.array([(3, 3), (1, 1), (2, 2), (1, 3)])
    feas = np.array([True, False, True, True])
    prog = hv_progress(pts, feas, (4, 4))
    assert prog.tolist() == pytest.approx([1.0, 1.0, 4.0, 4.0 + 1.0 * 1.0])
