"""
Themes for ggviews

This module contains theme classes that control the overall
visual appearance of plots, similar to ggplot2 themes.
"""

import colorsys
import holoviews as hv
from typing import Dict, Any, Optional


class Theme:
    """Base theme class"""
    
    def __init__(self, **kwargs):
        self.options = kwargs
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this theme to a ggplot object"""
        new_plot = ggplot_obj._copy()
        new_plot.theme = self
        return new_plot
    
    def _apply(self, plot, ggplot_obj):
        """Apply theme to a plot - to be implemented by subclasses"""
        return plot.opts(**self.options)


class theme_minimal(Theme):
    """Minimal theme with clean appearance
    
    Similar to ggplot2's theme_minimal(), provides a clean look
    with minimal visual elements and grid lines.
    """
    
    def __init__(self, **kwargs):
        # Default minimal theme options
        default_options = {
            'width': 500,
            'height': 400,
            'bgcolor': 'white',
            'show_grid': True,
            'gridstyle': {
                'grid_line_color': '#E0E0E0',
                'grid_line_alpha': 0.5,
                'grid_line_width': 1
            },
            'show_frame': False,
            'toolbar': 'above',
            'tools': ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']
        }
        default_options.update(kwargs)
        super().__init__(**default_options)
    
    def _apply(self, plot, ggplot_obj):
        """Apply minimal theme styling"""
        options = self.options.copy()
        
        # Apply styling with single toolbar to prevent duplication
        try:
            styled_plot = plot.opts(
                width=options.pop('width', 500),
                height=options.pop('height', 400),
                bgcolor=options.pop('bgcolor', 'white'),
                show_grid=options.pop('show_grid', True),
                gridstyle=options.pop('gridstyle', {}),
                show_frame=options.pop('show_frame', False)
            )
            
            # Apply toolbar only at the overlay level to prevent duplication
            if hasattr(plot, '_obj_type') and 'Overlay' in str(type(plot)):
                styled_plot = styled_plot.opts(
                    toolbar='above',
                    shared_axes=False
                )
            else:
                styled_plot = styled_plot.opts(
                    toolbar='above',
                    tools=['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']
                )
            
            return styled_plot
            
        except Exception as e:
            # Fallback to basic styling if complex options fail
            return plot.opts(
                width=500,
                height=400
            )


class theme_classic(Theme):
    """Classic theme with traditional appearance
    
    Similar to ggplot2's theme_classic(), provides a traditional
    statistical graphics appearance with axis lines.
    """
    
    def __init__(self, **kwargs):
        default_options = {
            'width': 500,
            'height': 400,
            'bgcolor': 'white',
            'show_grid': False,
            'show_frame': True,
            'framewise': True,
            'toolbar': 'above',
            'tools': ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']
        }
        default_options.update(kwargs)
        super().__init__(**default_options)


class theme_bw(Theme):
    """Black and white theme
    
    Similar to ggplot2's theme_bw(), provides a clean black and white
    appearance with gray grid lines.
    """
    
    def __init__(self, **kwargs):
        default_options = {
            'width': 500,
            'height': 400,
            'bgcolor': 'white',
            'show_grid': True,
            'gridstyle': {
                'grid_line_color': '#CCCCCC',
                'grid_line_alpha': 0.8,
                'grid_line_width': 1
            },
            'show_frame': True,
            'framewise': True,
            'toolbar': 'above',
            'tools': ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']
        }
        default_options.update(kwargs)
        super().__init__(**default_options)


class theme_dark(Theme):
    """Dark theme for low-light environments
    
    Provides a dark background theme that's easier on the eyes
    in low-light conditions.
    """
    
    def __init__(self, **kwargs):
        default_options = {
            'width': 500,
            'height': 400,
            'bgcolor': '#2F2F2F',
            'show_grid': True,
            'gridstyle': {
                'grid_line_color': '#4F4F4F',
                'grid_line_alpha': 0.6,
                'grid_line_width': 1
            },
            'show_frame': False,
            'toolbar': 'above',
            'tools': ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']
        }
        default_options.update(kwargs)
        super().__init__(**default_options)
    
    def _apply(self, plot, ggplot_obj):
        """Apply dark theme with appropriate text colors"""
        opts = self.options.copy()

        styled_plot = plot.opts(
            width=opts.pop('width', 500),
            height=opts.pop('height', 400),
            bgcolor=opts.pop('bgcolor', '#2F2F2F'),
            show_grid=opts.pop('show_grid', True),
            gridstyle=opts.pop('gridstyle', {}),
            show_frame=opts.pop('show_frame', False),
            toolbar=opts.pop('toolbar', 'above'),
            tools=opts.pop('tools', ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']),
        )

        return styled_plot


class theme_void(Theme):
    """Void theme with no background elements
    
    Similar to ggplot2's theme_void(), removes all background
    elements for a completely clean appearance.
    """
    
    def __init__(self, **kwargs):
        default_options = {
            'width': 500,
            'height': 400,
            'bgcolor': 'white',
            'show_grid': False,
            'show_frame': False,
            'xaxis': None,
            'yaxis': None,
            'toolbar': None,
            'tools': []
        }
        default_options.update(kwargs)
        super().__init__(**default_options)


# ── Essi palette: colorblind-safe (Krzywinski/BCGSC) ──────────────────────────

# Core 8 colors from mk.bcgsc.ca "8-color palette for color blindness"
# (black excluded — used for text/axes, not data encoding)
_ESSI_BASE = [
    '#2271B2',  # honolulu blue
    '#3DB7E9',  # summer sky
    '#F748A5',  # barbie pink
    '#359B73',  # ocean green
    '#D55E00',  # bamboo
    '#E69F00',  # gamboge
    '#F0E442',  # paris daisy
    '#000000',  # black (last resort)
]


def _hex_to_hsl(hex_color):
    """Convert #RRGGBB to (H, S, L) in [0,1]."""
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def _hsl_to_hex(h, s, l):
    """Convert (H, S, L) in [0,1] to #RRGGBB."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#{:02X}{:02X}{:02X}'.format(
        max(0, min(255, round(r * 255))),
        max(0, min(255, round(g * 255))),
        max(0, min(255, round(b * 255))),
    )


def palette_essi(n=8):
    """Return *n* colorblind-safe colors from the Essi palette.

    * n <= 8 — returns distinct colors from the BCGSC base palette.
    * n  > 8 — generates additional colors by interpolating in HSL
      space between adjacent base hues, then shifting lightness to
      maintain perceptual contrast.  The first 7 base colors are
      always preserved so they remain visually anchored.

    Parameters
    ----------
    n : int
        Number of colors to return.

    Returns
    -------
    list[str]
        Hex color strings.
    """
    if n <= 0:
        return []
    if n <= len(_ESSI_BASE):
        return _ESSI_BASE[:n]

    # Start with the first 7 non-black base colors
    base = _ESSI_BASE[:7]
    base_hsl = [_hex_to_hsl(c) for c in base]
    extras_needed = n - len(base)

    # Generate extras by rotating hue and alternating lightness
    extra = []
    for i in range(extras_needed):
        # Pick a base color to derive from (round-robin)
        src_h, src_s, src_l = base_hsl[i % len(base_hsl)]
        # Shift hue slightly and alternate lightness
        h_shift = 0.04 * ((i // len(base_hsl)) + 1)
        l_shift = 0.12 if (i % 2 == 0) else -0.10
        new_h = (src_h + h_shift) % 1.0
        new_s = max(0.3, min(1.0, src_s))
        new_l = max(0.25, min(0.75, src_l + l_shift))
        extra.append(_hsl_to_hex(new_h, new_s, new_l))

    return base + extra


class theme_essi(Theme):
    """Essi theme — modern, warm, colorblind-friendly.

    * **Background**: pale beige (#FAF6F1), inspired by Anthropic's brand.
    * **Grid**: subtle warm gray, low alpha.
    * **Palette**: Krzywinski / BCGSC 8-color colorblind-safe palette,
      expandable to any number of colors via ``palette_essi(n)``.
    * **Typography**: clean, no bold frames.

    Examples
    --------
    >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_essi()
    """

    def __init__(self, **kwargs):
        default_options = {
            'width': 500,
            'height': 400,
            'bgcolor': '#FAF6F1',       # pale beige
            'show_grid': True,
            'gridstyle': {
                # Major grid: thin white lines (ggplot2 default style)
                'grid_line_color': 'white',
                'grid_line_width': 1.4,
                'grid_line_alpha': 1.0,
                # Minor grid: even thinner white lines
                'minor_grid_line_color': 'white',
                'minor_grid_line_width': 0.6,
                'minor_grid_line_alpha': 0.7,
            },
            'show_frame': False,
            'toolbar': 'above',
            'tools': ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save'],
        }
        default_options.update(kwargs)
        super().__init__(**default_options)

    def _add_to_ggplot(self, ggplot_obj):
        """Add theme and immediately swap the color palette."""
        new_plot = super()._add_to_ggplot(ggplot_obj)
        new_plot.default_colors = palette_essi(max(len(new_plot.default_colors), 8))
        return new_plot

    def _apply(self, plot, ggplot_obj):
        """Apply the Essi theme styling."""
        opts = self.options.copy()

        try:
            styled_plot = plot.opts(
                width=opts.pop('width', 500),
                height=opts.pop('height', 400),
                bgcolor=opts.pop('bgcolor', '#FAF6F1'),
                show_grid=opts.pop('show_grid', True),
                gridstyle=opts.pop('gridstyle', {}),
                show_frame=opts.pop('show_frame', False),
            )

            styled_plot = styled_plot.opts(
                toolbar=opts.pop('toolbar', 'above'),
                tools=opts.pop('tools', []),
            )

            return styled_plot

        except Exception:
            return plot.opts(width=500, height=400)


# Custom theme builder
def theme(**kwargs):
    """Create a custom theme with specified options
    
    Args:
        **kwargs: Theme options to customize
        
    Returns:
        Theme: Custom theme object
        
    Example:
        custom_theme = theme(
            width=600,
            height=400,
            bgcolor='#F5F5F5',
            show_grid=True
        )
    """
    return Theme(**kwargs)


# Export all theme classes
__all__ = [
    'Theme',
    'theme_minimal',
    'theme_classic',
    'theme_bw',
    'theme_dark',
    'theme_void',
    'theme_essi',
    'palette_essi',
    'theme',
]