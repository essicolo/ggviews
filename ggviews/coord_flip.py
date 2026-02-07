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

            # Swap axis labels so they stay with the correct data dimension
            if ggplot_obj and ggplot_obj.mapping:
                x_col = ggplot_obj.mapping.mappings.get('x')
                y_col = ggplot_obj.mapping.mappings.get('y')
                x_label = ggplot_obj.labels.get('x', str(x_col) if x_col else None)
                y_label = ggplot_obj.labels.get('y', str(y_col) if y_col else None)
                # After invert_axes, the rendered x-axis shows y data and vice versa
                if y_label:
                    opts_kwargs['xlabel'] = y_label
                if x_label:
                    opts_kwargs['ylabel'] = x_label

            if opts_kwargs:
                flipped_plot = flipped_plot.opts(**opts_kwargs)

            return flipped_plot
        except Exception:
            return plot


# Export
__all__ = ['coord_flip']
