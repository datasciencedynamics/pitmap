Welcome to the pitmap documentation
===================================

.. note::

   This documentation is for pitmap version |release| (pre-alpha). The API will change.

``pitmap`` builds surfaces from scattered survey points for open-pit mine
surveying. It is a Python implementation of the surface-construction methods
used in the automated geological and mine-surveying support system developed at
the State University of Economics and Technology (Kryvyi Rih, Ukraine), with a
kernel-based interpolator added for comparison. Every interpolator shares one
``fit`` / ``predict`` interface.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting_started

.. toctree::
   :maxdepth: 2
   :caption: Methods

   methods/nearest_region
   methods/sector_idw

.. toctree::
   :maxdepth: 2
   :caption: Classes, Attributes, & Methods

   api/interpolation

.. toctree::
   :maxdepth: 1
   :caption: About pitmap

   about/contributors
   about/changelog
   about/references
