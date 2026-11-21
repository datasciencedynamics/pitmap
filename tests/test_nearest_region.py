import numpy as np

from pitsurf import NearestRegion


def test_nearest_region_reproduces_training_points():
    rng = np.random.default_rng(0)
    xy = rng.uniform(0, 100, size=(50, 2))
    z = rng.normal(500, 10, size=50)
    model = NearestRegion().fit(xy, z)
    np.testing.assert_allclose(model.predict(xy), z)


def test_nearest_region_is_piecewise_constant():
    xy = np.array([[0.0, 0.0], [10.0, 0.0]])
    z = np.array([1.0, 2.0])
    model = NearestRegion().fit(xy, z)
    assert model.predict(np.array([[2.0, 0.0]]))[0] == 1.0
    assert model.predict(np.array([[8.0, 0.0]]))[0] == 2.0
