"""Spatial variability of a sequence of control points.

Autocorrelation function (ACF) and the critical correlation radius, as used
in the automated geological and mine-surveying support system
(Zelensky & Lysenko, 2023; Zelensky & Donchenko, 2025, eq. 10).
"""

from __future__ import annotations

from typing import Optional

import numpy as np


def autocorrelation(values, max_lag: Optional[int] = None) -> np.ndarray:
    """Autocorrelation coefficients r_m for lags m = 0 .. max_lag.

    r_m is the Pearson correlation between the first n - m values and the
    sequence shifted by m. ``max_lag`` defaults to n // 4, the usual
    recommendation. ``values`` must be in sequence order (for example along a
    borehole or a survey line).
    """
    x = np.asarray(values, dtype=float).ravel()
    n = x.size
    if n < 3:
        raise ValueError("need at least 3 values")
    if max_lag is None:
        max_lag = max(1, n // 4)
    if max_lag >= n - 1:
        raise ValueError("max_lag must be smaller than n - 1")
    r = np.empty(max_lag + 1)
    r[0] = 1.0
    for m in range(1, max_lag + 1):
        a, b = x[: n - m], x[m:]
        sa, sb = a.std(), b.std()
        r[m] = 0.0 if sa == 0 or sb == 0 else np.corrcoef(a, b)[0, 1]
    return r


def lag1_autocorrelation(values) -> float:
    """r_1, the autocorrelation between adjacent control points.

    Zelensky & Donchenko (2025) treat r_1 > 0.7 as a consistent spatial trend
    worth modelling and r_1 <= 0.7 as a set of effectively random values.
    """
    return float(autocorrelation(values, max_lag=1)[1])


def critical_radius(values, step: float = 1.0, max_lag: Optional[int] = None) -> float:
    """Critical correlation radius r_k.

    Distance at which the ACF first crosses zero, found by linear
    interpolation between the last positive and first non-positive
    coefficient, multiplied by ``step`` (the spacing between control points).
    Returns ``inf`` if the ACF stays positive over all computed lags.
    """
    r = autocorrelation(values, max_lag)
    for m in range(1, r.size):
        if r[m] <= 0:
            frac = r[m - 1] / (r[m - 1] - r[m]) if r[m - 1] != r[m] else 0.0
            return float(((m - 1) + frac) * step)
    return float("inf")
