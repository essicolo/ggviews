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
from .coords import *
from .viridis import *
from .advanced_themes import element_blank, element_text, element_line, element_rect, AdvancedTheme
from .additional_geoms import *
from .stats import *
from .positions import *
from .geom_map import geom_map
from .geom_boxplot import geom_boxplot
from .geom_density import geom_density
from .geom_tile import geom_tile, geom_raster
from .coord_flip import coord_flip
from .brewer_scales import scale_colour_brewer, scale_color_brewer, scale_fill_brewer, display_brewer_palettes
from .position_dodge import position_dodge
from .theme_elements import theme, element_blank, element_text, element_line, element_rect

__version__ = "0.2.0"  # Version bump for major feature additions
__author__ = "ggviews team"
__email__ = "contact@ggviews.org"

__all__ = [
    'ggplot',
    'aes',
    # Core geoms
    'geom_point',
    'geom_line', 
    'geom_bar',
    'geom_histogram',
    'geom_boxplot',
    'geom_density',
    'geom_area',
    'geom_smooth',
    # Additional geoms (NEW!)
    'geom_ribbon',
    'geom_violin',
    'geom_text',
    'geom_label', 
    'geom_errorbar',
    'geom_map',
    'geom_boxplot',
    'geom_density',
    'geom_tile',
    'geom_raster',
    # Statistical transformations (NEW!)
    'stat_smooth',
    'stat_summary',
    'geom_smooth_enhanced',
    # Position adjustments (NEW!)
    'position_identity',
    'position_stack',
    'position_fill',
    'position_dodge',
    'position_jitter',
    'position_nudge',
    'position_jitterdodge',
    # Themes
    'theme_minimal',
    'theme_classic', 
    'theme_bw',
    'theme_dark',
    'theme_void',
    # Advanced theme elements
    'element_blank',
    'element_text',
    'element_line', 
    'element_rect',
    'AdvancedTheme',
    # Basic scales
    'scale_color_manual',
    'scale_color_discrete',
    'scale_color_continuous',
    'scale_x_continuous',
    'scale_y_continuous',
    'scale_x_discrete',
    'scale_y_discrete',
    # Viridis scales
    'scale_colour_viridis_c',
    'scale_colour_viridis_d',
    'scale_color_viridis_c', 
    'scale_color_viridis_d',
    'scale_colour_viridis',
    'scale_color_viridis',
    'scale_fill_viridis_c',
    'scale_fill_viridis_d',
    'scale_fill_viridis',
    # Brewer scales
    'scale_colour_brewer',
    'scale_color_brewer',
    'scale_fill_brewer',
    'display_brewer_palettes',
    # Facets
    'facet_wrap',
    'facet_grid',
    # Coordinate systems
    'coord_cartesian',
    'coord_fixed',
    'coord_equal', 
    'coord_flip',
    'coord_trans',
    'coord_polar',
    # Utils
    'labs',
    'xlim',
    'ylim',
]