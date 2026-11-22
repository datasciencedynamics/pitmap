Polynomial surface
==================

A bivariate polynomial of degree :math:`M` fitted to the survey points by
least squares (Zelensky and Donchenko, 2025):

.. math::

   Z(x, y) = \sum_{i + j \le M} a_{ij}\, x^i y^j

The original system solves the normal equations by Gaussian elimination;
``pitmap`` centres and scales the coordinates and solves the least-squares
problem directly, which is the same estimate with better conditioning at high
degree.

Adequacy
--------

A polynomial of high enough degree passes through every control point with
:math:`R^2 = 1` and is still useless, because it oscillates between the
points. The 2025 paper therefore judges a fit by three indicators, all
available as attributes after ``fit``:

``r2_``
   Coefficient of determination. 0.5 to 0.8 satisfactory, above 0.8 highly
   reliable, below 0.5 ineffective.
``variance_ratio_``
   :math:`k = (\sigma^2_{data} - \sigma^2_{surface}) / \sigma^2_{data} \cdot 100`.
   The surface should reproduce the spread of the data; the paper accepts
   :math:`|k| < 20\%`.
``lag1_autocorrelation_``
   :math:`r_1`, the autocorrelation between adjacent values of the input
   sequence. Above 0.7 the data carry a consistent trend worth modelling;
   below, they behave as independent values and no smooth surface will fit
   well. This describes the data, not the fit, and depends on the order of
   the points.

``is_adequate()`` applies the first two thresholds; ``select_degree`` fits
degrees 0 to ``max_degree`` and returns the lowest adequate one.

.. code-block:: python

   from pitmap import PolynomialSurface, select_degree

   model = PolynomialSurface(degree=3).fit(xy, z)
   model.adequacy()      # {'r2': ..., 'variance_ratio': ..., 'lag1_autocorrelation': ...}
   z_hat = model.predict(grid_xy)

   best = select_degree(xy, z, max_degree=5)
   best.degree

Parameters
----------

``degree``
   Polynomial degree. The original system offers 0 to 5.
