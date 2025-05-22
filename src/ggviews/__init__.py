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
    ...    + geom_point(alpha=0.5)
    ...    + labs(title='Diamond Prices by Carat and Cut')
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
from .geoms.boxplot import GeomBoxplot
from .geoms.violin import GeomViolin
from .geoms.density import GeomDensity

# Import scales
from .scales import scale_x_log10, scale_y_log10

# Import themes
from .themes import theme_default, theme_minimal, theme_bw, theme_ggplot2

# Import facets
from .facets import facet_grid, facet_wrap

# Import coordinates
from .coords.flip import coord_flip
from .coords.polar import coord_polar

# Initialize holoviews extension for better rendering
import holoviews as hv
try:
    hv.extension('bokeh')
except:
    # Fall back to no extension if bokeh is not available
    pass

# Define geom functions
def geom_point(*args, **kwargs):
    return GeomPoint(*args, **kwargs)

def geom_line(*args, **kwargs):
    return GeomLine(*args, **kwargs)

def geom_bar(*args, **kwargs):
    return GeomBar(*args, **kwargs)

def geom_histogram(*args, **kwargs):
    return GeomHistogram(*args, **kwargs)

def geom_boxplot(*args, **kwargs):
    return GeomBoxplot(*args, **kwargs)

def geom_violin(*args, **kwargs):
    return GeomViolin(*args, **kwargs)

def geom_density(*args, **kwargs):
    return GeomDensity(*args, **kwargs)

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
_add_geom_method('boxplot', GeomBoxplot)
_add_geom_method('violin', GeomViolin)
_add_geom_method('density', GeomDensity)


# Add scale methods
def _add_scale_method(name, scale_func):
    """Add a scale_* method to the GGPlot class."""
    
    def method(self, *args, **kwargs):
        return self.add_scale(scale_func(*args, **kwargs))
    
    # Add the method to GGPlot
    setattr(GGPlot, name, method)


# Define scale functions
def scale_color_continuous(*args, **kwargs):
    from .scales.color import scale_color_continuous
    return scale_color_continuous(*args, **kwargs)

def scale_color_discrete(*args, **kwargs):
    from .scales.color import scale_color_discrete
    # If no palette is specified, use ggplot2 palette by default
    if 'palette' not in kwargs:
        from .themes.presets import ggplot2_color_palette
        kwargs['palette'] = ggplot2_color_palette()
    return scale_color_discrete(*args, **kwargs)

def scale_fill_continuous(*args, **kwargs):
    from .scales.color import scale_fill_continuous
    return scale_fill_continuous(*args, **kwargs)

def scale_fill_discrete(*args, **kwargs):
    from .scales.color import scale_fill_discrete
    # If no palette is specified, use ggplot2 palette by default
    if 'palette' not in kwargs:
        from .themes.presets import ggplot2_fill_palette
        kwargs['palette'] = ggplot2_fill_palette()
    return scale_fill_discrete(*args, **kwargs)

# Add scale methods
_add_scale_method('scale_x_log10', scale_x_log10)
_add_scale_method('scale_y_log10', scale_y_log10)
_add_scale_method('scale_color_continuous', scale_color_continuous)
_add_scale_method('scale_color_discrete', scale_color_discrete)
_add_scale_method('scale_fill_continuous', scale_fill_continuous)
_add_scale_method('scale_fill_discrete', scale_fill_discrete)


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
_add_theme_method('theme_ggplot2', theme_ggplot2)


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


# Add coordinate methods
def _add_coord_method(name, coord_func):
    """Add a coord_* method to the GGPlot class."""
    
    def method(self, *args, **kwargs):
        return self.coord(coord_func(*args, **kwargs))
    
    # Add the method to GGPlot
    setattr(GGPlot, f"coord_{name}", method)


# Add coordinate methods
_add_coord_method('flip', coord_flip)
_add_coord_method('polar', coord_polar)


# Define public API
__all__ = [
    'ggplot',
    'aes',
    'load_dataset',
    'list_datasets',
    'geom_point',
    'geom_line',
    'geom_bar',
    'geom_histogram',
    'geom_boxplot',
    'geom_violin',
    'geom_density',
    'scale_x_log10',
    'scale_y_log10',
    'scale_color_continuous',
    'scale_color_discrete',
    'scale_fill_continuous',
    'scale_fill_discrete',
    'theme_default',
    'theme_minimal',
    'theme_bw',
    'theme_ggplot2',
    'facet_grid',
    'facet_wrap',
    'coord_flip',
    'coord_polar',
]