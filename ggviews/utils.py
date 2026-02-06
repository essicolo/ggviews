"""
Utility functions for ggviews

This module contains helper functions and utilities used throughout ggviews.
"""

from typing import Dict, Any, Optional, Union, List, Tuple
import warnings


class UtilityLayer:
    """Base class for utility layers like labs, xlim, ylim"""
    
    def __init__(self, **kwargs):
        self.params = kwargs
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this utility to a ggplot object"""
        new_plot = ggplot_obj._copy()
        self._apply_to_ggplot(new_plot)
        return new_plot
    
    def _apply_to_ggplot(self, ggplot_obj):
        """Apply utility to ggplot object - to be implemented by subclasses"""
        pass


class labs(UtilityLayer):
    """Add labels to plots
    
    Sets axis labels, plot title, subtitle, and caption.
    
    Args:
        title: Plot title
        subtitle: Plot subtitle  
        caption: Plot caption
        x: X-axis label
        y: Y-axis label
        color: Legend title for color aesthetic
        colour: Alias for color (British spelling)
        fill: Legend title for fill aesthetic
        size: Legend title for size aesthetic
        alpha: Legend title for alpha aesthetic
        **kwargs: Additional label mappings
        
    Example:
        labs(title="My Plot", x="Height", y="Weight", color="Species")
    """
    
    def __init__(self, title=None, subtitle=None, caption=None, x=None, y=None, 
                 color=None, colour=None, fill=None, size=None, alpha=None, **kwargs):
        params = {}
        
        if title is not None:
            params['title'] = title
        if subtitle is not None:
            params['subtitle'] = subtitle  
        if caption is not None:
            params['caption'] = caption
        if x is not None:
            params['x'] = x
        if y is not None:
            params['y'] = y
            
        # Handle color/colour
        color_val = color or colour
        if color_val is not None:
            params['color'] = color_val
            
        if fill is not None:
            params['fill'] = fill
        if size is not None:
            params['size'] = size
        if alpha is not None:
            params['alpha'] = alpha
            
        # Handle additional labels
        params.update(kwargs)
        
        super().__init__(**params)
    
    def _apply_to_ggplot(self, ggplot_obj):
        """Apply labels to ggplot object"""
        ggplot_obj.labels.update(self.params)


class xlim(UtilityLayer):
    """Set x-axis limits
    
    Args:
        *args: Either (min, max) or a single list/tuple of (min, max)
        
    Examples:
        xlim(0, 100)
        xlim([0, 100])
        xlim((0, 100))
    """
    
    def __init__(self, *args):
        if len(args) == 1:
            # Single argument - should be list/tuple
            if isinstance(args[0], (list, tuple)) and len(args[0]) == 2:
                limits = args[0]
            else:
                raise ValueError("xlim expects either (min, max) or a single (min, max) tuple/list")
        elif len(args) == 2:
            # Two arguments - min and max
            limits = args
        else:
            raise ValueError("xlim expects either (min, max) or a single (min, max) tuple/list")
        
        super().__init__(limits=limits)
    
    def _apply_to_ggplot(self, ggplot_obj):
        """Apply x-axis limits to ggplot object"""
        ggplot_obj.limits['x'] = self.params['limits']


class ylim(UtilityLayer):
    """Set y-axis limits
    
    Args:
        *args: Either (min, max) or a single list/tuple of (min, max)
        
    Examples:
        ylim(0, 100)
        ylim([0, 100])
        ylim((0, 100))
    """
    
    def __init__(self, *args):
        if len(args) == 1:
            # Single argument - should be list/tuple
            if isinstance(args[0], (list, tuple)) and len(args[0]) == 2:
                limits = args[0]
            else:
                raise ValueError("ylim expects either (min, max) or a single (min, max) tuple/list")
        elif len(args) == 2:
            # Two arguments - min and max
            limits = args
        else:
            raise ValueError("ylim expects either (min, max) or a single (min, max) tuple/list")
        
        super().__init__(limits=limits)
    
    def _apply_to_ggplot(self, ggplot_obj):
        """Apply y-axis limits to ggplot object"""
        ggplot_obj.limits['y'] = self.params['limits']


def expand_limits(**kwargs):
    """Expand the plot limits to include additional values
    
    Args:
        x: Expand x-axis to include these values
        y: Expand y-axis to include these values
        **kwargs: Additional limits to expand
        
    Example:
        expand_limits(x=0, y=c(0, 100))
    """
    return UtilityLayer(**kwargs)


def guides(**kwargs):
    """Control legend guides
    
    Args:
        color: Control color legend ('legend', 'colorbar', None)
        colour: Alias for color
        fill: Control fill legend
        size: Control size legend
        alpha: Control alpha legend
        **kwargs: Additional guide specifications
        
    Example:
        guides(color='none')  # Remove color legend
        guides(fill=guide_legend(title='Species'))
    """
    # Handle color/colour alias
    if 'colour' in kwargs and 'color' not in kwargs:
        kwargs['color'] = kwargs.pop('colour')
    
    guide_layer = UtilityLayer(**kwargs)
    
    def apply_guides(ggplot_obj):
        # Store guide specifications
        if not hasattr(ggplot_obj, 'guides'):
            ggplot_obj.guides = {}
        ggplot_obj.guides.update(kwargs)
    
    guide_layer._apply_to_ggplot = apply_guides
    return guide_layer


def guide_legend(title=None, **kwargs):
    """Create a legend guide
    
    Args:
        title: Legend title
        **kwargs: Additional legend parameters
        
    Example:
        guides(color=guide_legend(title='Species'))
    """
    params = {'type': 'legend'}
    if title is not None:
        params['title'] = title
    params.update(kwargs)
    return params


def guide_colorbar(title=None, **kwargs):
    """Create a colorbar guide
    
    Args:
        title: Colorbar title
        **kwargs: Additional colorbar parameters
        
    Example:
        guides(color=guide_colorbar(title='Value'))
    """
    params = {'type': 'colorbar'}
    if title is not None:
        params['title'] = title
    params.update(kwargs)
    return params


# Convenience functions that mirror R's c() function
def c(*args):
    """Combine values into a list (R-style c() function)
    
    Args:
        *args: Values to combine
        
    Returns:
        list: Combined values
        
    Example:
        c(1, 2, 3)  # Returns [1, 2, 3]
        c('a', 'b', 'c')  # Returns ['a', 'b', 'c']
    """
    return list(args)


def seq(start, stop, step=1):
    """Generate a sequence of numbers
    
    Args:
        start: Starting value
        stop: Ending value (inclusive)
        step: Step size
        
    Returns:
        list: Sequence of numbers
        
    Example:
        seq(1, 10)  # [1, 2, 3, ..., 10]
        seq(0, 1, 0.1)  # [0, 0.1, 0.2, ..., 1.0]
    """
    import numpy as np
    return np.arange(start, stop + step/2, step).tolist()


def rep(x, times):
    """Repeat elements
    
    Args:
        x: Value or list to repeat
        times: Number of times to repeat
        
    Returns:
        list: Repeated values
        
    Example:
        rep('a', 3)  # ['a', 'a', 'a']
        rep([1, 2], 2)  # [1, 2, 1, 2]
    """
    if isinstance(x, list):
        return x * times
    else:
        return [x] * times


# Data manipulation helpers
def cut(x, breaks, labels=None):
    """Cut continuous variable into discrete bins
    
    Args:
        x: Continuous values to cut
        breaks: Break points or number of breaks
        labels: Labels for the bins
        
    Returns:
        pandas.Categorical: Binned values
        
    Example:
        cut(df['age'], breaks=5)
        cut(df['score'], breaks=[0, 50, 80, 100], labels=['Low', 'Medium', 'High'])
    """
    import pandas as pd
    return pd.cut(x, bins=breaks, labels=labels)


# Export all utility functions
__all__ = [
    'UtilityLayer',
    'labs',
    'xlim',
    'ylim',
    'expand_limits',
    'guides',
    'guide_legend',
    'guide_colorbar',
    'c',
    'seq',
    'rep',
    'cut',
]