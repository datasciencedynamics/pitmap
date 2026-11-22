<img src="https://raw.githubusercontent.com/datasciencedynamics/pitmap/main/docs/logo.svg" width="520" alt="pitmap">

[![PyPI](https://img.shields.io/pypi/v/pitmap.svg)](https://pypi.org/project/pitmap/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/datasciencedynamics/pitmap/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
[![Docs](https://img.shields.io/badge/docs-datasciencedynamics.com%2Fpitmap-0057B7.svg)](https://datasciencedynamics.com/pitmap/)

Surface construction from scattered survey points for open-pit mine surveying.

`pitmap` is a Python implementation of the surface-modeling methods used in
the automated geological and mine-surveying support system developed at the
State University of Economics and Technology (Kryvyi Rih, Ukraine), with a
kernel-based interpolator added for comparison. All methods share one
`fit` / `predict` interface.

> **Status:** pre-alpha. The API will change. Nothing here is ready for
> production use yet.

Documentation: https://datasciencedynamics.com/pitmap/

## Methods

| Class | Method | Source |
|---|---|---|
| `NearestRegion` | Polygonal (nearest-region / Thiessen) surface | Zelensky & Lysenko (2023) |
| `SectorIDW` | Sector-constrained inverse distance weighting, optional anisotropy via critical correlation radius | Zelenskyi et al. (2020); Zelensky & Donchenko (2025) |
| `PolynomialSurface` | Bivariate least-squares polynomial up to degree 5, with adequacy statistics | Zelenskyi et al. (2020); Zelensky & Donchenko (2025) |
| `NURBSSurface` | Tensor-product NURBS smoother over an interpolated grid | Zelensky & Lysenko (2023) |
| `KernelSurface` | SVR / Gaussian process with the critical correlation radius as default length scale | this package |

Utilities: `autocorrelation()`, `lag1_autocorrelation()` and
`critical_radius()` (spatial autocorrelation function and the critical
correlation radius) and `prism_volume()` (volume between surfaces by unit
prisms). `pitmap.synthetic` generates a terraced test pit.

Implemented so far: `NearestRegion`, `SectorIDW`, `PolynomialSurface`,
`select_degree`, the autocorrelation utilities.

## Install

```bash
pip install pitmap
```

## Usage

```python
import numpy as np
from pitmap import NearestRegion

xy = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 10.0], [10.0, 10.0]])
z = np.array([100.0, 102.0, 101.0, 103.0])

model = NearestRegion().fit(xy, z)
model.predict(np.array([[2.0, 1.0], [9.0, 9.0]]))
# array([100., 103.])
```

## Repository layout

```
src/pitmap/      package; core/ holds the interpolators
data_gen.py          fetch a raw DEM tile -> data/raw (Parquet, optional CSV)
preprocessing.py     subsample to sparse survey points -> data/processed
notebooks/           analysis; outputs stripped before commit
data/                gitignored
```

## Development

```bash
conda activate conda_312
make create_venv && source venv_pitmap/bin/activate
make requirements
make test
make help            # list all targets
```

## Acknowledgements

The surface-construction methods implemented here were developed by
Prof. Oleksandr Zelenskyi, Volodymyr Lysenko and Oleksii Donchenko of the
Department of Informatics and Applied Software, State University of Economics
and Technology (Kryvyi Rih, Ukraine), over many years of work on automated
geological and mine-surveying support for open-pit mining. This package is an
independent open-source implementation of the methods as described in their
published papers (below); it contains none of their source code. Any errors in
the implementation are the package author's alone.

## References

Zelenskyi, O., Lysenko, V., Alekseyev, M., & Vlasov, V. (2020). Modeling of
the earth's surface subsidence during its undermining by stoping in coal mines.
*Naukovyi Visnyk Natsionalnoho Hirnychoho Universytetu*, (6), 121–127.
https://doi.org/10.33271/nvngu/2020-6/121

Zelensky, O., & Lysenko, V. (2023). Construction surface using desktop and
mobile applications. *Economics and Technical Engineering*, 1(1), 87–102.
https://doi.org/10.62911/ete.2023.01.01.07

Zelensky, O., & Donchenko, O. (2025). Research and application of polynomial
models in the development of an automated geological and mine surveying
support system for open-pit mining. *Mining Journal of Kryvyi Rih National
University*, 59(1), 10–21. https://doi.org/10.31721/2306-5435-2025-1-10-21

## License

MIT
