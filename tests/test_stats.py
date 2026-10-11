"""The paired tests behind the M4 A/B claims (hw_dse.stats), against textbook values."""

from __future__ import annotations

import pytest

from hw_dse.stats import betainc, paired_t, sign_test, t_two_sided_p


def test_t_distribution_tail_matches_tables() -> None:
    assert t_two_sided_p(2.262, 9) == pytest.approx(0.05, abs=2e-4)  # t_{0.975, 9}
    assert t_two_sided_p(2.064, 24) == pytest.approx(0.05, abs=2e-4)  # t_{0.975, 24}
    assert t_two_sided_p(0.0, 5) == pytest.approx(1.0)
    assert betainc(2.0, 3.0, 0.4) == pytest.approx(0.5248)  # I_0.4(2, 3)


def test_sign_test_is_exact_and_drops_ties() -> None:
    assert sign_test([1.0] * 5 + [-1.0] * 15) == {"n": 20, "positive": 5, "negative": 15,
                                                    "p": pytest.approx(0.041389, abs=1e-6)}
    assert sign_test([0.0, 1.0])["n"] == 1 and sign_test([])["p"] == 1.0


def test_paired_t() -> None:
    r = paired_t([1.0, 2.0, 3.0, 4.0])
    assert r["mean"] == 2.5 and r["t"] == pytest.approx(2.5 / (1.2909944 / 2)) and r["p"] == pytest.approx(0.0305, abs=1e-3)  # t = 3.873, 3 df
    assert paired_t([1.0])["t"] is None and paired_t([1.0, 1.0])["t"] is None
