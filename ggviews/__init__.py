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

# Core
from .core import ggplot, aes

# Geoms (core)
from .geoms import geom_point, geom_line, geom_bar, geom_histogram, geom_smooth, geom_area

# Geoms (additional, each in their own module to avoid duplication)
from .geom_boxplot import geom_boxplot
from .geom_density import geom_density
from .geom_tile import geom_tile, geom_raster
from .geom_map import geom_map
from .additional_geoms import geom_ribbon, geom_violin, geom_text, geom_label, geom_errorbar
from .repel import geom_text_repel, geom_label_repel

# Highlight
from .highlight import gghighlight

# Themes
from .themes import theme_minimal, theme_classic, theme_bw, theme_dark, theme_void

# Theme elements (canonical source: advanced_themes.py)
from .advanced_themes import element_blank, element_text, element_line, element_rect, AdvancedTheme
from .advanced_themes import theme

# Scales (basic)
from .scales import (
    scale_color_manual, scale_color_discrete, scale_color_continuous,
    scale_x_continuous, scale_y_continuous, scale_x_discrete, scale_y_discrete,
    scale_color_gradient, scale_color_gradient2,
    scale_fill_manual, scale_fill_discrete, scale_fill_continuous,
)

# Scales (viridis)
from .viridis import (
    scale_colour_viridis_c, scale_colour_viridis_d,
    scale_color_viridis_c, scale_color_viridis_d,
    scale_colour_viridis, scale_color_viridis,
    scale_fill_viridis_c, scale_fill_viridis_d, scale_fill_viridis,
)

# Scales (brewer)
from .brewer_scales import scale_colour_brewer, scale_color_brewer, scale_fill_brewer, display_brewer_palettes

# Facets
from .facets import facet_wrap, facet_grid

# Coordinate systems
from .coords import coord_cartesian, coord_fixed, coord_equal, coord_trans, coord_polar
from .coord_flip import coord_flip

# Position adjustments
from .positions import (
    position_identity, position_stack, position_fill, position_dodge,
    position_jitter, position_nudge, position_jitterdodge,
)

# Stats
from .stats import stat_smooth, stat_summary, geom_smooth_enhanced

# Utils
from .utils import labs, xlim, ylim


__version__ = "0.2.0"
__author__ = "Essi Parent"
__email__ = "essiparent@icloud.com"

__all__ = [
    # Core
    'ggplot', 'aes',
    # Geoms
    'geom_point', 'geom_line', 'geom_bar', 'geom_histogram', 'geom_smooth',
    'geom_area', 'geom_boxplot', 'geom_density', 'geom_tile', 'geom_raster',
    'geom_map', 'geom_ribbon', 'geom_violin', 'geom_text', 'geom_label',
    'geom_errorbar', 'geom_smooth_enhanced',
    'geom_text_repel', 'geom_label_repel',
    # Highlight
    'gghighlight',
    # Themes
    'theme_minimal', 'theme_classic', 'theme_bw', 'theme_dark', 'theme_void',
    'theme', 'element_blank', 'element_text', 'element_line', 'element_rect',
    'AdvancedTheme',
    # Scales
    'scale_color_manual', 'scale_color_discrete', 'scale_color_continuous',
    'scale_x_continuous', 'scale_y_continuous', 'scale_x_discrete', 'scale_y_discrete',
    'scale_color_gradient', 'scale_color_gradient2',
    'scale_fill_manual', 'scale_fill_discrete', 'scale_fill_continuous',
    'scale_colour_viridis_c', 'scale_colour_viridis_d',
    'scale_color_viridis_c', 'scale_color_viridis_d',
    'scale_colour_viridis', 'scale_color_viridis',
    'scale_fill_viridis_c', 'scale_fill_viridis_d', 'scale_fill_viridis',
    'scale_colour_brewer', 'scale_color_brewer', 'scale_fill_brewer',
    'display_brewer_palettes',
    # Facets
    'facet_wrap', 'facet_grid',
    # Coords
    'coord_cartesian', 'coord_fixed', 'coord_equal', 'coord_flip',
    'coord_trans', 'coord_polar',
    # Positions
    'position_identity', 'position_stack', 'position_fill', 'position_dodge',
    'position_jitter', 'position_nudge', 'position_jitterdodge',
    # Stats
    'stat_smooth', 'stat_summary',
    # Utils
    'labs', 'xlim', 'ylim',
]
