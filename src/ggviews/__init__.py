"""
ggviews: A Grammar of Graphics for Python with Holoviews

ggviews is a Python package that implements the Grammar of Graphics,
inspired by ggplot2 in R, using Holoviews as the rendering backend.
It allows users to create complex visualizations through layering
geometric objects, statistical transformations, and aesthetic mappings.

Basic usage example:
    >>> from ggviews import ggplot, aes, load_dataset
    >>> diamonds = load_dataset('diamonds')
    >>> (ggplot(diamonds, aes(x='carat', y='price', color='cut'))
    ...    .geom_point(alpha=0.5)
    ...    .labs(title='Diamond Prices by Carat and Cut')
    ... )
"""

# Import main plotting function
from .core import ggplot, GGPlot

# Import aesthetic mapping
from .aes import aes, Aesthetics

# Import data loader
from .data_loader import load_dataset, list_datasets

# Import geometries
from .geoms.point import GeomPoint
from .geoms.line import GeomLine
from .geoms.bar import GeomBar
from .geoms.histogram import GeomHistogram

# Import scales
from .scales import scale_x_log10, scale_y_log10

# Import themes
from .themes import theme_default, theme_minimal, theme_bw

# Import facets
from .facets import facet_grid, facet_wrap

# Initialize holoviews extension for better rendering
import holoviews as hv
try:
    hv.extension('bokeh')
except:
    # Fall back to no extension if bokeh is not available
    pass


# Add geometry methods to GGPlot class
def _add_geom_method(name, geom_class):
    """Add a geom_* method to the GGPlot class."""
    
    def method(self, *args, **kwargs):
        return self.add_layer(geom_class(*args, **kwargs))
    
    # Add the method to GGPlot
    setattr(GGPlot, f"geom_{name}", method)


# Add geom methods
_add_geom_method('point', GeomPoint)
_add_geom_method('line', GeomLine)
_add_geom_method('bar', GeomBar)
_add_geom_method('histogram', GeomHistogram)


# Add scale methods
def _add_scale_method(name, scale_func):
    """Add a scale_* method to the GGPlot class."""
    
    def method(self, *args, **kwargs):
        return self.add_scale(scale_func(*args, **kwargs))
    
    # Add the method to GGPlot
    setattr(GGPlot, name, method)


# Add scale methods
_add_scale_method('scale_x_log10', scale_x_log10)
_add_scale_method('scale_y_log10', scale_y_log10)


# Add theme methods
def _add_theme_method(name, theme_func):
    """Add a theme_* method to the GGPlot class."""
    
    def method(self, *args, **kwargs):
        return self.theme(theme_func(*args, **kwargs))
    
    # Add the method to GGPlot
    setattr(GGPlot, name, method)


# Add theme methods
_add_theme_method('theme_default', theme_default)
_add_theme_method('theme_minimal', theme_minimal)
_add_theme_method('theme_bw', theme_bw)


# Add facet methods
def _add_facet_method(name, facet_func):
    """Add a facet_* method to the GGPlot class."""
    
    def method(self, *args, **kwargs):
        return self.facet(facet_func(*args, **kwargs))
    
    # Add the method to GGPlot
    setattr(GGPlot, f"facet_{name}", method)


# Add facet methods
_add_facet_method('grid', facet_grid)
_add_facet_method('wrap', facet_wrap)


# Define public API
__all__ = [
    'ggplot',
    'aes',
    'load_dataset',
    'list_datasets',
    'scale_x_log10',
    'scale_y_log10',
    'theme_default',
    'theme_minimal',
    'theme_bw',
    'facet_grid',
    'facet_wrap',
]
