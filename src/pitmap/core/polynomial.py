"""Polynomial surface by least squares with the adequacy checks of
Zelensky & Donchenko (2025)."""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from pitmap.core.interpolation import _check_query, _check_xy_z
from pitmap.core.variability import lag1_autocorrelation


def _monomial_powers(degree: int) -> List[Tuple[int, int]]:
    return [
        (i, j) for d in range(degree + 1) for i in range(d, -1, -1) for j in [d - i]
    ]


class PolynomialSurface:
    """Bivariate polynomial surface z = f(x, y) fitted by least squares.

    The surface is a sum of monomials ``x**i * y**j`` with ``i + j <= degree``.
    Coordinates are centred and scaled internally so high degrees stay
    numerically stable; ``coef_`` is in those scaled units.

    After ``fit`` the three adequacy indicators of Zelensky & Donchenko (2025)
    are available:

    ``r2_``
        Coefficient of determination. The paper reads 0.5 to 0.8 as
        satisfactory, above 0.8 as highly reliable, below 0.5 as ineffective.
    ``variance_ratio_``
        ``(var(z) - var(fitted)) / var(z) * 100``, the percentage by which the
        surface's variance departs from the data's. The paper accepts
        differences under 20 percent; a polynomial that interpolates every point
        can have R2 = 1 and still fail this check by oscillating between points.
    ``lag1_autocorrelation_``
        r_1 of the input ``z`` in the order given. This describes the data,
        not the fit; the paper treats r_1 > 0.7 as a trend worth modelling.

    Parameters
    ----------
    degree
        Polynomial degree, 0 to 5 in the original system. Higher degrees are
        allowed but rarely adequate.
    """

    def __init__(self, degree: int = 2):
        if degree < 0:
            raise ValueError("degree must be >= 0")
        self.degree = int(degree)

    def _design(self, xy: np.ndarray) -> np.ndarray:
        u = (xy - self._center) / self._scale
        return np.column_stack([u[:, 0] ** i * u[:, 1] ** j for i, j in self._powers])

    def fit(self, xy, z) -> "PolynomialSurface":
        xy, z = _check_xy_z(xy, z)
        self._powers = _monomial_powers(self.degree)
        if xy.shape[0] < len(self._powers):
            raise ValueError(
                f"degree {self.degree} needs at least {len(self._powers)} points"
            )
        self._center = xy.mean(axis=0)
        self._scale = np.maximum(xy.std(axis=0), 1e-12)
        A = self._design(xy)
        self.coef_, *_ = np.linalg.lstsq(A, z, rcond=None)
        fitted = A @ self.coef_
        ss_res = float(np.sum((z - fitted) ** 2))
        ss_tot = float(np.sum((z - z.mean()) ** 2))
        self.r2_ = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        var_z = z.var(ddof=1) if z.size > 1 else 0.0
        var_f = fitted.var(ddof=1) if z.size > 1 else 0.0
        self.variance_ratio_ = (var_z - var_f) / var_z * 100.0 if var_z > 0 else 0.0
        self.lag1_autocorrelation_ = (
            lag1_autocorrelation(z) if z.size >= 3 else float("nan")
        )
        return self

    def predict(self, xy) -> np.ndarray:
        xy = _check_query(xy)
        return self._design(xy) @ self.coef_

    def adequacy(self) -> Dict[str, float]:
        """The three indicators as a dict."""
        return {
            "r2": self.r2_,
            "variance_ratio": self.variance_ratio_,
            "lag1_autocorrelation": self.lag1_autocorrelation_,
        }

    def is_adequate(
        self, r2_min: float = 0.5, variance_ratio_max: float = 20.0
    ) -> bool:
        """Whether the fit meets the paper's thresholds on R2 and variance ratio."""
        return self.r2_ >= r2_min and abs(self.variance_ratio_) <= variance_ratio_max


def select_degree(xy, z, max_degree: int = 5, **thresholds) -> PolynomialSurface:
    """Fit degrees 0..max_degree and return the lowest adequate one.

    If no degree is adequate, returns the one with the highest R2 among those
    within the variance-ratio limit, or the highest-R2 fit overall.
    """
    fits = []
    for d in range(max_degree + 1):
        try:
            fits.append(PolynomialSurface(d).fit(xy, z))
        except ValueError:
            break
    for m in fits:
        if m.is_adequate(**thresholds):
            return m
    vmax = thresholds.get("variance_ratio_max", 20.0)
    ok = [m for m in fits if abs(m.variance_ratio_) <= vmax] or fits
    return max(ok, key=lambda m: m.r2_)
