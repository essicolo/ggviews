# %% [markdown]
# # ggviews Comprehensive Examples
#
# This notebook demonstrates the full capabilities of ggviews, a ggplot2-style
# grammar of graphics library for Python built on holoviews.

# %% [markdown]
# ## Setup and Data Preparation

# %%
import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import *

# Set up holoviews backend
hv.extension('bokeh')

# Create comprehensive example datasets
np.random.seed(42)

# Dataset 1: Statistical analysis data
n = 200
stats_data = pd.DataFrame({
    'treatment': np.repeat(['Control', 'Drug A', 'Drug B', 'Drug C'], n//4),
    'response': np.concatenate([
        np.random.normal(50, 10, n//4),   # Control
        np.random.normal(65, 12, n//4),   # Drug A
        np.random.normal(75, 8, n//4),    # Drug B  
        np.random.normal(60, 15, n//4)    # Drug C
    ]),
    'age': np.random.uniform(18, 80, n),
    'gender': np.random.choice(['Male', 'Female'], n),
    'baseline': np.random.normal(45, 8, n)
})

# Dataset 2: Time series data
dates = pd.date_range('2020-01-01', periods=100, freq='D')
ts_data = pd.DataFrame({
    'date': np.tile(dates, 3),
    'value': np.concatenate([
        np.cumsum(np.random.randn(100)) + 100,  # Stock A
        np.cumsum(np.random.randn(100)) + 150,  # Stock B  
        np.cumsum(np.random.randn(100)) + 200   # Stock C
    ]),
    'stock': np.repeat(['AAPL', 'GOOGL', 'MSFT'], 100),
    'volume': np.random.uniform(1000, 10000, 300)
})

# Dataset 3: Geographic data
cities = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Sydney', 'São Paulo', 'Mumbai'],
    'longitude': [-74.0, -0.1, 139.7, 151.2, -46.6, 72.8],
    'latitude': [40.7, 51.5, 35.7, -33.9, -23.5, 19.1],
    'population': [8.4, 9.0, 13.9, 5.3, 12.3, 20.0],
    'continent': ['N. America', 'Europe', 'Asia', 'Oceania', 'S. America', 'Asia']
})

# Dataset 4: Heatmap data
x_vals = np.repeat(range(10), 10)
y_vals = np.tile(range(10), 10)
heatmap_data = pd.DataFrame({
    'x': x_vals,
    'y': y_vals,
    'temperature': np.sin(x_vals/2) * np.cos(y_vals/2) * 10 + np.random.normal(0, 2, 100),
    'category': np.random.choice(['Low', 'Medium', 'High'], 100)
})

print("📊 Example datasets created successfully!")

# %% [markdown]
# ## 1. Basic Aesthetics and Geoms
#
# The foundation of ggviews is the aesthetic mapping system that connects 
# data variables to visual properties.

# %%
# Basic scatter plot with color aesthetic
basic_scatter = (
    ggplot(stats_data, aes(x='age', y='response', color='treatment'))
    .geom_point(size=6, alpha=0.8)
    .labs(
        title='Treatment Response by Age',
        subtitle='Basic aesthetic mapping demonstration',
        x='Age (years)',
        y='Response Score',
        color='Treatment'
    )
)

basic_scatter.show()

# %% [markdown]
# ### Size and Shape Aesthetics

# %%
# Multiple aesthetics: color, size, and transparency
multi_aesthetic = (
    ggplot(stats_data, aes(x='age', y='response', color='treatment', size='baseline'))
    .geom_point(alpha=0.7)
    .scale_colour_brewer(palette='Set1')
    .labs(
        title='Multi-Aesthetic Mapping',
        subtitle='Color by treatment, size by baseline score',
        size='Baseline Score'
    )
)

multi_aesthetic.show()

# %% [markdown]
# ## 2. Statistical Visualizations
#
# ggviews provides comprehensive statistical geoms for data analysis.

# %% [markdown]
# ### Box Plots for Distribution Analysis

# %%
# Box plots showing treatment effect distributions
treatment_boxplot = (
    ggplot(stats_data, aes(x='treatment', y='response', fill='treatment'))
    .geom_boxplot(width=0.7, alpha=0.8)
    .scale_fill_brewer(palette='Set2')
    .coord_flip()
    .theme_minimal()
    .labs(
        title='Treatment Response Distributions',
        subtitle='Horizontal box plots with ColorBrewer palette',
        x='Treatment Group',
        y='Response Score',
        fill='Treatment'
    )
)

treatment_boxplot.show()

# %% [markdown]
# ### Density Plots for Smooth Distributions

# %%
# Overlapping density curves by treatment
density_comparison = (
    ggplot(stats_data, aes(x='response', fill='treatment'))
    .geom_density(alpha=0.6)
    .scale_fill_viridis_d()
    .theme_minimal()
    .labs(
        title='Treatment Response Densities',
        subtitle='Kernel density estimation with viridis colors',
        x='Response Score',
        y='Density',
        fill='Treatment'
    )
)

density_comparison.show()

# %% [markdown]
# ### Smoothed Trend Lines

# %%
# Scatter plot with trend lines by group
trend_analysis = (
    ggplot(stats_data, aes(x='age', y='response', color='gender'))
    .geom_point(alpha=0.5, size=4)
    .geom_smooth(method='lm', se=False, size=2)
    .scale_colour_brewer(palette='Dark2')
    .theme_classic()
    .labs(
        title='Age vs Response by Gender',
        subtitle='Linear trends with confidence intervals',
        x='Age (years)',
        y='Response Score',
        color='Gender'
    )
)

trend_analysis.show()

# %% [markdown]
# ## 3. Advanced Theming and Customization
#
# ggviews provides fine-grained control over plot appearance using theme elements.

# %%
# Publication-ready plot with custom theme
publication_plot = (
    ggplot(stats_data, aes(x='treatment', y='response'))
    .geom_boxplot(aes(fill='treatment'), alpha=0.7)
    .geom_point(position=position_jitter(width=0.2), alpha=0.4, size=2)
    .scale_fill_brewer(palette='Blues')
    .theme(
        panel_grid_minor=element_blank(),
        axis_text_x=element_text(angle=45, hjust=1, size=12),
        plot_title=element_text(size=16, color='darkblue'),
        legend_position='bottom',
        panel_background=element_rect(fill='white')
    )
    .labs(
        title='Treatment Efficacy Analysis',
        subtitle='Box plots with individual data points',
        x='Treatment Group',
        y='Response Score (higher is better)',
        fill='Treatment',
        caption='Data: Clinical trial results (n=200)'
    )
)

publication_plot.show()

# %% [markdown]
# ## 4. Faceting for Multi-Panel Plots
#
# Create multiple related plots to explore different aspects of your data.

# %%
# Faceted scatter plots by treatment and gender
faceted_analysis = (
    ggplot(stats_data, aes(x='age', y='response', color='gender'))
    .geom_point(alpha=0.7, size=3)
    .geom_smooth(method='lm', se=False)
    .facet_wrap('~treatment', scales='free')
    .scale_colour_brewer(palette='Set1')
    .theme_minimal()
    .labs(
        title='Age-Response Relationship by Treatment',
        subtitle='Separate panels for each treatment group',
        x='Age (years)',
        y='Response Score',
        color='Gender'
    )
)

faceted_analysis.show()

# %% [markdown]
# ### Grid-based Faceting

# %%
# 2D grid of facets
grid_facets = (
    ggplot(stats_data, aes(x='age', y='response'))
    .geom_point(alpha=0.6, size=2)
    .geom_smooth(method='lm', color='red', alpha=0.7)
    .facet_grid('gender ~ treatment')
    .theme_bw()
    .labs(
        title='Treatment Response by Age, Gender, and Treatment',
        subtitle='2D facet grid showing all combinations',
        x='Age (years)',
        y='Response Score'
    )
)

grid_facets.show()

# %% [markdown]
# ## 5. Time Series and Line Plots

# %%
# Multi-series time plot
time_series = (
    ggplot(ts_data, aes(x='date', y='value', color='stock'))
    .geom_line(size=2, alpha=0.8)
    .scale_colour_brewer(palette='Set1')
    .theme_minimal()
    .labs(
        title='Stock Price Performance',
        subtitle='Daily closing prices over time',
        x='Date',
        y='Price ($)',
        color='Stock'
    )
)

time_series.show()

# %% [markdown]
# ## 6. 2D Visualizations and Heatmaps

# %%
# Temperature heatmap with continuous color scale
temperature_heatmap = (
    ggplot(heatmap_data, aes(x='x', y='y', fill='temperature'))
    .geom_tile()
    .scale_fill_viridis_c(option='plasma')
    .theme_void()
    .labs(
        title='Temperature Distribution',
        subtitle='2D spatial temperature data',
        fill='Temperature (°C)'
    )
)

temperature_heatmap.show()

# %% [markdown]
# ### Categorical Heatmap

# %%
# Categorical tile plot
categorical_heatmap = (
    ggplot(heatmap_data, aes(x='x', y='y', fill='category'))
    .geom_tile(alpha=0.8)
    .scale_fill_brewer(palette='Set3')
    .theme_minimal()
    .labs(
        title='Categorical Spatial Data',
        subtitle='Discrete categories across 2D space',
        x='X Coordinate',
        y='Y Coordinate',
        fill='Category'
    )
)

categorical_heatmap.show()

# %% [markdown]
# ## 7. Geographic Visualizations

# %%
# World cities map
cities_map = (
    ggplot(cities, aes(x='longitude', y='latitude', size='population', color='continent'))
    .geom_map(map_type='simple', alpha=0.8)
    .scale_colour_brewer(palette='Set2')
    .theme_minimal()
    .labs(
        title='Major World Cities',
        subtitle='Population and location by continent',
        x='Longitude',
        y='Latitude',
        size='Population (millions)',
        color='Continent'
    )
)

cities_map.show()

# %% [markdown]
# ## 8. Bar Charts and Categorical Data

# %%
# Grouped bar chart with position dodge
treatment_summary = stats_data.groupby(['treatment', 'gender'])['response'].mean().reset_index()

grouped_bars = (
    ggplot(treatment_summary, aes(x='treatment', y='response', fill='gender'))
    .geom_bar(stat='identity', position=position_dodge(width=0.8), alpha=0.8)
    .scale_fill_brewer(palette='Pastel1')
    .theme_classic()
    .labs(
        title='Average Response by Treatment and Gender',
        subtitle='Side-by-side comparison using position_dodge',
        x='Treatment Group',
        y='Average Response Score',
        fill='Gender'
    )
)

grouped_bars.show()

# %% [markdown]
# ## 9. Statistical Summaries and Error Bars

# %%
# Calculate summary statistics
treatment_stats = (stats_data.groupby('treatment')['response']
                  .agg(['mean', 'std', 'count'])
                  .reset_index())
treatment_stats['se'] = treatment_stats['std'] / np.sqrt(treatment_stats['count'])

# Bar chart with error bars
error_bars_plot = (
    ggplot(treatment_stats, aes(x='treatment', y='mean'))
    .geom_bar(stat='identity', fill='steelblue', alpha=0.7)
    .geom_errorbar(aes(ymin='mean-se', ymax='mean+se'), width=0.3, color='black')
    .theme_minimal()
    .labs(
        title='Treatment Effects with Standard Errors',
        subtitle='Mean response ± standard error',
        x='Treatment Group',
        y='Mean Response Score'
    )
)

error_bars_plot.show()

# %% [markdown]
# ## 10. Advanced Color Scales and Palettes

# %%
# Showcase different color palettes
palette_demo = (
    ggplot(stats_data, aes(x='age', y='response', color='treatment'))
    .geom_point(size=6, alpha=0.8)
    .scale_colour_brewer(palette='Spectral')
    .theme_dark()
    .labs(
        title='ColorBrewer Spectral Palette',
        subtitle='Diverging color scale on dark theme',
        x='Age (years)',
        y='Response Score',
        color='Treatment'
    )
)

palette_demo.show()

# %% [markdown]
# ## 11. Complex Multi-Layer Visualizations

# %%
# Complex plot combining multiple geoms and aesthetics
complex_plot = (
    ggplot(stats_data, aes(x='age', y='response'))
    .geom_point(aes(color='treatment', size='baseline'), alpha=0.6)
    .geom_smooth(method='lm', color='black', alpha=0.8, se=True)
    .scale_colour_viridis_d(option='plasma')
    .facet_wrap('~gender')
    .theme(
        panel_grid_minor=element_blank(),
        strip_text=element_text(size=12, color='darkblue'),
        legend_position='bottom'
    )
    .labs(
        title='Comprehensive Multi-Layer Analysis',
        subtitle='Points (treatment + baseline) + smooth trend + facets by gender',
        x='Age (years)',
        y='Response Score',
        color='Treatment',
        size='Baseline',
        caption='Demonstrates advanced ggviews capabilities'
    )
)

complex_plot.show()

# %% [markdown]
# ## Summary
#
# This comprehensive example demonstrates ggviews' capabilities across all major
# areas of data visualization:
#
# - **Aesthetic Mappings**: Color, size, fill, and other visual properties
# - **Statistical Geoms**: Box plots, density plots, smoothing, error bars  
# - **Theming**: Fine-grained control over plot appearance
# - **Faceting**: Multi-panel plots for exploring subgroups
# - **Color Scales**: Viridis, ColorBrewer, and custom palettes
# - **Geographic Visualization**: Mapping capabilities
# - **2D Visualization**: Heatmaps and tile plots
# - **Complex Layering**: Multiple geoms and aesthetics combined
#
# ggviews provides a comprehensive, ggplot2-compatible grammar of graphics
# for Python, enabling publication-quality visualizations with readable,
# expressive code.

# %%