Spatial variability
===================

How far apart two measurements can be and still tell you something about each
other. The system answers this with the autocorrelation function of a
sequence of control points (Zelensky and Lysenko, 2023; Zelensky and
Donchenko, 2025, eq. 10):

.. math::

   r_m = \frac{\sum_{i=1}^{n-m} (x_i - \bar{x}_1)(x_{i+m} - \bar{x}_2)}
              {\sqrt{\sum_{i=1}^{n-m} (x_i - \bar{x}_1)^2 \sum_{i=1}^{n-m} (x_{i+m} - \bar{x}_2)^2}}

where :math:`\bar{x}_1` and :math:`\bar{x}_2` are the means of the original
and the shifted sequence. :math:`r_0 = 1`; the maximum lag is usually
:math:`n / 4`.

Critical correlation radius
---------------------------

The lag at which :math:`r_m` first reaches zero, times the spacing between
control points, is the critical correlation radius :math:`r_k`: beyond it the
measured quantity is effectively uncorrelated, so it bounds how far a model
can be trusted to extrapolate. The paper reports :math:`r_k` for copper grade
at Erdenet of roughly 24 m along strike versus 20 m across it from blast-hole
sampling, and 120 m by depth; those directional values are what
:class:`pitmap.SectorIDW` takes as ``anisotropy``.

.. code-block:: python

   from pitmap import autocorrelation, lag1_autocorrelation, critical_radius

   r = autocorrelation(grades, max_lag=10)      # r_0 .. r_10
   r1 = lag1_autocorrelation(grades)            # > 0.7: consistent trend
   rk = critical_radius(grades, step=8.0)       # metres, for an 8 m sample spacing

Values must be in sequence order, for example down a borehole or along a
survey line.
