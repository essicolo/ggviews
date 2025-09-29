"""
ggviews: A ggplot2-style API for holoviews

A grammar of graphics implementation for holoviews that provides
a familiar ggplot2-like interface with method chaining.

Usage:
    from ggviews import ggplot, aes
    
    (ggplot(df)
     .geom_point(aes(x='height', y='weight', color='species'))
     .theme_minimal()
     .labs(title='Height vs Weight by Species'))
"""

from .core import ggplot, aes
from .geoms import *
from .themes import *
from .scales import *
from .facets import *

__version__ = "0.1.0"
__author__ = "ggviews team"
__email__ = "contact@ggviews.org"

__all__ = [
    'ggplot',
    'aes',
    # Geoms
    'geom_point',
    'geom_line', 
    'geom_bar',
    'geom_histogram',
    'geom_boxplot',
    'geom_violin',
    'geom_density',
    'geom_smooth',
    'geom_area',
    'geom_ribbon',
    'geom_tile',
    'geom_text',
    # Themes
    'theme_minimal',
    'theme_classic', 
    'theme_bw',
    'theme_dark',
    'theme_void',
    # Scales
    'scale_color_manual',
    'scale_color_discrete',
    'scale_color_continuous',
    'scale_x_continuous',
    'scale_y_continuous',
    'scale_x_discrete',
    'scale_y_discrete',
    # Facets
    'facet_wrap',
    'facet_grid',
    # Utils
    'labs',
    'xlim',
    'ylim',
]