import numpy as np

from pitmap.synthetic import grid, sample_survey_points, true_surface


def test_rim_higher_than_floor():
    assert true_surface(np.array([480.0]), np.array([0.0]))[0] > true_surface(
        np.array([0.0]), np.array([0.0])
    )[0]


def test_sampling_is_reproducible():
    xy1, z1 = sample_survey_points(50, seed=1)
    xy2, z2 = sample_survey_points(50, seed=1)
    assert np.array_equal(xy1, xy2) and np.array_equal(z1, z2)


def test_grid_shape():
    ax, ay, nodes = grid(100.0)
    assert nodes.shape == (ax.size * ay.size, 2)
