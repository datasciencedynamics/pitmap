Getting Started
===============

Prerequisites
-------------

``pitmap`` requires Python 3.10 or higher. Its only required dependencies are
``numpy`` (1.24+) and ``scipy`` (1.11+). Optional extras:

- ``pitmap[kernel]`` adds scikit-learn for the kernel interpolator
- ``pitmap[nurbs]`` adds geomdl for the NURBS surface
- ``pitmap[data]`` adds pandas, pyarrow, rasterio and typer for the data scripts
- ``pitmap[viz]`` adds matplotlib

Installation
------------

.. code-block:: bash

   pip install pitmap

Quick example
-------------

Four survey points at the corners of a 10 m square, and a prediction at two
interior locations:

.. code-block:: python

   import numpy as np
   from pitmap import NearestRegion, SectorIDW

   xy = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 10.0], [10.0, 10.0]])
   z = np.array([100.0, 102.0, 101.0, 103.0])
   query = np.array([[2.0, 1.0], [5.0, 5.0]])

   NearestRegion().fit(xy, z).predict(query)
   # array([100., 100.])   nearest point wins (ties go to the first)

   SectorIDW(radius=20, power=2, n_sectors=8).fit(xy, z).predict(query)
   # array([100.27, 101.5 ])   inverse-distance weighted, one point per sector

Interface
---------

Every interpolator is a class with two methods:

``fit(xy, z)``
   ``xy`` is an ``(n, 2)`` array of survey coordinates, ``z`` an ``(n,)`` array
   of the quantity measured there (elevation, ore grade, seam thickness).
   Returns the fitted object.

``predict(xy)``
   ``xy`` is an ``(m, 2)`` array of locations to estimate. Returns an ``(m,)``
   array. Locations that cannot be estimated (for example, no survey point
   inside the search radius) come back as ``NaN``.

The names mirror scikit-learn so the interpolators can be swapped in a loop or
wrapped in a pipeline, but the geometric methods learn nothing from the data in
the statistical sense: ``fit`` stores the points and builds a search structure,
``predict`` evaluates the surface.
