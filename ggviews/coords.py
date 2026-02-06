"""
Coordinate systems for ggviews

This module implements coordinate system transformations that control
how data is mapped to the plot area, including aspect ratios and transformations.
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List, Tuple
import warnings


class CoordSystem:
    """Base coordinate system class"""
    
    def __init__(self, **kwargs):
        self.params = kwargs
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this coordinate system to a ggplot object"""
        new_plot = ggplot_obj._copy()
        new_plot.coord_system = self
        return new_plot
    
    def _apply(self, plot, ggplot_obj):
        """Apply coordinate transformation - to be implemented by subclasses"""
        return plot


class coord_cartesian(CoordSystem):
    """Cartesian coordinate system (default)
    
    The standard coordinate system where x and y map directly to horizontal
    and vertical positions.
    
    Args:
        xlim: X-axis limits (min, max)
        ylim: Y-axis limits (min, max)
        expand: Whether to expand limits slightly beyond data range
        **kwargs: Additional parameters
    """
    
    def __init__(self, xlim=None, ylim=None, expand=True, **kwargs):
        super().__init__(**kwargs)
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
    
    def _apply(self, plot, ggplot_obj):
        """Apply cartesian coordinate system"""
        opts = {}
        
        if self.xlim is not None:
            opts['xlim'] = self.xlim
        if self.ylim is not None:
            opts['ylim'] = self.ylim
            
        if opts:
            return plot.opts(**opts)
        return plot


class coord_fixed(CoordSystem):
    """Fixed aspect ratio coordinate system
    
    Forces a fixed ratio between the physical representation of data units
    on the axes. This is useful for ensuring that one unit on the x-axis
    is the same length as one unit on the y-axis.
    
    Args:
        ratio: Aspect ratio (y/x). If 1, one unit on x-axis = one unit on y-axis
        xlim: X-axis limits (min, max) 
        ylim: Y-axis limits (min, max)
        expand: Whether to expand limits slightly beyond data range
        **kwargs: Additional parameters
        
    Examples:
        coord_fixed()  # ratio = 1 (equal scaling)
        coord_fixed(ratio=2)  # y-axis units are twice as long as x-axis units
    """
    
    def __init__(self, ratio=1, xlim=None, ylim=None, expand=True, **kwargs):
        super().__init__(**kwargs)
        self.ratio = ratio
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
    
    def _apply(self, plot, ggplot_obj):
        """Apply fixed aspect ratio coordinate system"""
        opts = {}
        
        # Set axis limits if provided
        if self.xlim is not None:
            opts['xlim'] = self.xlim
        if self.ylim is not None:
            opts['ylim'] = self.ylim
        
        # Apply aspect ratio
        # In holoviews, we can control aspect ratio through plot dimensions
        if hasattr(plot, 'opts'):
            # Calculate appropriate dimensions based on aspect ratio
            base_width = 500
            base_height = int(base_width * self.ratio)
            
            opts.update({
                'width': base_width,
                'height': base_height,
                'aspect': self.ratio,
                'data_aspect': self.ratio  # This forces equal scaling of data units
            })
        
        if opts:
            return plot.opts(**opts)
        return plot


class coord_equal(coord_fixed):
    """Equal aspect ratio coordinate system
    
    Convenience function for coord_fixed(ratio=1). Forces equal scaling
    so that one unit on the x-axis is the same length as one unit on the y-axis.
    This is particularly useful for maps, scatter plots where distances matter,
    or any plot where the relationship between x and y units is meaningful.
    
    Args:
        xlim: X-axis limits (min, max)
        ylim: Y-axis limits (min, max)
        expand: Whether to expand limits slightly beyond data range
        **kwargs: Additional parameters
        
    Example:
        coord_equal()  # Same as coord_fixed(ratio=1)
    """
    
    def __init__(self, xlim=None, ylim=None, expand=True, **kwargs):
        super().__init__(ratio=1, xlim=xlim, ylim=ylim, expand=expand, **kwargs)


# coord_flip is defined in coord_flip.py to avoid duplication


class coord_trans(CoordSystem):
    """Transformed coordinate system
    
    Applies transformations to the coordinate system, such as log scales.
    
    Args:
        x: Transformation for x-axis ('identity', 'log', 'log10', 'sqrt', etc.)
        y: Transformation for y-axis ('identity', 'log', 'log10', 'sqrt', etc.)
        xlim: X-axis limits (in transformed space)
        ylim: Y-axis limits (in transformed space)
        **kwargs: Additional parameters
    """
    
    def __init__(self, x='identity', y='identity', xlim=None, ylim=None, **kwargs):
        super().__init__(**kwargs)
        self.x_trans = x
        self.y_trans = y
        self.xlim = xlim
        self.ylim = ylim
    
    def _apply(self, plot, ggplot_obj):
        """Apply coordinate transformations"""
        opts = {}
        
        # Apply transformations
        if self.x_trans == 'log' or self.x_trans == 'log10':
            opts['logx'] = True
        if self.y_trans == 'log' or self.y_trans == 'log10':
            opts['logy'] = True
            
        # Set limits
        if self.xlim is not None:
            opts['xlim'] = self.xlim
        if self.ylim is not None:
            opts['ylim'] = self.ylim
            
        if opts:
            return plot.opts(**opts)
        return plot


class coord_polar(CoordSystem):
    """Polar coordinate system
    
    Maps x and y coordinates to angle and radius in a polar coordinate system.
    Useful for creating pie charts, radar charts, and other circular visualizations.
    
    Args:
        theta: Which aesthetic to map to angle ('x' or 'y')
        start: Starting angle (in radians)
        direction: Direction of angles (1 for counter-clockwise, -1 for clockwise)
        **kwargs: Additional parameters
    """
    
    def __init__(self, theta='x', start=0, direction=1, **kwargs):
        super().__init__(**kwargs)
        self.theta = theta
        self.start = start
        self.direction = direction
        
    def _apply(self, plot, ggplot_obj):
        """Apply polar coordinate transformation"""
        # This would require significant transformation of the underlying plot
        warnings.warn("coord_polar() not yet fully implemented. Consider using holoviews polar plots directly.")
        return plot


# Convenience functions that mirror ggplot2 API
def coord_quickmap():
    """Quick map projection (approximates coord_map for small areas)
    
    Provides a quick approximation of a map projection that works well
    for small areas where the earth's curvature is not a major factor.
    
    Returns:
        coord_fixed: Fixed coordinate system with appropriate aspect ratio
    """
    return coord_fixed(ratio=1)


# Export all coordinate system classes
__all__ = [
    'CoordSystem',
    'coord_cartesian',
    'coord_fixed', 
    'coord_equal',
    'coord_trans',
    'coord_polar',
    'coord_quickmap',
]