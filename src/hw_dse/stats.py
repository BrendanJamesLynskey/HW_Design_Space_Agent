"""Paired tests for the A/Bs (milestone 4), without a SciPy dependency.

The fleet A/B compares two arms run on the same (spec, seed) pairs, so the
comparisons are paired: per pair, the difference fleet - single. Two tests:

* :func:`sign_test`: the exact two-sided binomial sign test (ties dropped),
  which assumes nothing about the size of the differences;
* :func:`paired_t`: Student's paired t-test, two-sided, with the t
  distribution's tail from the regularized incomplete beta function
  (the Numerical Recipes continued fraction, accurate to ~1e-10 here).

Both are what code reports; the write-up quotes them, with the sample size,
and never a p-value without its test.
"""

from __future__ import annotations

import math


def sign_test(diffs: list[float]) -> dict[str, float | int]:
    """Exact two-sided sign test on paired differences; zero differences are dropped."""
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    n = pos + neg
    if n == 0:
        return {"n": 0, "positive": 0, "negative": 0, "p": 1.0}
    k = min(pos, neg)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return {"n": n, "positive": pos, "negative": neg, "p": min(1.0, 2 * tail)}


def _betacf(a: float, b: float, x: float) -> float:
    tiny, eps = 1e-300, 3e-16
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        dl = d * c
        h *= dl
        if abs(dl - 1.0) < eps:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x)
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(lbt) * _betacf(a, b, x) / a
    return 1.0 - math.exp(lbt) * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t: float, df: int) -> float:
    return betainc(df / 2.0, 0.5, df / (df + t * t))


def paired_t(diffs: list[float]) -> dict[str, float | int | None]:
    """Paired t-test (two-sided) on the differences; ``t`` is None below two pairs."""
    n = len(diffs)
    if n < 2:
        return {"n": n, "mean": diffs[0] if diffs else None, "t": None, "p": None}
    mean = sum(diffs) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1))
    if sd == 0:
        return {"n": n, "mean": mean, "t": None, "p": None}
    t = mean / (sd / math.sqrt(n))
    return {"n": n, "mean": mean, "t": t, "p": t_two_sided_p(t, n - 1)}
