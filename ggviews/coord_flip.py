"""
Coordinate flipping for ggviews
"""

import holoviews as hv
import pandas as pd
from .coords import CoordSystem

class coord_flip(CoordSystem):
    """Flip cartesian coordinates
    
    Flips the x and y axes, making horizontal plots from vertical ones.
    Very useful for creating horizontal bar charts, box plots, etc.
    
    Args:
        xlim: Limits for x-axis (after flipping - originally y-axis)
        ylim: Limits for y-axis (after flipping - originally x-axis)
        expand: Whether to expand limits to include data
        
    Examples:
        # Horizontal bar chart
        ggplot(df, aes(x='category', y='value')).geom_bar() + coord_flip()
        
        # Horizontal boxplot  
        ggplot(df, aes(x='group', y='value')).geom_boxplot() + coord_flip()
        
        # With custom limits
        coord_flip(xlim=[0, 100], ylim=['A', 'B', 'C'])
    """
    
    def __init__(self, xlim=None, ylim=None, expand=True):
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
    
    def _apply(self, plot, ggplot_obj, data=None):
        """Apply coordinate flipping to the plot"""
        
        if plot is None:
            return None
        
        # For holoviews, we can use the invert_axes option
        try:
            # Apply inversion to flip x and y axes
            flipped_plot = plot.opts(invert_axes=True)
            
            # Apply custom limits if specified
            opts_kwargs = {}
            
            # Note: limits are applied to the flipped axes
            # xlim becomes ylim after flipping, ylim becomes xlim after flipping
            if self.ylim is not None:  # This becomes xlim after flip
                opts_kwargs['xlim'] = self.ylim
            if self.xlim is not None:  # This becomes ylim after flip  
                opts_kwargs['ylim'] = self.xlim
            
            if opts_kwargs:
                flipped_plot = flipped_plot.opts(**opts_kwargs)
            
            return flipped_plot
            
        except Exception:
            # Fallback: manually swap data if invert_axes doesn't work
            return self._manual_flip(plot, ggplot_obj, data)
    
    def _manual_flip(self, plot, ggplot_obj, data):
        """Manual coordinate flipping by swapping data"""
        
        # This is more complex and would require accessing the underlying data
        # For now, try to use holoviews transformation
        try:
            # Use holoviews dimension transformation
            if hasattr(plot, 'redim'):
                # Swap the dimension names/roles
                flipped = plot.redim(x='temp', y='x', temp='y')
                return flipped
            else:
                return plot
        except:
            # Last resort - return original plot
            return plot
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this coordinate system to a ggplot object"""
        ggplot_obj.coord = self
        return ggplot_obj


# Export
__all__ = ['coord_flip']