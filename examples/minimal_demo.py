"""
Minimal demonstration of ggviews features.

This script creates a simple scatter plot to demonstrate the features of ggviews.
"""
import pandas as pd
import numpy as np
import holoviews as hv

# Initialize holoviews extension
hv.extension('bokeh')

# Import from ggviews
from ggviews import ggplot, aes, geom_point, theme_minimal

# Create a sample dataset
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'x': np.random.normal(0, 1, n),
    'y': np.random.normal(0, 1, n),
    'category': np.random.choice(['A', 'B', 'C', 'D'], n)
})

# Create a scatter plot
scatter_plot = (ggplot(data, aes(x='x', y='y', color='category'))
                .geom_point(size=5, alpha=0.7)
                .theme_minimal())

# Build the plot
print("Building plot...")
scatter_element = scatter_plot.build()
print("Plot built successfully!")
print(f"Plot type: {type(scatter_element)}")

# Display the plot (this will only work in a notebook environment)
# scatter_element