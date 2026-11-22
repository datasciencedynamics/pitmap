Polygonal (nearest region)
==========================

The oldest method in mine surveying. Every location takes the value of its
closest survey point, so the surface is piecewise constant over the Voronoi
cell (polygon of influence) of each point:

.. math::

   z(\mathbf{x}) = z_{k^*}, \qquad k^* = \arg\min_k \lVert \mathbf{x} - \mathbf{p}_k \rVert

In the automated system described by Zelensky and Lysenko (2023), polygons are
built around boreholes inside a block, clipped to the block contour, and the
area of each clipped polygon weights that borehole's thickness and grade in the
block's reserve estimate.

.. code-block:: python

   from pitmap import NearestRegion
   model = NearestRegion().fit(xy, z)
   z_hat = model.predict(grid_xy)

The surface is exact at the survey points and discontinuous between them, which
is fine for reserve accounting and poor for drawing.
