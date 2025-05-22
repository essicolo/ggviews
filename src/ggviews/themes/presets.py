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
        # Legend
        'show_legend': True,
        'legend_position': 'right',
    }
    
    return Theme("bw", opts)

def ggplot2_color_palette():
    # ggplot2's default discrete color palette (hue)
    return [
        '#F8766D', # red
        '#7CAE00', # green
        '#00BFC4', # cyan
        '#C77CFF', # purple
        '#FF61C3', # pink
        '#00BA38', # dark green
        '#619CFF', # blue
        '#FFB300', # orange
    ]

def ggplot2_fill_palette():
    # Same as color palette for most geoms
    return ggplot2_color_palette()

def theme_ggplot2() -> Theme:
    """A theme inspired by ggplot2's default look in R.
    Includes background, grid, axis, and legend styling, and uses ggplot2's default color palette.
    Note: Color palette is provided for use in geoms/scales, but not all elements may use it automatically.
    Returns
    -------
    Theme
        A ggplot2-like theme.
    """
    opts = {
        # Panel background
        'bgcolor': '#EBEBEB',
        'width': 600,
        'height': 400,
        # Panel border (supported)
        'border_line_color': 'black',
        'border_line_width': 1.0,
        # Major grid lines
        'gridstyle': {
            'grid_line_color': 'white',
            'grid_line_width': 1.1,
            'grid_line_dash': 'solid',
        },
        # Axes
        'show_grid': True,
        # Legend
        'show_legend': True,
        'legend_position': 'right',
        # Note: ggplot2_palette is available as a function for use in geoms/scales, not as a theme option
    }
    return Theme("ggplot2", opts)