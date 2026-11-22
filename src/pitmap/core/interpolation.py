"""Interpolators that share one fit/predict interface.

Each class takes survey points as an (n, 2) array of x, y coordinates and an
(n,) array of elevations (or any indicator such as ore grade) z, and predicts
z at new x, y locations.

Methods follow the automated geological and mine-surveying support system
described in Zelenskyi et al. (2020), Zelensky & Lysenko (2023), and
Zelensky & Donchenko (2025).
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import NearestNDInterpolator
from scipy.spatial import cKDTree


def _check_xy_z(xy: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xy = np.asarray(xy, dtype=float)
    z = np.asarray(z, dtype=float)
    if xy.ndim != 2 or xy.shape[1] != 2:
        raise ValueError("xy must have shape (n, 2)")
    if z.shape != (xy.shape[0],):
        raise ValueError("z must have shape (n,)")
    return xy, z


def _check_query(xy: np.ndarray) -> np.ndarray:
    xy = np.asarray(xy, dtype=float)
    if xy.ndim != 2 or xy.shape[1] != 2:
        raise ValueError("query xy must have shape (m, 2)")
    return xy


class NearestRegion:
    """Polygonal (nearest-region / Thiessen polygon) surface.

    Every location takes the elevation of its closest survey point, so the
    surface is piecewise constant over the Voronoi cell of each point. This is
    the classical polygonal method of mine surveying and reserve estimation
    (Zelensky & Lysenko, 2023, section 4).
    """

    def __init__(self) -> None:
        self._interp: NearestNDInterpolator | None = None

    def fit(self, xy: np.ndarray, z: np.ndarray) -> "NearestRegion":
        xy, z = _check_xy_z(xy, z)
        self._interp = NearestNDInterpolator(xy, z)
        return self

    def predict(self, xy: np.ndarray) -> np.ndarray:
        if self._interp is None:
            raise RuntimeError("call fit() before predict()")
        xy = _check_query(xy)
        return self._interp(xy[:, 0], xy[:, 1])


class SectorIDW:
    """Sector-constrained inverse distance weighting.

    The value at a query point is a weighted average of nearby survey points,
    with weight 1 / d**power (Zelenskyi et al., 2020; Zelensky & Donchenko,
    2025, eq. 11). To stop a cluster of points on one side from dominating,
    the search circle of the given radius is cut into ``n_sectors`` equal
    angular sectors and only the single closest point in each sector is used
    (2020 paper, Fig. 3). Query points with no survey point inside the radius
    return NaN.

    Parameters
    ----------
    radius : float
        Search radius in the units of xy.
    power : float, default 2.0
        Distance exponent alpha. 2 is the usual choice.
    n_sectors : int, default 8
        Number of angular sectors around each query point.
    anisotropy : tuple[float, float] or None
        Critical correlation radius along x and along y, (rk_x, rk_y). When
        given, distances are scaled by rk_max / rk_axis before weighting so a
        point along the better-correlated axis counts as closer (Zelensky &
        Donchenko, 2025, eq. 12-13). None means isotropic.
    """

    def __init__(
        self,
        radius: float,
        power: float = 2.0,
        n_sectors: int = 8,
        anisotropy: tuple[float, float] | None = None,
    ) -> None:
        if radius <= 0:
            raise ValueError("radius must be positive")
        if n_sectors < 1:
            raise ValueError("n_sectors must be at least 1")
        if anisotropy is not None:
            rk_x, rk_y = anisotropy
            if rk_x <= 0 or rk_y <= 0:
                raise ValueError("anisotropy radii must be positive")
        self.radius = float(radius)
        self.power = float(power)
        self.n_sectors = int(n_sectors)
        self.anisotropy = anisotropy
        self._xy: np.ndarray | None = None
        self._z: np.ndarray | None = None
        self._tree: cKDTree | None = None

    # scale factors that stretch the axis with the shorter correlation radius
    def _axis_scale(self) -> np.ndarray:
        if self.anisotropy is None:
            return np.ones(2)
        rk = np.asarray(self.anisotropy, dtype=float)
        return rk.max() / rk

    def fit(self, xy: np.ndarray, z: np.ndarray) -> "SectorIDW":
        xy, z = _check_xy_z(xy, z)
        self._xy = xy
        self._z = z
        # the tree is built on scaled coordinates so the radius search already
        # respects anisotropy
        self._tree = cKDTree(xy * self._axis_scale())
        return self

    def _predict_one(self, q: np.ndarray) -> float:
        assert self._tree is not None and self._xy is not None and self._z is not None
        scale = self._axis_scale()
        q_scaled = q * scale
        idx = self._tree.query_ball_point(q_scaled, self.radius)
        if len(idx) == 0:
            return np.nan
        idx = np.asarray(idx)

        delta = self._xy[idx] * scale - q_scaled  # (k, 2) offsets, scaled
        d = np.hypot(delta[:, 0], delta[:, 1])

        # a survey point sitting exactly on the query location wins outright
        hit = np.where(d == 0.0)[0]
        if hit.size:
            return float(self._z[idx[hit[0]]])

        # assign each candidate to an angular sector and keep the closest per sector
        angle = np.arctan2(delta[:, 1], delta[:, 0])  # (-pi, pi]
        sector = np.floor((angle + np.pi) / (2.0 * np.pi / self.n_sectors)).astype(int)
        sector = np.clip(sector, 0, self.n_sectors - 1)

        keep: list[int] = []
        for s in np.unique(sector):
            members = np.where(sector == s)[0]
            keep.append(members[np.argmin(d[members])])
        keep_arr = np.asarray(keep)

        w = d[keep_arr] ** (-self.power)
        return float(np.sum(w * self._z[idx[keep_arr]]) / np.sum(w))

    def predict(self, xy: np.ndarray) -> np.ndarray:
        if self._tree is None:
            raise RuntimeError("call fit() before predict()")
        xy = _check_query(xy)
        return np.array([self._predict_one(q) for q in xy])
