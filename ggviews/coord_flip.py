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
        super().__init__()
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand

    def _apply(self, plot, ggplot_obj):
        """Apply coordinate flipping to the plot"""
        if plot is None:
            return None

        try:
            flipped_plot = plot.opts(invert_axes=True)

            opts_kwargs = {}
            if self.ylim is not None:
                opts_kwargs['xlim'] = self.ylim
            if self.xlim is not None:
                opts_kwargs['ylim'] = self.xlim

            if opts_kwargs:
                flipped_plot = flipped_plot.opts(**opts_kwargs)

            return flipped_plot
        except Exception:
            return plot


# Export
__all__ = ['coord_flip']
