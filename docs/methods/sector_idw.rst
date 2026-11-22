Sector inverse distance weighting
=================================

The value at a location is a weighted average of nearby survey points, each
weighted by the inverse of its distance raised to a power
:math:`\alpha` (Zelenskyi et al., 2020; Zelensky and Donchenko, 2025, eq. 11):

.. math::

   Z_A = \frac{\sum_{i=1}^{N} Z_i\, d_i^{-\alpha}}{\sum_{i=1}^{N} d_i^{-\alpha}}

Plain inverse distance weighting has a known weakness: a cluster of points on
one side of the location dominates the average even though the cluster carries
little extra information. The sector rule fixes this. A search circle of the
given radius is divided into ``n_sectors`` equal angular sectors and only the
single closest point in each sector is used, so at most ``n_sectors`` points
contribute and no direction dominates. A location with no survey point inside
the radius returns ``NaN``.

Anisotropy
----------

The critical correlation radius :math:`r_k` (the lag at which the spatial
autocorrelation of the measured quantity dies out) can differ by direction,
for example along versus across the strike of an ore body. Passing
``anisotropy=(rk_x, rk_y)`` scales distances by :math:`r_{k,\max} / r_{k,i}`
before weighting, so a point along the better-correlated axis counts as closer
(Zelensky and Donchenko, 2025, eqs. 12-13).

.. code-block:: python

   from pitmap import SectorIDW
   model = SectorIDW(radius=250, power=2, n_sectors=8).fit(xy, z)
   z_hat = model.predict(grid_xy)

   # along-strike correlation radius 40 m, across-strike 10 m
   model = SectorIDW(radius=250, anisotropy=(40, 10)).fit(xy, z)

Parameters
----------

``radius``
   Search radius, in the units of ``xy``.
``power``
   The exponent :math:`\alpha`. 2 is the usual choice.
``n_sectors``
   Number of angular sectors. 8 follows the original system. With 1 the method
   reduces to nearest neighbour.
``anisotropy``
   ``(rk_x, rk_y)`` or ``None`` for isotropic distances.
