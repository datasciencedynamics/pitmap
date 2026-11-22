"""pitmap: surface construction from scattered survey points."""

from pitmap.core.interpolation import NearestRegion, SectorIDW
from pitmap.core.polynomial import PolynomialSurface, select_degree
from pitmap.core.variability import (
    autocorrelation,
    critical_radius,
    lag1_autocorrelation,
)

__all__ = [
    "NearestRegion",
    "SectorIDW",
    "PolynomialSurface",
    "select_degree",
    "autocorrelation",
    "lag1_autocorrelation",
    "critical_radius",
]
__version__ = "0.0.0a6"
