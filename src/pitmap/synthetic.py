"""Synthetic open-pit surface for examples and tests.

A terraced bowl: elevation drops toward the centre in discrete benches, the
way an open pit does, with mild noise so the surface is not perfectly
symmetric. Nothing here comes from any external dataset.
"""

from __future__ import annotations

import numpy as np

EXTENT = 500.0  # metres, half-width of the square domain
RIM_ELEV = 200.0  # metres, elevation at the pit rim
BENCH_HEIGHT = 15.0  # metres, same bench height as in Zelensky & Donchenko (2025)
PIT_RADIUS = 420.0  # metres, radius at which the pit meets flat ground
N_BENCHES = 8


def true_surface(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Elevation of the synthetic pit at (x, y)."""
    r = np.hypot(x, y)
    # smooth cone from rim down to the pit floor
    depth_frac = np.clip(1.0 - r / PIT_RADIUS, 0.0, 1.0)
    cone = RIM_ELEV - depth_frac * N_BENCHES * BENCH_HEIGHT
    # quantise into benches so the walls are stepped
    stepped = RIM_ELEV - np.floor((RIM_ELEV - cone) / BENCH_HEIGHT) * BENCH_HEIGHT
    # gentle regional tilt outside the pit so the ground is not dead flat
    tilt = 0.01 * x + 0.005 * y
    return stepped + tilt


def sample_survey_points(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random survey points over the domain with small measurement noise."""
    rng = np.random.default_rng(seed)
    xy = rng.uniform(-EXTENT, EXTENT, size=(n, 2))
    z = true_surface(xy[:, 0], xy[:, 1]) + rng.normal(0.0, 0.3, size=n)
    return xy, z


def grid(step: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Regular evaluation grid: 1-D axes and the flattened (m, 2) node array."""
    ax = np.arange(-EXTENT, EXTENT + step, step)
    gx, gy = np.meshgrid(ax, ax)
    nodes = np.column_stack([gx.ravel(), gy.ravel()])
    return ax, ax, nodes
