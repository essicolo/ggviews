Examples Gallery
================

This section provides comprehensive examples of ggviews functionality.

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

   from ggviews import ggplot, aes
   import pandas as pd
   
   df = pd.DataFrame({
       'x': [1, 2, 3, 4, 5],
       'y': [2, 5, 3, 8, 7],
       'group': ['A', 'A', 'B', 'B', 'C']
   })
   
   plot = (ggplot(df, aes(x='x', y='y', color='group'))
          .geom_point(size=8)
          .theme_minimal())

Box Plot with Custom Colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot = (ggplot(df, aes(x='group', y='value', fill='group'))
          .geom_boxplot(alpha=0.7)
          .scale_fill_brewer(palette='Set2')
          .coord_flip()
          .labs(title='Distribution by Group'))

Heatmap Visualization
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot = (ggplot(heatmap_df, aes(x='x', y='y', fill='temperature'))
          .geom_tile()
          .scale_fill_viridis_c()
          .theme_void()
          .labs(title='Temperature Map'))

Advanced Multi-Layer Plot
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot = (ggplot(df, aes(x='age', y='score'))
          .geom_point(aes(color='group', size='weight'), alpha=0.7)
          .geom_smooth(method='lm', color='black')
          .facet_wrap('~category')
          .scale_colour_brewer(palette='Set1')
          .theme_minimal()
          .labs(title='Complex Analysis'))