"""
Scales for ggviews

This module contains scale classes that control how data values
are mapped to visual aesthetics (colors, sizes, positions, etc.)
"""

import holoviews as hv
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Union, List
import warnings
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap


class Scale:
    """Base scale class"""
    
    def __init__(self, aesthetic, **kwargs):
        self.aesthetic = aesthetic  # Which aesthetic this scale applies to
        self.params = kwargs
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this scale to a ggplot object"""
        new_plot = ggplot_obj._copy()
        new_plot.scales[self.aesthetic] = self
        return new_plot
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply scale transformation - to be implemented by subclasses"""
        return plot


class scale_color_manual(Scale):
    """Manual color scale
    
    Allows you to manually specify colors for discrete values.
    
    Args:
        values: List or dict of colors to use
        name: Name for the legend
        labels: Custom labels for legend
        **kwargs: Additional parameters
        
    Example:
        scale_color_manual(values=['red', 'blue', 'green'])
        scale_color_manual(values={'A': 'red', 'B': 'blue'})
    """
    
    def __init__(self, values=None, name=None, labels=None, **kwargs):
        super().__init__('color', **kwargs)
        self.values = values
        self.name = name
        self.labels = labels
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply manual color mapping"""
        if self.values is None:
            return plot
            
        # This would be applied during geom rendering
        # Store the color mapping in the ggplot object
        if isinstance(self.values, dict):
            ggplot_obj.color_mapping = self.values
        elif isinstance(self.values, list):
            # Create mapping based on unique values in data
            if hasattr(ggplot_obj, 'mapping') and 'color' in ggplot_obj.mapping.mappings:
                color_col = ggplot_obj.mapping.mappings['color']
                if color_col in data.columns:
                    unique_vals = data[color_col].unique()
                    n_vals = len(unique_vals)
                    colors = self.values[:n_vals] if n_vals <= len(self.values) else self.values * ((n_vals // len(self.values)) + 1)
                    ggplot_obj.color_mapping = dict(zip(unique_vals, colors[:n_vals]))
        
        return plot


class scale_color_discrete(Scale):
    """Discrete color scale using default ggplot2 colors
    
    Uses the default ggplot2 color palette for discrete variables.
    
    Args:
        name: Name for the legend
        labels: Custom labels for legend  
        **kwargs: Additional parameters
    """
    
    def __init__(self, name=None, labels=None, **kwargs):
        super().__init__('color', **kwargs)
        self.name = name
        self.labels = labels
        
        # ggplot2 default colors
        self.default_colors = [
            '#F8766D',  # Red
            '#00BFC4',  # Cyan
            '#7CAE00',  # Green
            '#C77CFF',  # Purple
            '#FF61CC',  # Pink
            '#00B4F0',  # Blue
            '#FFAA00',  # Orange
            '#FF4B4B',  # Light red
        ]
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply discrete color scale"""
        # Use default colors - this gets applied during geom rendering
        ggplot_obj.default_colors = self.default_colors
        return plot


class scale_color_continuous(Scale):
    """Continuous color scale
    
    Maps continuous values to colors using a color gradient.
    
    Args:
        low: Color for low values
        high: Color for high values
        mid: Color for middle values (creates 3-color gradient)
        name: Name for the legend
        trans: Transformation ('identity', 'log', 'sqrt')
        **kwargs: Additional parameters
    """
    
    def __init__(self, low='#132B43', high='#56B1F7', mid=None, name=None, trans='identity', **kwargs):
        super().__init__('color', **kwargs)
        self.low = low
        self.high = high
        self.mid = mid
        self.name = name
        self.trans = trans
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply continuous color scale"""
        # Create color mapping based on data range
        if hasattr(ggplot_obj, 'mapping') and 'color' in ggplot_obj.mapping.mappings:
            color_col = ggplot_obj.mapping.mappings['color']
            if color_col in data.columns:
                values = data[color_col]
                
                if self.mid is not None:
                    # 3-color gradient
                    colors = [self.low, self.mid, self.high]
                    cmap = LinearSegmentedColormap.from_list('custom', colors)
                else:
                    # 2-color gradient  
                    colors = [self.low, self.high]
                    cmap = LinearSegmentedColormap.from_list('custom', colors)
                
                # Normalize values to [0, 1]
                if self.trans == 'log':
                    values = np.log(values + 1e-10)  # Avoid log(0)
                elif self.trans == 'sqrt':
                    values = np.sqrt(np.abs(values))
                
                vmin, vmax = values.min(), values.max()
                if vmax > vmin:
                    normalized = (values - vmin) / (vmax - vmin)
                    colors = [cmap(val) for val in normalized]
                    
                    # Convert to hex colors
                    hex_colors = ['#%02x%02x%02x' % tuple(int(c*255) for c in color[:3]) for color in colors]
                    ggplot_obj.continuous_color_map = dict(zip(values.index, hex_colors))
        
        return plot


class scale_x_continuous(Scale):
    """Continuous x-axis scale
    
    Controls the x-axis for continuous variables.
    
    Args:
        name: Axis label
        breaks: Tick mark positions
        labels: Tick mark labels
        limits: Axis limits (min, max)
        trans: Transformation ('identity', 'log', 'sqrt')
        **kwargs: Additional parameters
    """
    
    def __init__(self, name=None, breaks=None, labels=None, limits=None, trans='identity', **kwargs):
        super().__init__('x', **kwargs)
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.limits = limits
        self.trans = trans
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply x-axis scale -- stores config on ggplot_obj for later application"""
        if self.name is not None:
            ggplot_obj.labels.setdefault('x', self.name)
        if self.limits is not None:
            ggplot_obj.limits['x'] = self.limits
        return plot


class scale_y_continuous(Scale):
    """Continuous y-axis scale
    
    Controls the y-axis for continuous variables.
    
    Args:
        name: Axis label
        breaks: Tick mark positions
        labels: Tick mark labels  
        limits: Axis limits (min, max)
        trans: Transformation ('identity', 'log', 'sqrt')
        **kwargs: Additional parameters
    """
    
    def __init__(self, name=None, breaks=None, labels=None, limits=None, trans='identity', **kwargs):
        super().__init__('y', **kwargs)
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.limits = limits
        self.trans = trans
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply y-axis scale -- stores config on ggplot_obj for later application"""
        if self.name is not None:
            ggplot_obj.labels.setdefault('y', self.name)
        if self.limits is not None:
            ggplot_obj.limits['y'] = self.limits
        return plot


class scale_x_discrete(Scale):
    """Discrete x-axis scale
    
    Controls the x-axis for categorical/discrete variables.
    
    Args:
        name: Axis label
        labels: Custom labels for categories
        limits: Which categories to include/order
        **kwargs: Additional parameters
    """
    
    def __init__(self, name=None, labels=None, limits=None, **kwargs):
        super().__init__('x', **kwargs)
        self.name = name
        self.labels = labels
        self.limits = limits
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply x-axis discrete scale -- stores config on ggplot_obj"""
        if self.name is not None:
            ggplot_obj.labels.setdefault('x', self.name)
        return plot


class scale_y_discrete(Scale):
    """Discrete y-axis scale
    
    Controls the y-axis for categorical/discrete variables.
    
    Args:
        name: Axis label
        labels: Custom labels for categories
        limits: Which categories to include/order
        **kwargs: Additional parameters
    """
    
    def __init__(self, name=None, labels=None, limits=None, **kwargs):
        super().__init__('y', **kwargs)
        self.name = name
        self.labels = labels
        self.limits = limits
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply y-axis discrete scale -- stores config on ggplot_obj"""
        if self.name is not None:
            ggplot_obj.labels.setdefault('y', self.name)
        return plot


# Additional scale functions
def scale_color_gradient(low='#132B43', high='#56B1F7', **kwargs):
    """Create a 2-color gradient scale
    
    Args:
        low: Color for low values
        high: Color for high values
        **kwargs: Additional parameters passed to scale_color_continuous
    """
    return scale_color_continuous(low=low, high=high, **kwargs)


def scale_color_gradient2(low='#132B43', mid='#FFFFFF', high='#56B1F7', midpoint=None, **kwargs):
    """Create a 3-color diverging gradient scale
    
    Args:
        low: Color for low values
        mid: Color for middle values  
        high: Color for high values
        midpoint: Data value for middle color
        **kwargs: Additional parameters passed to scale_color_continuous
    """
    return scale_color_continuous(low=low, mid=mid, high=high, **kwargs)


def scale_fill_manual(*args, **kwargs):
    """Manual fill scale - alias for scale_color_manual for fill aesthetic"""
    scale = scale_color_manual(*args, **kwargs)
    scale.aesthetic = 'fill'
    return scale


def scale_fill_discrete(*args, **kwargs):
    """Discrete fill scale - alias for scale_color_discrete for fill aesthetic"""
    scale = scale_color_discrete(*args, **kwargs)
    scale.aesthetic = 'fill'  
    return scale


def scale_fill_continuous(*args, **kwargs):
    """Continuous fill scale - alias for scale_color_continuous for fill aesthetic"""
    scale = scale_color_continuous(*args, **kwargs)
    scale.aesthetic = 'fill'
    return scale


# Export all scale classes
__all__ = [
    'Scale',
    'scale_color_manual',
    'scale_color_discrete', 
    'scale_color_continuous',
    'scale_x_continuous',
    'scale_y_continuous',
    'scale_x_discrete',
    'scale_y_discrete',
    'scale_color_gradient',
    'scale_color_gradient2',
    'scale_fill_manual',
    'scale_fill_discrete',
    'scale_fill_continuous',
]