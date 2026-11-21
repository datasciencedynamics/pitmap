<img src="https://raw.githubusercontent.com/lshpaner/pitsurf/main/docs/logo.svg" width="520" alt="pitsurf">

[![PyPI](https://img.shields.io/pypi/v/pitsurf.svg)](https://pypi.org/project/pitsurf/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/lshpaner/pitsurf/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

Surface construction from scattered survey points for open-pit mine surveying.

`pitsurf` is a Python implementation of the surface-modeling methods used in
the automated geological and mine-surveying support system developed at the
State University of Economics and Technology (Kryvyi Rih, Ukraine), with a
kernel-based interpolator added for comparison. All methods share one
`fit` / `predict` interface.

> **Status:** pre-alpha. The API will change. Nothing here is ready for
> production use yet.

## Methods

| Class | Method | Source |
|---|---|---|
| `NearestRegion` | Polygonal (nearest-region / Thiessen) surface | Zelensky & Lysenko (2023) |
| `SectorIDW` | Sector-constrained inverse distance weighting, optional anisotropy via critical correlation radius | Zelenskyi et al. (2020); Zelensky & Donchenko (2025) |
| `PolynomialSurface` | Bivariate least-squares polynomial up to degree 5, with adequacy statistics | Zelenskyi et al. (2020); Zelensky & Donchenko (2025) |
| `NURBSSurface` | Tensor-product NURBS smoother over an interpolated grid | Zelensky & Lysenko (2023) |
| `KernelSurface` | SVR / Gaussian process with the critical correlation radius as default length scale | this package |

Utilities: `acf_radius()` (critical correlation radius from the spatial
autocorrelation function) and `prism_volume()` (volume between surfaces by
unit prisms).

Implemented so far: `NearestRegion`, `SectorIDW`.

## Install

```bash
pip install pitsurf
```

## Usage

```python
import numpy as np
from pitsurf import NearestRegion

xy = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 10.0], [10.0, 10.0]])
z = np.array([100.0, 102.0, 101.0, 103.0])

model = NearestRegion().fit(xy, z)
model.predict(np.array([[2.0, 1.0], [9.0, 9.0]]))
# array([100., 103.])
```

## Repository layout

```
pitsurf/          package; core/ holds the interpolators
data_gen.py          fetch a raw DEM tile -> data/raw (Parquet, optional CSV)
preprocessing.py     subsample to sparse survey points -> data/processed
notebooks/           analysis; outputs stripped before commit
data/                gitignored
```

## Development

```bash
conda activate conda_312
make create_venv && source venv_pit/bin/activate
make requirements
make test
make help            # list all targets
```

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
