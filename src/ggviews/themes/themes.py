"""
Theme implementations for ggviews.

This module implements themes, similar to ggplot2's theme_* functions.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Tuple

import holoviews as hv


class Theme:
    """Base class for all themes.
    
    Parameters
    ----------
    name : str
        Name of the theme.
    opts : dict
        Options to apply for the theme.
    """
    
    def __init__(self, name: str, opts: Dict[str, Any]):
        self.name = name
        self.opts = opts
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the theme to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the theme to.
        
        Returns
        -------
        hv.Element
            The plot element with the theme applied.
        """
        return plot.opts(**self.opts)


def theme_default() -> Theme:
    """Default theme for ggviews.
    
    Returns
    -------
    Theme
        The default theme.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, theme_default
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .theme_default()
    ... )
    """    
    opts = {
        # Basic styling
        'bgcolor': 'white',
        'width': 600,
        'height': 400,
        # Gridlines
        'gridstyle': {'grid_line_dash': [6, 4]},
        # Axes
        'show_grid': True,
        # Legend
        'show_legend': True,
        'legend_position': 'right',
    }
    
    return Theme("default", opts)


def theme_minimal() -> Theme:
    """A minimal theme with light grey lines and axes.
    
    Returns
    -------
    Theme
        A minimal theme.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, theme_minimal
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .theme_minimal()
    ... )
    """    
    opts = {
        # Basic styling
        'bgcolor': 'white',
        'width': 600,
        'height': 400,
        # Gridlines
        'gridstyle': {'grid_line_color': '#EDEDED', 'grid_line_width': 0.5},
        # Axes
        'show_grid': True,
        'xaxis': {'axis_line_width': 0},
        'yaxis': {'axis_line_width': 0},
        # Legend
        'show_legend': True,
        'legend_position': 'right',
    }
    
    return Theme("minimal", opts)


def theme_bw() -> Theme:
    """A black and white theme with a light grey background.
    
    Returns
    -------
    Theme
        A black and white theme.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, theme_bw
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .theme_bw()
    ... )
    """    
    opts = {
        # Basic styling
        'bgcolor': '#F0F0F0',
        'width': 600,
        'height': 400,
        # Gridlines
        'gridstyle': {'grid_line_color': 'white', 'grid_line_width': 1},
        # Axes
        'show_grid': True,
        'xaxis': {'axis_line_color': 'black', 'axis_line_width': 1},
        'yaxis': {'axis_line_color': 'black', 'axis_line_width': 1},
        # Legend
        'show_legend': True,
        'legend_position': 'right',
    }
    
    return Theme("bw", opts)
