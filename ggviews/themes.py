"""
Themes for ggviews

This module contains theme classes that control the overall
visual appearance of plots, similar to ggplot2 themes.
"""

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
        opts = self.options.copy()
        
        # Apply styling with proper holoviews options management
        styled_plot = plot.opts(
            opts.Scatter(
                width=opts.pop('width', 500),
                height=opts.pop('height', 400),
                bgcolor=opts.pop('bgcolor', 'white'),
                show_grid=opts.pop('show_grid', True),
                gridstyle=opts.pop('gridstyle', {}),
                show_frame=opts.pop('show_frame', False),
                tools=opts.pop('tools', ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save'])
            ),
            opts.Overlay(
                width=opts.pop('width', 500),
                height=opts.pop('height', 400),
                toolbar=opts.pop('toolbar', 'above')
            )
        )
        
        return styled_plot


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
        
        # Apply dark styling - use all keyword arguments
        styled_plot = plot.opts(
            width=opts.pop('width', 500),
            height=opts.pop('height', 400),
            bgcolor=opts.pop('bgcolor', '#2F2F2F'),
            show_grid=opts.pop('show_grid', True),
            gridstyle=opts.pop('gridstyle', {}),
            show_frame=opts.pop('show_frame', False),
            toolbar=opts.pop('toolbar', 'above'),
            tools=opts.pop('tools', ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']),
            # Text colors for dark theme
            fontcolor='white',
            **opts
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
    'theme',
]