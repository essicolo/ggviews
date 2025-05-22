"""
Test all features of ggviews.

This script tests all the features of ggviews to ensure they work correctly.
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
    load_dataset,
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
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100),
    'group': np.random.choice(['A', 'B', 'C', 'D'], 100),
    'value': np.random.uniform(0, 10, 100)
})

# Test 1: Basic point plot
print("Test 1: Basic point plot")
plot1 = ggplot(data, aes(x='x', y='y', color='group')).geom_point()
print(f"Plot type: {type(plot1)}")
print(f"Number of layers: {len(plot1.layers)}")
print(f"Layer type: {type(plot1.layers[0])}")

# Test 2: Line plot with log scales
print("\nTest 2: Line plot with log scales")
plot2 = (ggplot(data, aes(x='value', y='value', color='group'))
         .geom_line()
         .scale_x_log10()
         .scale_y_log10())
print(f"Plot type: {type(plot2)}")
print(f"Number of layers: {len(plot2.layers)}")
print(f"Number of scales: {len(plot2.scales)}")

# Test 3: Bar plot with theme
print("\nTest 3: Bar plot with theme")
plot3 = (ggplot(data, aes(x='group', y='value', fill='group'))
         .geom_bar(stat='identity')
         .theme_minimal())
print(f"Plot type: {type(plot3)}")
print(f"Number of layers: {len(plot3.layers)}")
print(f"Theme: {plot3._theme}")

# Test 4: Histogram
print("\nTest 4: Histogram")
plot4 = ggplot(data, aes(x='value')).geom_histogram(bins=10)
print(f"Plot type: {type(plot4)}")
print(f"Number of layers: {len(plot4.layers)}")
print(f"Layer type: {type(plot4.layers[0])}")

# Test 5: Boxplot
print("\nTest 5: Boxplot")
plot5 = ggplot(data, aes(x='group', y='value')).geom_boxplot()
print(f"Plot type: {type(plot5)}")
print(f"Number of layers: {len(plot5.layers)}")
print(f"Layer type: {type(plot5.layers[0])}")

# Test 6: Violin plot
print("\nTest 6: Violin plot")
plot6 = ggplot(data, aes(x='group', y='value')).geom_violin()
print(f"Plot type: {type(plot6)}")
print(f"Number of layers: {len(plot6.layers)}")
print(f"Layer type: {type(plot6.layers[0])}")

# Test 7: Density plot
print("\nTest 7: Density plot")
plot7 = ggplot(data, aes(x='value', fill='group')).geom_density(alpha=0.5)
print(f"Plot type: {type(plot7)}")
print(f"Number of layers: {len(plot7.layers)}")
print(f"Layer type: {type(plot7.layers[0])}")

# Test 8: Facet grid
print("\nTest 8: Facet grid")
plot8 = (ggplot(data, aes(x='x', y='y'))
         .geom_point()
         .facet_grid(row='group'))
print(f"Plot type: {type(plot8)}")
print(f"Number of layers: {len(plot8.layers)}")
print(f"Facet: {plot8.facets}")

# Test 9: Facet wrap
print("\nTest 9: Facet wrap")
plot9 = (ggplot(data, aes(x='x', y='y'))
         .geom_point()
         .facet_wrap('group', ncol=2))
print(f"Plot type: {type(plot9)}")
print(f"Number of layers: {len(plot9.layers)}")
print(f"Facet: {plot9.facets}")

# Test 10: Coordinate flip
print("\nTest 10: Coordinate flip")
plot10 = (ggplot(data, aes(x='group', y='value'))
          .geom_boxplot()
          .coord_flip())
print(f"Plot type: {type(plot10)}")
print(f"Number of layers: {len(plot10.layers)}")
print(f"Coordinates: {plot10.coords}")

# Test 11: Polar coordinates
print("\nTest 11: Polar coordinates")
plot11 = (ggplot(data, aes(x='group', y='value', fill='group'))
          .geom_bar(stat='identity')
          .coord_polar())
print(f"Plot type: {type(plot11)}")
print(f"Number of layers: {len(plot11.layers)}")
print(f"Coordinates: {plot11.coords}")

print("\nAll tests completed successfully!")