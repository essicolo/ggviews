# ggviews - Grammar of Graphics for Python with Holoviews

ggviews is a Python package that implements the Grammar of Graphics, inspired by ggplot2 in R, using Holoviews as the rendering backend. It allows users to create complex visualizations through layering geometric objects, statistical transformations, and aesthetic mappings.

## Basic Usage

```python
from ggviews import ggplot, aes, load_dataset
diamonds = load_dataset('diamonds')
(ggplot(diamonds, aes(x='carat', y='price', color='cut'))
    .geom_point(alpha=0.5)
    .labs(title='Diamond Prices by Carat and Cut')
    .theme_minimal()
)
```

## Features

- Method chaining for building complex plots (similar to ggplot2 syntax)
- Support for different geometries (points, lines, bars, histograms)
- Aesthetic mappings (color, size, shape, etc.)
- Scales (log scales, discrete scales, continuous scales)
- Themes (default, minimal, black-and-white)
- Faceting (grid, wrap)
- Coordinate systems (Cartesian, Polar)
- Labels and annotations

## Requirements

- Python 3.10+
- pandas
- holoviews
- bokeh
- numpy
- scipy

## Changelog

### Version 0.2.0 (May 22, 2025)

- Added faceting functionality with `facet_grid` and `facet_wrap`
- Fixed dimension error when using numeric aesthetic mappings with `geom_point`, `geom_line`, and `geom_bar`
- Fixed HTML representation of plots in Jupyter notebooks
- Fixed handling of nested aesthetics in geometry methods (e.g., `geom_point(aes(color='cyl'))`)
- Enhanced robustness of aesthetic processing functions
- Added example notebook for debugging common issues and demonstrating fixes

## Example Gallery

### Scatter Plot

```python
from ggviews import ggplot, aes, load_dataset
mtcars = load_dataset('mtcars')
(ggplot(mtcars, aes(x='wt', y='mpg', color='cyl'))
    .geom_point(size=5, alpha=0.7)
    .labs(
        title='Car Weight vs. Fuel Efficiency',
        subtitle='With Engine Cylinders as Color',
        x='Weight (1000 lbs)',
        y='Miles per Gallon'
    )
    .theme_minimal()
)
```

### Line Plot with Points

```python
from ggviews import ggplot, aes, load_dataset
economics = load_dataset('economics')
(ggplot(economics, aes(x='date', y='unemploy/pop'))
    .geom_line(color='blue', linewidth=1.5)
    .geom_point(color='red', size=3)
    .labs(
        title='US Unemployment Rate Over Time',
        x='Year',
        y='Unemployment Rate'
    )
    .theme_bw()
)
```

### Bar Chart

```python
from ggviews import ggplot, aes, load_dataset
mtcars = load_dataset('mtcars')
gear_mpg = mtcars.groupby('gear')['mpg'].mean().reset_index()
(ggplot(gear_mpg, aes(x='gear', y='mpg'))
    .geom_bar(stat='identity', fill='skyblue', color='black')
    .labs(
        title='Average MPG by Number of Gears',
        x='Number of Gears',
        y='Average Miles per Gallon'
    )
    .theme_default()
)
```

### Histogram

```python
from ggviews import ggplot, aes, load_dataset
diamonds = load_dataset('diamonds')
(ggplot(diamonds, aes(x='price'))
    .geom_histogram(bins=50, fill='steelblue', color='black')
    .labs(
        title='Distribution of Diamond Prices',
        x='Price ($)',
        y='Count'
    )
    .theme_minimal()
)
```

### Scatter Plot with Log Scale

```python
from ggviews import ggplot, aes, load_dataset, scale_x_log10
mtcars = load_dataset('mtcars')
(ggplot(mtcars, aes(x='hp', y='qsec', color='am'))
    .geom_point(size=5, alpha=0.7)
    .scale_x_log10()
    .labs(
        title='Horsepower vs. Quarter Mile Time',
        subtitle='With Transmission Type as Color',
        x='Horsepower (log scale)',
        y='Quarter Mile Time (s)'
    )
    .theme_bw()
)
```

### Facet Grid

```python
from ggviews import ggplot, aes, facet_grid, load_dataset
mpg = load_dataset('mpg')
(ggplot(mpg, aes(x='displ', y='hwy', color='class'))
    .geom_point(size=4, alpha=0.7)
    .facet_grid(row='drv', col='cyl')
    .labs(
        title='Highway MPG vs. Engine Displacement',
        subtitle='Faceted by Drive Type (rows) and Cylinders (columns)',
        x='Engine Displacement (L)',
        y='Highway MPG'
    )
    .theme_minimal()
)
```

### Facet Wrap

```python
from ggviews import ggplot, aes, facet_wrap, load_dataset
mpg = load_dataset('mpg')
(ggplot(mpg, aes(x='cty', y='hwy', color='drv'))
    .geom_point(size=3, alpha=0.7)
    .facet_wrap('manufacturer', ncol=3)
    .labs(
        title='City vs Highway MPG by Manufacturer',
        x='City MPG',
        y='Highway MPG'
    )
    .theme_minimal()
)
```

## Architecture

ggviews is organized in a modular fashion with the following structure:

```
src/
  ggviews/
    coords/        # Coordinate systems
    facets/        # Faceting
    geoms/         # Geometric objects
    legends/       # Legend handling
    scales/        # Scale transformations
    stats/         # Statistical transformations
    themes/        # Visual themes
    utils/         # Utility functions
    __init__.py    # Package initialization
    aes.py         # Aesthetic mappings
    core.py        # Core functionality
    data_loader.py # Data loading utilities
```

## Design Notes

- Users can build complex plots by composing objects with method chaining (not '+') (e.g., `ggplot(data, aes(...)).geom_point().facet_wrap().scale_x_log10().theme_bw()`), mimicking ggplot2 syntax.
- User aesthetic mappings (aes) are mapped to Holoviews kdims/vdims for each supported geometry.
- The package supports the main geoms, stats, scales, guides, themes, facets, coordinate systems, overlays, and layouts as in ggplot2.
- Users do not interact directly with Holoviews, but only with this grammar-of-graphics API.
- Each submodule (geoms, scales, etc.) is extensible and independently testable.
- The layer system allows overlays and layouts via Holoviews operations.
- Faceting is supported via layout/grid using Holoviews .groupby/.layout.
- Custom legends, themes, and scales are implemented using Holoviews opts.

## Testing

- All core functionalities have unittests.
- For plotting outputs, image comparison is NOT used.
- Tests render the output to HTML using Holoviews' .save() or .to_html(), and parse the HTML output to check for the expected structure, content, and element presence.
- For interactive features (tooltips, hovers, facets), the HTML/JS is parsed for expected content or structure.
- All modules and public APIs are tested for robustness, errors, and correct composition of layers/facets.

## Quality/Completeness

- All modules are documented and type-annotated.
- Docstrings and usage examples are provided in each module.
- Examples in src/examples/ cover: scatter plot, overlay, facet grid, custom legend, and theme.
- The package uses modern Python best practices (type hints, dataclasses where useful).
- The package is pip installable and follows standard Python packaging (pyproject.toml).
- Output is robust for both Jupyter/Marimo and web export.