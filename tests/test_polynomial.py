import numpy as np
import pytest

from pitmap import PolynomialSurface, select_degree


def quadratic(xy):
    x, y = xy[:, 0], xy[:, 1]
    return 3.0 + 0.5 * x - 0.2 * y + 0.01 * x * y + 0.02 * x**2


@pytest.fixture
def data():
    rng = np.random.default_rng(0)
    xy = rng.uniform(-50, 50, size=(200, 2))
    return xy, quadratic(xy)


def test_recovers_quadratic_exactly(data):
    xy, z = data
    m = PolynomialSurface(degree=2).fit(xy, z)
    q = np.array([[10.0, -5.0], [-30.0, 20.0]])
    assert np.allclose(m.predict(q), quadratic(q))
    assert m.r2_ == pytest.approx(1.0)
    assert abs(m.variance_ratio_) < 1e-6


def test_degree_zero_is_mean(data):
    xy, z = data
    m = PolynomialSurface(degree=0).fit(xy, z)
    assert np.allclose(m.predict(xy[:3]), z.mean())
    assert m.r2_ == pytest.approx(0.0, abs=1e-12)
    assert m.variance_ratio_ == pytest.approx(100.0)


def test_too_few_points_raises():
    xy = np.zeros((3, 2))
    with pytest.raises(ValueError):
        PolynomialSurface(degree=2).fit(xy, np.zeros(3))


def test_select_degree_picks_two_for_quadratic(data):
    xy, z = data
    assert select_degree(xy, z, max_degree=5).degree == 2


def test_adequacy_keys(data):
    xy, z = data
    a = PolynomialSurface(1).fit(xy, z).adequacy()
    assert set(a) == {"r2", "variance_ratio", "lag1_autocorrelation"}
