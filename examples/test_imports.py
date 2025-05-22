"""
Test imports for ggviews.

This script tests the imports for ggviews to ensure they work correctly.
"""
import pandas as pd
import numpy as np

# Import from ggviews
from ggviews import (
    ggplot, 
    aes, 
    geom_point,
    geom_line,
    geom_bar,
    geom_histogram,
    geom_boxplot,
    geom_violin,
    geom_density,
    scale_x_log10,
    scale_y_log10,
    scale_color_continuous,
    scale_fill_continuous,
    scale_color_discrete,
    scale_fill_discrete,
    theme_default,
    theme_minimal,
    theme_bw,
    facet_grid,
    facet_wrap,
    coord_flip,
    coord_polar
)

# Create a simple dataframe
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 4, 9, 16, 25],
    'group': ['A', 'B', 'C', 'D', 'E']
})

# Create a basic plot
plot = ggplot(data, aes(x='x', y='y', color='group'))

# Add a point layer
plot = plot.geom_point()

# Display the plot
print("Plot created successfully!")
print(f"Plot type: {type(plot)}")
print(f"Number of layers: {len(plot.layers)}")
print(f"Layer type: {type(plot.layers[0])}")