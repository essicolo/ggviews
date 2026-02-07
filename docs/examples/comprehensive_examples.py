# %% [markdown]
# # ggviews Comprehensive Examples
#
# This notebook demonstrates the full capabilities of ggviews, a ggplot2-style
# grammar of graphics library for Python built on holoviews.
#
# ggviews supports two equivalent syntaxes:
#
# - **Method chaining** (fluent style): `.geom_point().theme_minimal()`
# - **`+` operator** (ggplot2 style): `+ gv.geom_point() + gv.theme_minimal()`
#
# This file uses method chaining throughout.  To switch any example to
# the `+` operator style, replace `.geom_xxx(...)` with `+ gv.geom_xxx(...)`
# and so on.

# %% [markdown]
# ## Setup and Data Preparation

# %%
import pandas as pd
import numpy as np
import holoviews as hv
import ggviews as gv

# Set up holoviews backend
hv.extension('bokeh')

# Create comprehensive example datasets
np.random.seed(42)

# Dataset 1: Statistical analysis data
n = 200
stats_data = pd.DataFrame({
    'treatment': np.repeat(['Control', 'Drug A', 'Drug B', 'Drug C'], n // 4),
    'response': np.concatenate([
        np.random.normal(50, 10, n // 4),   # Control
        np.random.normal(65, 12, n // 4),   # Drug A
        np.random.normal(75, 8, n // 4),    # Drug B
        np.random.normal(60, 15, n // 4),   # Drug C
    ]),
    'age': np.random.uniform(18, 80, n),
    'gender': np.random.choice(['Male', 'Female'], n),
    'baseline': np.random.normal(45, 8, n),
})

# Dataset 2: Time series data
dates = pd.date_range('2020-01-01', periods=100, freq='D')
ts_data = pd.DataFrame({
    'date': np.tile(dates, 3),
    'value': np.concatenate([
        np.cumsum(np.random.randn(100)) + 100,
        np.cumsum(np.random.randn(100)) + 150,
        np.cumsum(np.random.randn(100)) + 200,
    ]),
    'stock': np.repeat(['AAPL', 'GOOGL', 'MSFT'], 100),
    'volume': np.random.uniform(1000, 10000, 300),
})

# Dataset 3: Geographic data
cities = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Sydney', 'São Paulo', 'Mumbai'],
    'longitude': [-74.0, -0.1, 139.7, 151.2, -46.6, 72.8],
    'latitude': [40.7, 51.5, 35.7, -33.9, -23.5, 19.1],
    'population': [8.4, 9.0, 13.9, 5.3, 12.3, 20.0],
    'continent': ['N. America', 'Europe', 'Asia', 'Oceania', 'S. America', 'Asia'],
})

# Dataset 4: Heatmap data
x_vals = np.repeat(range(10), 10)
y_vals = np.tile(range(10), 10)
heatmap_data = pd.DataFrame({
    'x': x_vals,
    'y': y_vals,
    'temperature': np.sin(x_vals / 2) * np.cos(y_vals / 2) * 10
                   + np.random.normal(0, 2, 100),
    'category': np.random.choice(['Low', 'Medium', 'High'], 100),
})

print("Example datasets created successfully!")

# %% [markdown]
# ## 1. Basic Aesthetics and Geoms
#
# The foundation of ggviews is the aesthetic mapping system that connects
# data variables to visual properties.

# %%
# Basic scatter plot with color aesthetic
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response', color='treatment'))
    .geom_point(alpha=0.8)
    .labs(
        title='Treatment Response by Age',
        x='Age (years)',
        y='Response Score',
        color='Treatment',
    )
).show()

# %% [markdown]
# ### Size and Shape Aesthetics

# %%
# Multiple aesthetics: color, size, and transparency
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response', color='treatment', size='baseline'))
    .geom_point(alpha=0.7)
    .scale_colour_brewer(palette='Set1')
    .labs(
        title='Multi-Aesthetic Mapping',
        size='Baseline Score',
    )
).show()

# %% [markdown]
# ## 2. Statistical Visualizations
#
# ggviews provides comprehensive statistical geoms for data analysis.

# %% [markdown]
# ### Box Plots for Distribution Analysis

# %%
(
    gv.ggplot(stats_data, gv.aes(x='treatment', y='response', fill='treatment'))
    .geom_boxplot(width=0.7, alpha=0.8)
    .scale_fill_brewer(palette='Set2')
    .coord_flip()
    .theme_minimal()
    .labs(
        title='Treatment Response Distributions',
        x='Treatment Group',
        y='Response Score',
        fill='Treatment',
    )
).show()

# %% [markdown]
# ### Density Plots for Smooth Distributions

# %%
(
    gv.ggplot(stats_data, gv.aes(x='response', fill='treatment'))
    .geom_density(alpha=0.6)
    .scale_fill_viridis_d()
    .theme_minimal()
    .labs(
        title='Treatment Response Densities',
        x='Response Score',
        y='Density',
        fill='Treatment',
    )
).show()

# %% [markdown]
# ### Smoothed Trend Lines

# %%
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response', color='gender'))
    .geom_point(alpha=0.5)
    .geom_smooth(method='lm', se=False)
    .scale_colour_brewer(palette='Dark2')
    .theme_classic()
    .labs(
        title='Age vs Response by Gender',
        x='Age (years)',
        y='Response Score',
        color='Gender',
    )
).show()

# %% [markdown]
# ## 3. Advanced Theming and Customization
#
# ggviews provides fine-grained control over plot appearance using theme elements.

# %%
(
    gv.ggplot(stats_data, gv.aes(x='treatment', y='response'))
    .geom_boxplot(gv.aes(fill='treatment'), alpha=0.7)
    .geom_point(position=gv.position_jitter(width=0.2), alpha=0.4)
    .scale_fill_brewer(palette='Blues')
    .theme(
        panel_grid_minor=gv.element_blank(),
        axis_text_x=gv.element_text(angle=45, hjust=1, size=12),
        plot_title=gv.element_text(size=16, color='darkblue'),
        legend_position='bottom',
        panel_background=gv.element_rect(fill='white'),
    )
    .labs(
        title='Treatment Efficacy Analysis',
        x='Treatment Group',
        y='Response Score (higher is better)',
        fill='Treatment',
    )
).show()

# %% [markdown]
# ## 4. Faceting for Multi-Panel Plots
#
# Create multiple related plots to explore different aspects of your data.

# %%
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response', color='gender'))
    .geom_point(alpha=0.7)
    .geom_smooth(method='lm', se=False)
    .facet_wrap('~treatment', scales='free')
    .scale_colour_brewer(palette='Set1')
    .theme_minimal()
    .labs(
        title='Age-Response Relationship by Treatment',
        x='Age (years)',
        y='Response Score',
        color='Gender',
    )
).show()

# %% [markdown]
# ### Grid-based Faceting

# %%
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response'))
    .geom_point(alpha=0.6)
    .geom_smooth(method='lm', color='red', alpha=0.7)
    .facet_grid('gender ~ treatment')
    .theme_bw()
    .labs(
        title='Treatment Response by Age, Gender, and Treatment',
        x='Age (years)',
        y='Response Score',
    )
).show()

# %% [markdown]
# ## 5. Time Series and Line Plots

# %%
(
    gv.ggplot(ts_data, gv.aes(x='date', y='value', color='stock'))
    .geom_line(alpha=0.8)
    .scale_colour_brewer(palette='Set1')
    .theme_minimal()
    .labs(
        title='Stock Price Performance',
        x='Date',
        y='Price ($)',
        color='Stock',
    )
).show()

# %% [markdown]
# ## 6. 2D Visualizations and Heatmaps

# %%
(
    gv.ggplot(heatmap_data, gv.aes(x='x', y='y', fill='temperature'))
    .geom_tile()
    .scale_fill_viridis_c(option='plasma')
    .theme_void()
    .labs(title='Temperature Distribution', fill='Temperature')
).show()

# %% [markdown]
# ### Categorical Heatmap

# %%
(
    gv.ggplot(heatmap_data, gv.aes(x='x', y='y', fill='category'))
    .geom_tile(alpha=0.8)
    .scale_fill_brewer(palette='Set3')
    .theme_minimal()
    .labs(
        title='Categorical Spatial Data',
        x='X Coordinate',
        y='Y Coordinate',
        fill='Category',
    )
).show()

# %% [markdown]
# ## 7. Geographic Visualizations

# %%
(
    gv.ggplot(cities, gv.aes(x='longitude', y='latitude', size='population', color='continent'))
    .geom_map(map_type='simple', alpha=0.8)
    .scale_colour_brewer(palette='Set2')
    .theme_minimal()
    .labs(
        title='Major World Cities',
        x='Longitude',
        y='Latitude',
        size='Population (millions)',
        color='Continent',
    )
).show()

# %% [markdown]
# ## 8. Bar Charts and Categorical Data

# %%
treatment_summary = stats_data.groupby(['treatment', 'gender'])['response'].mean().reset_index()

(
    gv.ggplot(treatment_summary, gv.aes(x='treatment', y='response', fill='gender'))
    .geom_bar(stat='identity', position=gv.position_dodge(width=0.8), alpha=0.8)
    .scale_fill_brewer(palette='Pastel1')
    .theme_classic()
    .labs(
        title='Average Response by Treatment and Gender',
        x='Treatment Group',
        y='Average Response Score',
        fill='Gender',
    )
).show()

# %% [markdown]
# ## 9. Statistical Summaries and Error Bars

# %%
treatment_stats = (
    stats_data
    .groupby('treatment')['response']
    .agg(['mean', 'std', 'count'])
    .reset_index()
)
treatment_stats['se'] = treatment_stats['std'] / np.sqrt(treatment_stats['count'])

(
    gv.ggplot(treatment_stats, gv.aes(x='treatment', y='mean'))
    .geom_bar(stat='identity', fill='steelblue', alpha=0.7)
    .geom_errorbar(gv.aes(ymin='mean-se', ymax='mean+se'), width=0.3, color='black')
    .theme_minimal()
    .labs(
        title='Treatment Effects with Standard Errors',
        x='Treatment Group',
        y='Mean Response Score',
    )
).show()

# %% [markdown]
# ## 10. Colorblind-Safe Theme (theme_essi)

# %%
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response', color='treatment'))
    .geom_point(alpha=0.8)
    .theme_essi()
    .labs(
        title='Colorblind-Safe Palette',
        x='Age (years)',
        y='Response Score',
        color='Treatment',
    )
).show()

# %% [markdown]
# ## 11. Highlighting with gghighlight

# %%
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response'))
    .geom_point(alpha=0.7)
    .gghighlight("treatment == 'Drug B'")
    .labs(
        title='Drug B Highlighted',
        x='Age (years)',
        y='Response Score',
    )
).show()

# %% [markdown]
# ## 12. Complex Multi-Layer Visualizations

# %%
(
    gv.ggplot(stats_data, gv.aes(x='age', y='response'))
    .geom_point(gv.aes(color='treatment', size='baseline'), alpha=0.6)
    .geom_smooth(method='lm', color='black', alpha=0.8, se=True)
    .scale_colour_viridis_d(option='plasma')
    .facet_wrap('~gender')
    .theme(
        panel_grid_minor=gv.element_blank(),
        strip_text=gv.element_text(size=12, color='darkblue'),
        legend_position='bottom',
    )
    .labs(
        title='Comprehensive Multi-Layer Analysis',
        x='Age (years)',
        y='Response Score',
        color='Treatment',
        size='Baseline',
    )
).show()

# %% [markdown]
# ## Summary
#
# This comprehensive example demonstrates ggviews' capabilities across all major
# areas of data visualization:
#
# - **Aesthetic Mappings**: Color, size, fill, and other visual properties
# - **Statistical Geoms**: Box plots, density plots, smoothing, error bars
# - **Theming**: Fine-grained control over plot appearance with `theme_essi()`,
#   `theme_minimal()`, `theme_classic()`, etc.
# - **Faceting**: Multi-panel plots for exploring subgroups
# - **Color Scales**: Viridis, ColorBrewer, and custom palettes
# - **Geographic Visualization**: Mapping capabilities
# - **2D Visualization**: Heatmaps and tile plots
# - **Highlighting**: `gghighlight()` for emphasising subsets
# - **Complex Layering**: Multiple geoms and aesthetics combined
#
# ggviews provides a comprehensive, ggplot2-compatible grammar of graphics
# for Python, enabling publication-quality visualizations with readable,
# expressive code.

# %%
