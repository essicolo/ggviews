# ggviews: A ggplot2-style API for holoviews

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

ggviews is a Python library that provides a **ggplot2-style API** for creating beautiful, interactive visualizations using **holoviews**. It brings the beloved grammar of graphics from R's ggplot2 to the Python ecosystem with the power and flexibility of holoviews.

## Features

✨ **Familiar Syntax**: Use the same grammar of graphics you know and love from ggplot2
🔗 **Method Chaining**: Build plots incrementally with intuitive method chaining  
🎨 **Rich Geoms**: Support for all major geom types (point, line, bar, histogram, etc.)
🎭 **Themes**: Beautiful default themes matching ggplot2's aesthetics
🎯 **Faceting**: Powerful facet_wrap and facet_grid for subplotting
⚡ **Interactive**: Leverage holoviews' interactive capabilities
📊 **Extensible**: Easy to extend with custom geoms and themes

## Installation

```bash
pip install ggviews
```

For development installation:
```bash
git clone https://github.com/ggviews/ggviews.git
cd ggviews  
pip install -e ".[dev]"
```

## Quick Start

```python
from ggviews import ggplot, aes
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Create a beautiful plot with method chaining
(ggplot(df, aes(x='height', y='weight'))
 .geom_point(aes(color='species'), size=3, alpha=0.7)
 .geom_smooth(method='lm')
 .theme_minimal()
 .labs(
     title='Height vs Weight by Species',
     x='Height (cm)', 
     y='Weight (kg)'
 )
 .facet_wrap('~species'))
```

## Core Concepts

### Grammar of Graphics
ggviews implements the layered grammar of graphics:

1. **Data**: Your pandas DataFrame
2. **Aesthetics**: Map data to visual properties (x, y, color, size, etc.)
3. **Geometries**: Visual representations of data (points, lines, bars, etc.) 
4. **Scales**: Control aesthetic mappings
5. **Themes**: Overall visual styling
6. **Facets**: Subplots based on data subsets

### Method Chaining
Build plots incrementally:

```python
plot = (ggplot(data)
        .geom_point()     # Add points
        .geom_line()      # Add lines  
        .theme_classic()  # Apply theme
        .labs(title='My Plot'))  # Add labels
```

## Available Geoms

- `geom_point()` - Scatter plots
- `geom_line()` - Line plots
- `geom_bar()` - Bar charts
- `geom_histogram()` - Histograms  
- `geom_boxplot()` - Box plots
- `geom_violin()` - Violin plots
- `geom_density()` - Density plots
- `geom_smooth()` - Smoothed conditional means
- `geom_area()` - Area plots
- `geom_ribbon()` - Ribbons/confidence bands
- `geom_tile()` - Heatmaps
- `geom_text()` - Text annotations

## Themes

- `theme_minimal()` - Clean, minimal theme
- `theme_classic()` - Classic ggplot2 theme  
- `theme_bw()` - Black and white theme
- `theme_dark()` - Dark theme
- `theme_void()` - Completely blank theme

## Scales

- `scale_color_manual()` - Manual color scales
- `scale_color_discrete()` - Discrete color scales
- `scale_color_continuous()` - Continuous color scales
- `scale_x_continuous()` / `scale_y_continuous()` - Continuous axis scales
- `scale_x_discrete()` / `scale_y_discrete()` - Discrete axis scales

## Faceting

Create subplots with:
- `facet_wrap('~variable')` - Wrap subplots in a grid
- `facet_grid('row_var ~ col_var')` - Grid of subplots

## Examples

### Basic Scatter Plot
```python
ggplot(df, aes(x='x', y='y')).geom_point()
```

### Colored by Category
```python
ggplot(df, aes(x='x', y='y', color='category')).geom_point()
```

### Multiple Layers
```python
(ggplot(df, aes(x='x', y='y'))
 .geom_point()
 .geom_smooth())
```

### Faceted Plot
```python
(ggplot(df, aes(x='x', y='y'))
 .geom_point() 
 .facet_wrap('~group'))
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Hadley Wickham's [ggplot2](https://ggplot2.tidyverse.org/)
- Built on the excellent [holoviews](http://holoviews.org/) library
- Thanks to the broader Python data visualization community