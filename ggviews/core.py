"""
Core classes for ggviews: ggplot and aes
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List
import warnings

# Set holoviews backend
try:
    hv.extension('bokeh')
except:
    # Fallback to matplotlib if bokeh is not available
    hv.extension('matplotlib')


class aes:
    """Aesthetic mappings for ggplot
    
    Maps data variables to visual properties like x, y, color, size, etc.
    
    Args:
        x: Variable for x-axis
        y: Variable for y-axis  
        color: Variable for color mapping
        colour: Alias for color (British spelling)
        size: Variable for size mapping
        alpha: Variable for alpha/transparency mapping
        shape: Variable for shape mapping
        fill: Variable for fill color mapping
        linetype: Variable for line type mapping
        **kwargs: Additional aesthetic mappings
    """
    
    def __init__(self, x=None, y=None, color=None, colour=None, size=None, 
                 alpha=None, shape=None, fill=None, linetype=None, **kwargs):
        self.mappings = {}
        
        # Handle x and y
        if x is not None:
            self.mappings['x'] = x
        if y is not None:
            self.mappings['y'] = y
            
        # Handle color/colour
        color_val = color or colour
        if color_val is not None:
            self.mappings['color'] = color_val
            
        # Handle other aesthetics
        if size is not None:
            self.mappings['size'] = size
        if alpha is not None:
            self.mappings['alpha'] = alpha
        if shape is not None:
            self.mappings['shape'] = shape
        if fill is not None:
            self.mappings['fill'] = fill
        if linetype is not None:
            self.mappings['linetype'] = linetype
            
        # Handle additional mappings
        for k, v in kwargs.items():
            self.mappings[k] = v
    
    def __repr__(self):
        mappings_str = ', '.join([f"{k}='{v}'" for k, v in self.mappings.items()])
        return f"aes({mappings_str})"


class ggplot:
    """Main ggplot class for creating grammar of graphics plots
    
    This is the entry point for all ggplot-style visualizations.
    Use method chaining to build up your plot layer by layer.
    
    Args:
        data: pandas DataFrame containing the data to plot
        mapping: aes object defining default aesthetic mappings
    
    Example:
        ggplot(df, aes(x='x', y='y')).geom_point()
    """
    
    def __init__(self, data=None, mapping=None):
        self.data = data
        self.mapping = mapping or aes()
        self.layers = []
        self.scales = {}
        self.theme = None
        self.facets = None
        self.labels = {}
        self.limits = {}
        
        # Default theme colors (ggplot2-like)
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
        
        # Validate data
        if data is not None and not isinstance(data, pd.DataFrame):
            raise ValueError("data must be a pandas DataFrame")
    
    def __add__(self, other):
        """Add layers, themes, scales etc using + operator"""
        if hasattr(other, '_add_to_ggplot'):
            return other._add_to_ggplot(self)
        else:
            # Default behavior for backwards compatibility
            new_plot = self._copy()
            if hasattr(other, 'geom_type'):
                new_plot.layers.append(other)
            return new_plot
    
    def _copy(self):
        """Create a copy of the ggplot object"""
        new_plot = ggplot(self.data, self.mapping)
        new_plot.layers = self.layers.copy()
        new_plot.scales = self.scales.copy()
        new_plot.theme = self.theme
        new_plot.facets = self.facets
        new_plot.labels = self.labels.copy()
        new_plot.limits = self.limits.copy()
        return new_plot
    
    def _get_data_for_layer(self, layer_data=None):
        """Get data for a layer, with layer data taking precedence"""
        if layer_data is not None:
            return layer_data
        elif self.data is not None:
            return self.data
        else:
            raise ValueError("No data available. Provide data to ggplot() or individual layers.")
    
    def _combine_aesthetics(self, layer_aes=None):
        """Combine plot-level and layer-level aesthetics"""
        combined = aes()
        
        # Start with plot-level aesthetics
        if self.mapping:
            combined.mappings.update(self.mapping.mappings)
            
        # Override with layer-level aesthetics
        if layer_aes:
            combined.mappings.update(layer_aes.mappings)
            
        return combined
    
    def _render(self):
        """Render the plot using holoviews"""
        if not self.layers:
            warnings.warn("No layers added to plot")
            return hv.Scatter([]).opts(width=400, height=300)
        
        plots = []
        
        for layer in self.layers:
            layer_data = self._get_data_for_layer(layer.data)
            combined_aes = self._combine_aesthetics(layer.mapping)
            
            # Render layer
            layer_plot = layer._render(layer_data, combined_aes, self)
            if layer_plot is not None:
                plots.append(layer_plot)
        
        if not plots:
            return hv.Scatter([]).opts(width=400, height=300)
        
        # Combine all plots
        final_plot = plots[0]
        for plot in plots[1:]:
            final_plot = final_plot * plot
        
        # Apply theme
        if self.theme:
            final_plot = self.theme._apply(final_plot, self)
        else:
            # Apply default styling
            final_plot = final_plot.opts(
                width=500, height=400,
                show_grid=True,
                gridstyle={'grid_line_alpha': 0.3}
            )
        
        # Apply labels
        if self.labels:
            opts = {}
            if 'title' in self.labels:
                opts['title'] = self.labels['title']
            if 'x' in self.labels:
                opts['xlabel'] = self.labels['x']
            if 'y' in self.labels:
                opts['ylabel'] = self.labels['y']
            if opts:
                final_plot = final_plot.opts(**opts)
        
        # Apply limits
        if 'x' in self.limits:
            final_plot = final_plot.opts(xlim=self.limits['x'])
        if 'y' in self.limits:
            final_plot = final_plot.opts(ylim=self.limits['y'])
        
        # Apply facets
        if self.facets:
            final_plot = self.facets._apply(final_plot, self)
        
        return final_plot
    
    def show(self):
        """Display the plot"""
        plot = self._render()
        return plot
    
    def _repr_mimebundle_(self, include=None, exclude=None):
        """For Jupyter notebook display"""
        plot = self._render()
        return plot._repr_mimebundle_(include, exclude)
    
    def __repr__(self):
        return f"<ggplot: {len(self.layers)} layers>"
    
    # Convenience methods
    def labs(self, title=None, x=None, y=None, **kwargs):
        """Add labels to the plot"""
        from .utils import labs
        return labs(title=title, x=x, y=y, **kwargs)._add_to_ggplot(self)
    
    def xlim(self, *args):
        """Set x-axis limits"""  
        from .utils import xlim
        return xlim(*args)._add_to_ggplot(self)
    
    def ylim(self, *args):
        """Set y-axis limits"""
        from .utils import ylim
        return ylim(*args)._add_to_ggplot(self)