"""
Demonstration of new features in ggviews.

This script demonstrates the new features added to ggviews.
"""
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import (
    ggplot, 
    aes, 
    load_dataset,
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
    coord_flip
)

# Initialize holoviews extension
hv.extension('bokeh')

# Load a dataset
diamonds = load_dataset('diamonds')

# Basic scatter plot with color
plot1 = (ggplot(diamonds, aes(x='carat', y='price', color='cut'))
         .geom_point(alpha=0.5)
         .labs(title='Diamond Prices by Carat and Cut')
         .theme_minimal())

# Save the plot
plot1.save('diamond_scatter.html')

# Boxplot with coordinate flip
plot2 = (ggplot(diamonds, aes(x='cut', y='price'))
         .geom_boxplot(fill='skyblue')
         .labs(title='Diamond Prices by Cut', x='Cut', y='Price')
         .coord_flip()
         .theme_bw())

# Save the plot
plot2.save('diamond_boxplot_flipped.html')

# Violin plot with facets
plot3 = (ggplot(diamonds, aes(x='cut', y='price', fill='cut'))
         .geom_violin()
         .facet_wrap('color')
         .labs(title='Diamond Prices by Cut and Color')
         .scale_fill_discrete(palette='Category20')
         .theme_minimal())

# Save the plot
plot3.save('diamond_violin_facets.html')

# Density plot with continuous color scale
plot4 = (ggplot(diamonds, aes(x='carat', fill='price'))
         .geom_density(alpha=0.7)
         .scale_fill_continuous(palette='viridis')
         .labs(title='Distribution of Diamond Carats by Price')
         .theme_minimal())

# Save the plot
plot4.save('diamond_density.html')

print("Plots saved to current directory.")