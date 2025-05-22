"""
Visual demonstration of ggviews features.

This script creates several plots to demonstrate the features of ggviews.
"""
import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts

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

# Set default options for all plots
hv.opts.defaults(
    opts.Scatter(width=400, height=400, size=8),
    opts.Curve(width=400, height=400, line_width=2),
    opts.Bars(width=400, height=400),
    opts.BoxWhisker(width=400, height=400),
    opts.Violin(width=400, height=400),
    opts.Area(width=400, height=400),
)

# Create a sample dataset
np.random.seed(42)
n = 200
data = pd.DataFrame({
    'x': np.random.normal(0, 1, n),
    'y': np.random.normal(0, 1, n),
    'category': np.random.choice(['A', 'B', 'C', 'D'], n),
    'value': np.random.uniform(1, 10, n),
    'group': np.random.choice(['Group 1', 'Group 2'], n)
})

# Create a more complex dataset for demonstrating facets
diamonds = pd.DataFrame({
    'carat': np.random.uniform(0.2, 5.0, n),
    'cut': np.random.choice(['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'], n),
    'color': np.random.choice(['D', 'E', 'F', 'G', 'H', 'I', 'J'], n),
    'clarity': np.random.choice(['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'], n),
    'depth': np.random.uniform(55, 70, n),
    'table': np.random.uniform(50, 80, n),
    'price': np.random.uniform(300, 20000, n),
    'x': np.random.uniform(3, 10, n),
    'y': np.random.uniform(3, 10, n),
    'z': np.random.uniform(2, 7, n)
})

# 1. Basic scatter plot with color
scatter_plot = (ggplot(data, aes(x='x', y='y', color='category'))
                .geom_point(size=5, alpha=0.7)
                .theme_minimal())

# 2. Scatter plot with size mapping
scatter_size = (ggplot(data, aes(x='x', y='y', color='category', size='value'))
                .geom_point(alpha=0.7)
                .theme_minimal())

# 3. Bar plot
bar_plot = (ggplot(data, aes(x='category', y='value', fill='category'))
            .geom_bar(stat='identity', position='dodge')
            .theme_minimal())

# 4. Histogram
histogram = (ggplot(data, aes(x='value', fill='category'))
             .geom_histogram(bins=20, alpha=0.7)
             .theme_minimal())

# 5. Box plot
box_plot = (ggplot(data, aes(x='category', y='value', fill='category'))
            .geom_boxplot()
            .theme_minimal())

# 6. Violin plot
violin_plot = (ggplot(data, aes(x='category', y='value', fill='category'))
               .geom_violin()
               .theme_minimal())

# 7. Density plot
density_plot = (ggplot(data, aes(x='value', fill='category'))
                .geom_density(alpha=0.5)
                .theme_minimal())

# 8. Facet grid
facet_grid_plot = (ggplot(diamonds, aes(x='carat', y='price', color='cut'))
                   .geom_point(alpha=0.7)
                   .facet_grid(row='color', col='clarity')
                   .theme_minimal())

# 9. Facet wrap
facet_wrap_plot = (ggplot(diamonds, aes(x='carat', y='price', color='cut'))
                   .geom_point(alpha=0.7)
                   .facet_wrap('color', ncol=3)
                   .theme_minimal())

# 10. Coordinate flip
coord_flip_plot = (ggplot(data, aes(x='category', y='value', fill='category'))
                   .geom_boxplot()
                   .coord_flip()
                   .theme_minimal())

# 11. Polar coordinates
polar_plot = (ggplot(data, aes(x='category', y='value', fill='category'))
              .geom_bar(stat='identity')
              .coord_polar()
              .theme_minimal())

# 12. Combined features
combined_plot = (ggplot(diamonds, aes(x='carat', y='price', color='cut'))
                 .geom_point(alpha=0.7)
                 .scale_y_log10()
                 .facet_wrap('color', ncol=3)
                 .theme_minimal())

# Display the plots
print("Displaying plots...")

# Save the plots to HTML files
hv.save(scatter_plot.build(), 'scatter_plot.html')
hv.save(scatter_size.build(), 'scatter_size.html')
hv.save(bar_plot.build(), 'bar_plot.html')
hv.save(histogram.build(), 'histogram.html')
hv.save(box_plot.build(), 'box_plot.html')
hv.save(violin_plot.build(), 'violin_plot.html')
hv.save(density_plot.build(), 'density_plot.html')
hv.save(coord_flip_plot.build(), 'coord_flip_plot.html')
hv.save(polar_plot.build(), 'polar_plot.html')
hv.save(combined_plot.build(), 'combined_plot.html')

print("Plots saved to HTML files.")

# Create a layout of all plots for display
layout = (scatter_plot.build() + scatter_size.build() + bar_plot.build() + 
          histogram.build() + box_plot.build() + violin_plot.build() + 
          density_plot.build() + coord_flip_plot.build() + polar_plot.build())

# Save the layout to an HTML file
hv.save(layout, 'all_plots.html')

print("All plots saved to all_plots.html")