# ggviews Implementation Guide

## Overview

ggviews is a complete implementation of the grammar of graphics for Python, built on top of holoviews. It provides a ggplot2-style API that should be familiar to R users while leveraging the power and interactivity of holoviews.

## Architecture

### Core Components

1. **ggplot** - Main plotting class that manages data, aesthetics, layers, scales, themes, and facets
2. **aes** - Aesthetic mappings that connect data variables to visual properties  
3. **Geoms** - Geometric objects that represent data (points, lines, bars, etc.)
4. **Themes** - Control overall plot appearance and styling
5. **Scales** - Control how data values map to aesthetics
6. **Facets** - Create subplots based on categorical variables
7. **Utils** - Helper functions for labels, limits, and other utilities

### Method Chaining

The library supports both R-style `+` operator and Python-style method chaining:

```python
# R-style (+ operator)
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_minimal()

# Python-style (method chaining) 
ggplot(df, aes(x='x', y='y')).geom_point().theme_minimal()
```

## Key Features Implemented

### ✅ Core Grammar of Graphics
- [x] Data layer (pandas DataFrame support)
- [x] Aesthetic mappings (x, y, color, size, alpha, etc.)
- [x] Geometric objects (geoms)
- [x] Statistical transformations (basic stats)
- [x] Scales (color, continuous, discrete)
- [x] Coordinate systems (basic support)
- [x] Themes (multiple built-in themes)
- [x] Faceting (wrap and grid)

### ✅ Geoms (Geometric Objects)
- [x] `geom_point()` - Scatter plots
- [x] `geom_line()` - Line plots  
- [x] `geom_bar()` - Bar charts (count and identity stats)
- [x] `geom_histogram()` - Histograms
- [x] `geom_boxplot()` - Box plots
- [x] `geom_smooth()` - Smoothed regression lines
- [x] `geom_density()` - Density plots

### ✅ Themes
- [x] `theme_minimal()` - Clean, minimal appearance
- [x] `theme_classic()` - Traditional statistical graphics
- [x] `theme_bw()` - Black and white theme
- [x] `theme_dark()` - Dark theme for low light
- [x] `theme_void()` - Completely clean theme

### ✅ Scales  
- [x] `scale_color_manual()` - Manual color specification
- [x] `scale_color_discrete()` - Discrete color scales
- [x] `scale_color_continuous()` - Continuous color gradients
- [x] `scale_x_continuous()` / `scale_y_continuous()` - Continuous axis scales
- [x] `scale_x_discrete()` / `scale_y_discrete()` - Discrete axis scales

### ✅ Faceting
- [x] `facet_wrap()` - Wrap subplots in rectangular layout
- [x] `facet_grid()` - Grid of subplots with row/column variables
- [x] Formula syntax support (`~var`, `row_var ~ col_var`)
- [x] Multiple faceting variables
- [x] Layout control (ncol, nrow)

### ✅ Utilities
- [x] `labs()` - Add labels (title, axis labels, legend titles)
- [x] `xlim()` / `ylim()` - Set axis limits  
- [x] R-style helper functions (`c()`, `seq()`, `rep()`)
- [x] Data manipulation helpers (`cut()`)

## Usage Patterns

### Basic Plotting
```python
from ggviews import ggplot, aes

# Basic scatter plot
ggplot(df, aes(x='height', y='weight')).geom_point()
```

### Method Chaining (Recommended)
```python
(ggplot(df, aes(x='height', y='weight', color='species'))
 .geom_point(size=4, alpha=0.8)
 .geom_smooth(method='lm')
 .scale_color_manual(values=['red', 'blue', 'green'])
 .theme_minimal()
 .labs(title='Height vs Weight by Species')
 .facet_wrap('~location'))
```

### Plus Operator (R-style)
```python
from ggviews.geoms import geom_point
from ggviews.themes import theme_minimal

(ggplot(df, aes(x='height', y='weight'))
 + geom_point() 
 + theme_minimal())
```

## Extensibility

The library is designed to be easily extensible:

### Adding New Geoms
```python
class geom_custom(GeomLayer):
    def __init__(self, mapping=None, data=None, **kwargs):
        super().__init__(mapping, data, **kwargs)
        # Custom initialization
    
    def _render(self, data, combined_aes, ggplot_obj):
        # Custom rendering logic
        return holoviews_plot
```

### Adding New Themes
```python
class theme_custom(Theme):
    def __init__(self, **kwargs):
        default_options = {
            'width': 600,
            'bgcolor': 'lightgray',
            # ... more options
        }
        default_options.update(kwargs)
        super().__init__(**default_options)
```

### Adding New Scales
```python
class scale_custom(Scale):
    def __init__(self, **kwargs):
        super().__init__('aesthetic_name', **kwargs)
    
    def _apply(self, plot, ggplot_obj, data):
        # Custom scale logic
        return plot
```

## Integration with holoviews

ggviews builds on holoviews' powerful features:

- **Interactive plots** - Zoom, pan, hover tooltips
- **Multiple backends** - Bokeh (interactive) and Matplotlib (static)
- **Composable plots** - Combine multiple plot types
- **Rich ecosystem** - Integrates with Jupyter, Panel, etc.

## Testing

Comprehensive test suite covers:
- Core functionality (ggplot, aes)  
- All geom types
- Theme system
- Scale system
- Faceting (wrap and grid)
- Method chaining
- Error handling
- Integration testing

Run tests with:
```bash
python -m pytest tests/ -v
```

## Performance Considerations

- **Data copying** - ggplot objects are immutable; each operation creates a copy
- **Large datasets** - Consider sampling for interactive plots
- **Memory usage** - Faceting creates multiple plot objects
- **Rendering** - holoviews handles efficient rendering

## Comparison with Other Libraries

| Feature | ggviews | plotnine | seaborn |
|---------|---------|----------|---------|
| ggplot2 syntax | ✅ Full | ✅ Full | ❌ Different |
| Method chaining | ✅ | ❌ | ❌ |
| Interactive plots | ✅ holoviews | ❌ | ❌ |
| Faceting | ✅ wrap+grid | ✅ wrap+grid | ✅ Limited |
| Themes | ✅ Multiple | ✅ Multiple | ✅ Limited |
| Extensions | ✅ Easy | ✅ Moderate | ❌ Hard |

## Future Enhancements

### Planned Features
- [ ] Additional geoms (violin, ribbon, errorbar, etc.)
- [ ] Advanced statistical transformations
- [ ] Custom coordinate systems (polar, map projections)
- [ ] Animation support
- [ ] More sophisticated legends and guides
- [ ] Better text/annotation support

### Advanced Faceting
- [ ] Free scales per facet
- [ ] Nested faceting
- [ ] Custom facet layouts

### Statistical Layers
- [ ] More smoothing methods (loess, gam)  
- [ ] Confidence intervals
- [ ] Statistical tests overlays

## Best Practices

1. **Use method chaining** for complex plots
2. **Start simple** and build up layers incrementally  
3. **Test faceting** thoroughly with your data structure
4. **Consider performance** for large datasets
5. **Use appropriate themes** for your context
6. **Leverage holoviews backends** (Bokeh for interactivity, Matplotlib for publication)

## Conclusion

ggviews provides a comprehensive, extensible implementation of the grammar of graphics for Python. It combines the familiar ggplot2 syntax with the power of holoviews, making it ideal for both exploratory data analysis and publication-ready visualizations.

The library is designed to grow with the community - contributions of new geoms, themes, and features are welcome!