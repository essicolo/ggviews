Examples Gallery
================

This section provides comprehensive examples of ggviews functionality.

All examples use the recommended alias:

.. code-block:: python

   import ggviews as gv

.. toctree::
   :maxdepth: 2

   comprehensive_examples
   basic_plots
   aesthetics_guide
   theming_guide
   statistical_plots
   faceting_examples
   geographic_maps

Quick Examples
--------------

Basic Scatter Plot
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   (
       gv.ggplot(df, gv.aes(x='x', y='y', color='group'))
       .geom_point(alpha=0.8)
       .theme_minimal()
   )

Or, equivalently, with the ``+`` operator:

.. code-block:: python

   (
       gv.ggplot(df, gv.aes(x='x', y='y', color='group'))
       + gv.geom_point(alpha=0.8)
       + gv.theme_minimal()
   )

Box Plot with Custom Colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   (
       gv.ggplot(df, gv.aes(x='group', y='value', fill='group'))
       .geom_boxplot(alpha=0.7)
       .scale_fill_brewer(palette='Set2')
       .coord_flip()
       .labs(title='Distribution by Group')
   )

Heatmap Visualization
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   (
       gv.ggplot(heatmap_df, gv.aes(x='x', y='y', fill='temperature'))
       .geom_tile()
       .scale_fill_viridis_c()
       .theme_void()
       .labs(title='Temperature Map')
   )

Highlighted Subset
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   (
       gv.ggplot(df, gv.aes(x='x', y='y'))
       .geom_point()
       .gghighlight("group == 'A'")
       .labs(title='Group A Highlighted')
   )

Advanced Multi-Layer Plot
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   (
       gv.ggplot(df, gv.aes(x='age', y='score'))
       .geom_point(gv.aes(color='group', size='weight'), alpha=0.7)
       .geom_smooth(method='lm', color='black')
       .facet_wrap('~category')
       .scale_colour_brewer(palette='Set1')
       .theme_essi()
       .labs(title='Complex Analysis')
   )
