ggviews: A ggplot2-style API for holoviews
===========================================

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

**ggviews** is a Python library that provides a ggplot2-style grammar of graphics API for creating visualizations using holoviews as the backend. It allows you to create beautiful, publication-quality plots using the familiar ggplot2 syntax that R users love.

Quick Start
-----------

.. code-block:: python

   import ggviews as gv
   import pandas as pd

   df = pd.DataFrame({
       'x': [1, 2, 3, 4, 5],
       'y': [2, 5, 3, 8, 7],
       'group': ['A', 'A', 'B', 'B', 'C'],
   })

Method chaining (fluent style):

.. code-block:: python

   (
       gv.ggplot(df, gv.aes(x='x', y='y', color='group'))
       .geom_point(alpha=0.8)
       .theme_minimal()
       .labs(title='My First ggviews Plot')
   )

``+`` operator (ggplot2 style):

.. code-block:: python

   (
       gv.ggplot(df, gv.aes(x='x', y='y', color='group'))
       + gv.geom_point(alpha=0.8)
       + gv.theme_minimal()
       + gv.labs(title='My First ggviews Plot')
   )

Both styles produce identical results. Method chaining reads like a pipeline;
the ``+`` operator mirrors R's ggplot2 syntax.

Key Features
------------

- **Grammar of Graphics**. Build plots layer by layer using the grammar of graphics approach
- **Rich Geom Library**. Points, lines, bars, boxplots, density plots, heatmaps, and more
- **Professional Color Scales**. Viridis, ColorBrewer, and custom color palettes
- **Colorblind-Safe Palette**. ``theme_essi()`` and ``palette_essi()`` based on BCGSC research
- **Statistical Transformations**. Smoothing, density estimation, and statistical summaries
- **Label Repulsion**. ``geom_text_repel()`` and ``geom_label_repel()`` for non-overlapping labels
- **Conditional Highlighting**. ``gghighlight()`` to emphasise subsets of data
- **Flexible Theming**. Fine-grained control over plot appearance
- **Geographic Visualization**. Built-in mapping capabilities with ``geom_map``
- **Notebook Integration**. Works seamlessly in Jupyter notebooks and other environments

Installation
------------

.. code-block:: bash

   pip install ggviews

Contents
--------

.. toctree::
   :maxdepth: 1
   :caption: Documentation

   user_guide/installation
   user_guide/quickstart
   examples/index
   api/core

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
