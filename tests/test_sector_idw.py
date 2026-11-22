import numpy as np
import pytest

from pitmap import SectorIDW


def test_exact_at_training_points():
    rng = np.random.default_rng(1)
    xy = rng.uniform(0, 100, size=(40, 2))
    z = rng.normal(500, 10, size=40)
    model = SectorIDW(radius=50).fit(xy, z)
    np.testing.assert_allclose(model.predict(xy), z)


def test_symmetric_square_returns_mean_at_center():
    # four points at equal distance from the origin, one per quadrant
    xy = np.array([[1.0, 1.0], [-1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]])
    z = np.array([10.0, 20.0, 30.0, 40.0])
    model = SectorIDW(radius=5, n_sectors=4).fit(xy, z)
    assert model.predict(np.array([[0.0, 0.0]]))[0] == pytest.approx(25.0)


def test_outside_radius_is_nan():
    xy = np.array([[0.0, 0.0], [1.0, 0.0]])
    z = np.array([1.0, 2.0])
    model = SectorIDW(radius=2).fit(xy, z)
    assert np.isnan(model.predict(np.array([[100.0, 100.0]]))[0])


def test_sector_rule_limits_cluster_influence():
    # nine points clustered just north of the origin, one point south
    north = np.column_stack([np.linspace(-0.5, 0.5, 9), np.full(9, 2.0)])
    south = np.array([[0.0, -2.0]])
    xy = np.vstack([north, south])
    z = np.concatenate([np.full(9, 100.0), [0.0]])

    plain = SectorIDW(radius=10, n_sectors=1).fit(xy, z)  # effectively plain IDW
    sectored = SectorIDW(radius=10, n_sectors=8).fit(xy, z)
    q = np.array([[0.0, 0.0]])

    # plain IDW is pulled hard toward the cluster; sectoring pulls it back toward the middle
    assert plain.predict(q)[0] > 85.0
    assert sectored.predict(q)[0] < plain.predict(q)[0]


def test_anisotropy_favours_long_axis():
    # one point east, one point north, same distance; stretch correlation along x
    xy = np.array([[10.0, 0.0], [0.0, 10.0]])
    z = np.array([0.0, 100.0])
    iso = SectorIDW(radius=50).fit(xy, z)
    aniso = SectorIDW(radius=50, anisotropy=(40.0, 10.0)).fit(xy, z)
    q = np.array([[0.0, 0.0]])
    assert iso.predict(q)[0] == pytest.approx(50.0)
    # the east point lies along the long axis so it should pull the estimate down
    assert aniso.predict(q)[0] < 50.0


def test_batch_matches_per_node():
    from pitmap.synthetic import grid, sample_survey_points

    xy, z = sample_survey_points(300, seed=3)
    _, _, nodes = grid(60.0)
    for aniso in (None, (40.0, 10.0)):
        m = SectorIDW(radius=200.0, power=2.0, n_sectors=8, anisotropy=aniso).fit(xy, z)
        fast = m.predict(nodes)
        slow = np.array([m._predict_one(q) for q in nodes])
        assert np.allclose(fast, slow, equal_nan=True)
