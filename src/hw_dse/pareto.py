"""Pareto dominance and hypervolume: the maths that decides "better".

Everything here works in **minimisation form**: a point is a tuple of
objective values where smaller is better in every coordinate (maximised
objectives are negated by :func:`hw_dse.evaluate.objective_vector`).

Dominance
    a dominates b iff a <= b in every coordinate and a < b in at least one.
    The Pareto front is the set of points nobody dominates.

Hypervolume (HV)
    The volume of objective space that is dominated by the front and
    bounded by a reference point r (the "worst acceptable" corner). Points
    that do not strictly beat r in every coordinate contribute nothing.
    HV is the standard single-number quality measure for a front: it grows
    when the front moves towards the ideal *or* spreads out, and it is
    maximised only by the true Pareto front. The eval reports what
    fraction of the true (exhaustive-grid) HV each method reaches.

Algorithms
    * 2-D: sort by the first objective and sweep, O(n log n).
    * n-D: recursive slicing along the last objective ("HSO"). Exponential
      in the worst case but exact, and our fronts are small (tens of
      points, <= 3 objectives).

Both are checked against hand-computed cases in ``tests/test_pareto.py``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

Point = Sequence[float]


def dominates(a: Point, b: Point) -> bool:
    better_or_equal = all(x <= y for x, y in zip(a, b))
    strictly = any(x < y for x, y in zip(a, b))
    return better_or_equal and strictly


def pareto_mask(points: np.ndarray) -> np.ndarray:
    """Boolean mask of non-dominated rows of an (n, d) array.

    Duplicates of a non-dominated point are all kept (neither dominates the
    other). Vectorised over the candidate set; O(n^2 d) worst case, fine for
    the hundreds-to-thousands of points we feed it, and :func:`pareto_front_large`
    handles the exhaustive grid.
    """
    pts = np.asarray(points, dtype=float)
    n = pts.shape[0]
    if n == 0:
        return np.zeros(0, dtype=bool)
    keep = np.ones(n, dtype=bool)
    for i in range(n):
        if not keep[i]:
            continue
        p = pts[i]
        # rows that p dominates
        dominated = np.all(p <= pts, axis=1) & np.any(p < pts, axis=1)
        keep &= ~dominated
    return keep


def pareto_front_large(points: np.ndarray) -> np.ndarray:
    """Indices of the non-dominated rows of a big (n, d) array.

    Sorts lexicographically first so dominated points are discarded early;
    only survivors are compared against each other.
    """
    pts = np.asarray(points, dtype=float)
    if pts.shape[0] == 0:
        return np.zeros(0, dtype=int)
    order = np.lexsort(pts.T[::-1])
    front: list[int] = []
    front_pts = np.empty((0, pts.shape[1]))
    for idx in order:
        p = pts[idx]
        if front_pts.shape[0] and np.any(np.all(front_pts <= p, axis=1) & np.any(front_pts < p, axis=1)):
            continue
        # p is not dominated by the current front; since we visit in
        # lexicographic order, p cannot dominate an earlier front member
        # unless equal-prefix ties, so remove any it dominates.
        if front_pts.shape[0]:
            dom = np.all(p <= front_pts, axis=1) & np.any(p < front_pts, axis=1)
            if dom.any():
                keep = ~dom
                front = [f for f, k in zip(front, keep) if k]
                front_pts = front_pts[keep]
        front.append(int(idx))
        front_pts = np.vstack([front_pts, p])
    return np.array(sorted(front), dtype=int)


def _filter_ref(points: np.ndarray, ref: Point) -> np.ndarray:
    pts = np.asarray(points, dtype=float).reshape(-1, len(ref))
    r = np.asarray(ref, dtype=float)
    return pts[np.all(pts < r, axis=1)]


def hypervolume(points: np.ndarray | Sequence[Point], ref: Point) -> float:
    """Exact hypervolume of ``points`` (minimisation) w.r.t. ``ref``."""
    pts = _filter_ref(np.asarray(points, dtype=float), ref)
    if pts.shape[0] == 0:
        return 0.0
    pts = pts[pareto_mask(pts)]
    pts = np.unique(pts, axis=0)
    return _hv(pts, np.asarray(ref, dtype=float))


def _hv(pts: np.ndarray, ref: np.ndarray) -> float:
    d = pts.shape[1]
    if pts.shape[0] == 0:
        return 0.0
    if d == 1:
        return float(ref[0] - pts[:, 0].min())
    if d == 2:
        order = np.argsort(pts[:, 0], kind="stable")
        hv, best_y = 0.0, ref[1]
        for x, y in pts[order]:
            if y < best_y:
                hv += (ref[0] - x) * (best_y - y)
                best_y = y
        return float(hv)
    # Slice along the last objective: between consecutive distinct values
    # of that objective, the dominated region is a (d-1)-D HV times the
    # slab thickness.
    order = np.argsort(pts[:, -1], kind="stable")
    pts = pts[order]
    hv = 0.0
    zs = list(pts[:, -1]) + [ref[-1]]
    for i in range(pts.shape[0]):
        thickness = zs[i + 1] - zs[i]
        if thickness <= 0:
            continue
        slab = pts[: i + 1, :-1]
        slab = slab[pareto_mask(slab)]
        hv += thickness * _hv(slab, ref[:-1])
    return float(hv)


def hv_progress(points: np.ndarray, feasible: np.ndarray, ref: Point) -> np.ndarray:
    """HV of the feasible prefix after each evaluation (anytime curve).

    ``points[i]`` is the objective vector of evaluation i. Returns an array
    ``hv[i]`` = HV of feasible points among the first i+1 evaluations. The
    HV is only recomputed when a new feasible point beats the reference.
    """
    pts = np.asarray(points, dtype=float)
    r = np.asarray(ref, dtype=float)
    out = np.zeros(pts.shape[0])
    current: list[np.ndarray] = []
    hv = 0.0
    for i in range(pts.shape[0]):
        if feasible[i] and np.all(pts[i] < r):
            if not current or not np.any([np.all(c <= pts[i]) for c in current]):
                current.append(pts[i])
                cur = np.array(current)
                cur = cur[pareto_mask(cur)]
                current = list(cur)
                hv = hypervolume(cur, ref)
        out[i] = hv
    return out
