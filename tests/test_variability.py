import numpy as np
import pytest

from pitmap import autocorrelation, critical_radius, lag1_autocorrelation


def test_paper_example_lag1():
    # Zelensky & Donchenko (2025): 5, 8, 1, 9, 4, 6, 9, 10
    x = [5, 8, 1, 9, 4, 6, 9, 10]
    r1 = lag1_autocorrelation(x)
    expected = np.corrcoef(x[:-1], x[1:])[0, 1]
    assert r1 == pytest.approx(expected)


def test_smooth_trend_has_high_r1():
    x = np.sin(np.linspace(0, 2 * np.pi, 40))
    assert lag1_autocorrelation(x) > 0.9


def test_acf_starts_at_one():
    r = autocorrelation(np.arange(20.0), max_lag=4)
    assert r[0] == 1.0 and r.size == 5


def test_critical_radius_scales_with_step():
    x = np.sin(np.linspace(0, 2 * np.pi, 40))
    assert critical_radius(x, step=2.0, max_lag=15) == pytest.approx(
        2.0 * critical_radius(x, step=1.0, max_lag=15)
    )


def test_critical_radius_sine():
    # ACF of a sine over one period crosses zero near a quarter period
    x = np.sin(np.linspace(0, 2 * np.pi, 41))
    rk = critical_radius(x, step=1.0, max_lag=15)
    assert 8 < rk < 15
