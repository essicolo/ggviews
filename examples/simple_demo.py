"""
Simple demonstration of ggviews features.

This script creates several plots to demonstrate the features of ggviews.
"""
import pandas as pd
import numpy as np
import holoviews as hv

# Initialize holoviews extension
hv.extension('bokeh')

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
    theme_minimal
)

# Create a sample dataset
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'x': np.random.normal(0, 1, n),
    'y': np.random.normal(0, 1, n),
    'category': np.random.choice(['A', 'B', 'C', 'D'], n),
    'value': np.random.uniform(1, 10, n)
})

# 1. Basic scatter plot with color
scatter_plot = (ggplot(data, aes(x='x', y='y', color='category'))
                .geom_point(size=5, alpha=0.7)
                .theme_minimal())

# 2. Bar plot
bar_plot = (ggplot(data, aes(x='category', y='value'))
            .geom_bar(stat='identity', position='dodge')
            .theme_minimal())

# 3. Histogram
histogram = (ggplot(data, aes(x='value'))
             .geom_histogram(bins=20)
             .theme_minimal())

# 4. Box plot
box_plot = (ggplot(data, aes(x='category', y='value'))
            .geom_boxplot()
            .theme_minimal())

# 5. Violin plot
violin_plot = (ggplot(data, aes(x='category', y='value'))
               .geom_violin()
               .theme_minimal())

# Display the plots
print("Building plots...")

# Build the plots
scatter_element = scatter_plot.build()
bar_element = bar_plot.build()
histogram_element = histogram.build()
box_element = box_plot.build()
violin_element = violin_plot.build()

print("Plots built successfully!")

# Print information about the plots
print(f"Scatter plot type: {type(scatter_element)}")
print(f"Bar plot type: {type(bar_element)}")
print(f"Histogram type: {type(histogram_element)}")
print(f"Box plot type: {type(box_element)}")
print(f"Violin plot type: {type(violin_element)}")

print("Demo completed successfully!")