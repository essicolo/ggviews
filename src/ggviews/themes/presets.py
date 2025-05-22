"""
Theme presets for ggviews.

This module defines preset themes for ggviews.
"""
from .base import Theme


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