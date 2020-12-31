.. datablend documentation master file, created by
   sphinx-quickstart on Mon Dec 28 14:23:04 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. numbered
.. caption
.. name
.. titlesonly
.. glob
.. reversed
.. hidden
.. includehidden

.. note
.. warning
.. versionadded
.. versionchanged
.. d

Welcome to DataBlend's documentation!
=====================================

The ``DataBlend`` python library allows to format manually collected data
into other useful data structures such as (i) **Stacked data** frequently
used in databases and (ii) **Tidy data** often required when using AI/ML
libraries.

The origin of this project comes from the need of cleaning and merging
different clinical data sets that were manually collected using Microsoft
Excel.

The code of the project is on Github: Link

.. toctree::
   :maxdepth: 2
   :caption: Using DataBlend
   :hidden:

   usage/installation
   usage/quickstart
   usage/widgets
   usage/tips
   usage/configuration

.. toctree::
   :maxdepth: 2
   :caption: Advanced Usage and Information
   :hidden:

   usage/advanced

.. toctree::
   :maxdepth: 2
   :caption: Example Galleries
   :hidden:

   _examples/widgets/index
   _examples/blender/index
   _examples/template/index

.. automodule:: datablend.core.blend
   :members:
   :hidden:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
