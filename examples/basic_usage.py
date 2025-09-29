"""
Basic usage examples for ggviews

This script demonstrates the basic functionality of ggviews
with simple examples similar to ggplot2.
"""

import pandas as pd
import numpy as np
from ggviews import ggplot, aes
from ggviews.geoms import geom_point, geom_line, geom_bar, geom_histogram
from ggviews.themes import theme_minimal, theme_classic
from ggviews.scales import scale_color_manual
from ggviews.facets import facet_wrap

# Create sample data
np.random.seed(42)
n = 100

df = pd.DataFrame({
    'x': np.random.randn(n),
    'y': 2 * np.random.randn(n) + 1,
    'category': np.random.choice(['A', 'B', 'C'], n),
    'size_var': np.random.uniform(1, 5, n),
    'color_var': np.random.uniform(0, 10, n)
})

print("Sample data:")
print(df.head())
print(f"Data shape: {df.shape}")

# Example 1: Basic scatter plot
print("\n=== Example 1: Basic Scatter Plot ===")
p1 = ggplot(df, aes(x='x', y='y')) + geom_point()
print("Created basic scatter plot")

# Example 2: Colored scatter plot
print("\n=== Example 2: Colored Scatter Plot ===")
p2 = (ggplot(df, aes(x='x', y='y', color='category'))
      + geom_point(size=4, alpha=0.7)
      + theme_minimal()
      + labs(title='Scatter Plot by Category', 
             x='X Variable', 
             y='Y Variable',
             color='Category'))
print("Created colored scatter plot with theme")

# Example 3: Line plot with smoothing
print("\n=== Example 3: Line Plot with Smoothing ===")
# Create time series data
time_df = pd.DataFrame({
    'time': range(50),
    'value': np.cumsum(np.random.randn(50)) + np.sin(np.arange(50) * 0.1) * 5,
    'group': np.repeat(['Group1', 'Group2'], 25)
})

p3 = (ggplot(time_df, aes(x='time', y='value', color='group'))
      + geom_line(size=2)
      + geom_smooth(method='lm', se=False)
      + theme_classic()
      + labs(title='Time Series with Trend Lines'))
print("Created line plot with smoothing")

# Example 4: Bar chart
print("\n=== Example 4: Bar Chart ===")
category_counts = df['category'].value_counts().reset_index()
category_counts.columns = ['category', 'count']

p4 = (ggplot(category_counts, aes(x='category', y='count'))
      + geom_bar(stat='identity', fill='steelblue', alpha=0.7)
      + theme_minimal()
      + labs(title='Category Counts', 
             x='Category', 
             y='Count'))
print("Created bar chart")

# Example 5: Histogram
print("\n=== Example 5: Histogram ===")
p5 = (ggplot(df, aes(x='x'))
      + geom_histogram(bins=20, fill='lightblue', alpha=0.7)
      + theme_minimal()
      + labs(title='Distribution of X Variable',
             x='X Variable',
             y='Frequency'))
print("Created histogram")

# Example 6: Faceted plot
print("\n=== Example 6: Faceted Plot ===")
p6 = (ggplot(df, aes(x='x', y='y'))
      + geom_point(alpha=0.6)
      + facet_wrap('~category')
      + theme_minimal()
      + labs(title='Scatter Plot by Category (Faceted)'))
print("Created faceted plot")

# Example 7: Custom colors
print("\n=== Example 7: Custom Colors ===")
custom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
p7 = (ggplot(df, aes(x='x', y='y', color='category'))
      + geom_point(size=4, alpha=0.8)
      + scale_color_manual(values=custom_colors)
      + theme_minimal()
      + labs(title='Custom Color Palette'))
print("Created plot with custom colors")

# Example 8: Method chaining demonstration
print("\n=== Example 8: Method Chaining ===")
p8 = (ggplot(df)
      .geom_point(aes(x='x', y='y', size='size_var', color='color_var'), alpha=0.7)
      .theme_minimal()
      .labs(title='Multiple Aesthetics',
            x='X Variable', 
            y='Y Variable',
            size='Size Variable',
            color='Color Variable')
      .xlim(-3, 3)
      .ylim(-5, 5))
print("Created plot using method chaining")

print("\n=== All Examples Created Successfully! ===")
print("\nTo display plots in Jupyter notebook, use:")
print("p1.show()  # or just p1 in Jupyter")
print("\nNote: Install holoviews extensions for interactivity:")
print("hv.extension('bokeh')  # for Bokeh backend")
print("hv.extension('matplotlib')  # for matplotlib backend")