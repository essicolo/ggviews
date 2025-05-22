"""
Core functionality for ggviews.

This module contains the core classes and functions for ggviews.
"""

from __future__ import annotations

import pandas as pd
import holoviews as hv
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple, Type, Callable

from .aes import Aesthetics, aes
from .facets.wrap import facet_wrap as _facet_wrap


class GGPlot:
    def _store_for_faceting(self, plot):
        # Attach layers and mapping to the plot element for faceting
        plot._gv_layers = self.layers
        plot._gv_mapping = self.mapping
        return plot
    """Main class for creating plots using the grammar of graphics.
    
    Parameters
    ----------
    data : pandas.DataFrame
        The data to plot.
    mapping : Aesthetics, optional
        Aesthetic mappings from data variables to visual attributes.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ... )
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        mapping: Optional[Aesthetics] = None,    ):
        self.data = data
        self.mapping = mapping or Aesthetics()
        self.layers = []
        self.scales = []
        self.facets = None
        self.coords = None
        self._theme = None
        self.labels = {}
        
    def add_layer(self, layer) -> GGPlot:
        """Add a layer to the plot.
        
        Parameters
        ----------
        layer : Layer
            The layer to add.
        
        Returns
        -------
        GGPlot
            The plot object with the layer added.
        """
        self.layers.append(layer)
        return self
    
    def add_scale(self, scale) -> GGPlot:
        """Add a scale to the plot.
        
        Parameters
        ----------
        scale : Scale
            The scale to add.
        
        Returns
        -------
        GGPlot
            The plot object with the scale added.
        """
        self.scales.append(scale)
        return self
    
    def facet(self, facet) -> GGPlot:
        """Set the faceting for the plot.
        
        Parameters
        ----------
        facet : Facet
            The facet specification.
        
        Returns
        -------
        GGPlot
            The plot object with faceting set.
        """
        self.facets = facet
        return self
    
    def facet_wrap(self, facets, nrow=None, ncol=None, scales='fixed') -> GGPlot:
        """Shorthand to apply wrap faceting by passing directly facet variables."""
        # Use ggviews.facet_wrap to construct a FacetWrap and set it
        return self.facet(_facet_wrap(facets=facets, nrow=nrow, ncol=ncol, scales=scales))
    
    def coord(self, coord) -> GGPlot:
        """Set the coordinate system for the plot.
        
        Parameters
        ----------
        coord : CoordinateSystem
            The coordinate system.
        
        Returns
        -------
        GGPlot
            The plot object with the coordinate system set.
        """
        self.coords = coord
        return self
    
    def theme(self, theme_obj) -> GGPlot:
        """Set the theme for the plot.
        
        Parameters
        ----------
        theme_obj : Theme
            The theme to use.
        
        Returns
        -------
        GGPlot
            The plot object with the theme set.
        """
        self._theme = theme_obj
        return self
    
    def labs(self, title=None, subtitle=None, caption=None, 
             x=None, y=None, **kwargs) -> GGPlot:
        """Set the labels for the plot.
        
        Parameters
        ----------
        title : str, optional
            The title of the plot.
        subtitle : str, optional
            The subtitle of the plot.
        caption : str, optional
            The caption of the plot.
        x : str, optional
            The x-axis label.
        y : str, optional
            The y-axis label.
        **kwargs : str, optional
            Additional labels.
        
        Returns
        -------
        GGPlot
            The plot object with the labels set.
        """
        if title is not None:
            self.labels['title'] = title
        if subtitle is not None:
            self.labels['subtitle'] = subtitle
        if caption is not None:
            self.labels['caption'] = caption
        if x is not None:
            self.labels['x'] = x
        if y is not None:
            self.labels['y'] = y
        
        for key, value in kwargs.items():
            self.labels[key] = value
        
        return self
    
    def _build_plot(self) -> hv.Element:
        """Build the plot from the layers, scales, facets, and theme.
        
        Returns
        -------
        hv.Element
            The constructed Holoviews plot.
        """
        if not self.layers:
            raise ValueError("No layers in plot. Add a layer with a geom_*() function.")
        
        # Build the plot from the layers
        plots = []
        for layer in self.layers:
            plots.append(layer.build(self.data, self.mapping))
        
        # Combine layers as overlays
        plot = plots[0]
        for p in plots[1:]:
            plot = plot * p
        
        # Apply scales
        for scale in self.scales:
            plot = scale.apply(plot)
        
        # Apply faceting
        if self.facets:
            # Provide original DataFrame to Facet object for use in apply
            setattr(self.facets, '_data', self.data)
            plot = self._store_for_faceting(plot)
            plot = self.facets.apply(plot)
        
        # Apply coordinate system
        if self.coords:
            plot = self.coords.apply(plot)
          # Apply theme
        if self._theme:
            plot = self._theme.apply(plot)
        
        # Apply labels
        opts = {}
        if 'title' in self.labels:
            opts['title'] = self.labels['title']
        if 'x' in self.labels:
            opts['xlabel'] = self.labels['x']
        if 'y' in self.labels:
            opts['ylabel'] = self.labels['y']
        
        if opts:
            plot = plot.opts(**opts)
        
        return plot
    
    def build(self) -> hv.Element:
        """Build the plot.
        
        Returns
        -------
        hv.Element
            The constructed Holoviews plot.
        """
        return self._build_plot()
    
    def __repr__(self):
        """Get a string representation of the plot.
        
        Returns
        -------
        str
            A string representation of the plot.
        """
        return f"GGPlot(data={self.data.shape}, layers={len(self.layers)})"
    
    def _repr_html_(self):
        """Display the plot as HTML in Jupyter notebook.
        
        Returns
        -------
        str
            HTML representation of the plot.
        """
        plot = self._build_plot()
        
        # Check if the object has _repr_html_ method
        if hasattr(plot, '_repr_html_'):
            return plot._repr_html_()
        else:
            # For HoloViews objects without _repr_html_, use the renderer
            import holoviews as hv
            renderer = hv.renderer('bokeh')
            return renderer.html(plot)


def ggplot(data: pd.DataFrame, mapping: Optional[Aesthetics] = None) -> GGPlot:
    """Create a new ggplot.
    
    Parameters
    ----------
    data : pandas.DataFrame
        The data to plot.
    mapping : Aesthetics, optional
        Aesthetic mappings from data variables to visual attributes.
    
    Returns
    -------
    GGPlot
        A new ggplot object.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    >>> plot = ggplot(data, aes(x='x', y='y'))
    """
    return GGPlot(data, mapping)
