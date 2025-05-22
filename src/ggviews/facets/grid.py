"""
Grid faceting for ggviews.

This module implements grid faceting functionality.
"""
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

import holoviews as hv
import pandas as pd
import numpy as np

from .base import Facet


class FacetGrid(Facet):
    """Create a grid of panels, defined by row and column faceting variables.
    
    Parameters
    ----------
    row : str, optional
        Variable name for row faceting.
    col : str, optional
        Variable name for column faceting.
    scales : str, default 'fixed'
        Should scales be fixed ('fixed'), or allowed to vary between facets ('free'),
        or only free in one dimension ('free_x', 'free_y')
    """
    
    def __init__(
        self,
        row: Optional[str] = None,
        col: Optional[str] = None,
        scales: str = 'fixed'
    ):
        self.row = row
        self.col = col
        self.scales = scales
        
        # Validate input
        if row is None and col is None:
            raise ValueError("At least one of 'row' or 'col' must be specified")
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the grid faceting to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the faceting to.
        
        Returns
        -------
        hv.Element
            The plot element with the faceting applied.
        """
        # Get the data from the plot
        data = plot.data
        
        facet_layout = None
        
        # Facet by row variable only
        if self.row and not self.col:
            # Create a grid of plots by row variable
            facet_layout = hv.Layout([
                plot.clone(data[data[self.row] == val]).relabel(f"{self.row}={val}")
                for val in sorted(data[self.row].unique())
            ]).cols(1)
        
        # Facet by column variable only
        elif self.col and not self.row:
            # Create a grid of plots by column variable
            facet_layout = hv.Layout([
                plot.clone(data[data[self.col] == val]).relabel(f"{self.col}={val}")
                for val in sorted(data[self.col].unique())
            ]).cols(len(data[self.col].unique()))
        
        # Facet by both row and column
        elif self.row and self.col:
            # Create a grid of plots by row and column variables
            row_vals = sorted(data[self.row].unique())
            col_vals = sorted(data[self.col].unique())
            
            # Create a nested layout
            facet_layout = hv.Layout([
                hv.Layout([
                    plot.clone(
                        data[(data[self.row] == r_val) & (data[self.col] == c_val)]
                    ).relabel(f"{self.row}={r_val}, {self.col}={c_val}")
                    for c_val in col_vals
                ])
                for r_val in row_vals
            ])
        
        # Apply shared scales if requested
        if self.scales == 'fixed':
            # For fixed scales, we need to set the same limits for all plots
            facet_layout = facet_layout.opts(shared_axes=True)
        elif self.scales == 'free_x':
            # For free x scales, set shared y axes only
            facet_layout = facet_layout.opts(shared_axes='y')
        elif self.scales == 'free_y':
            # For free y scales, set shared x axes only
            facet_layout = facet_layout.opts(shared_axes='x')
        
        return facet_layout


def facet_grid(
    row: Optional[str] = None,
    col: Optional[str] = None,
    scales: str = 'fixed'
) -> FacetGrid:
    """Create a grid of panels, defined by row and column faceting variables.
    
    Parameters
    ----------
    row : str, optional
        Variable name for row faceting.
    col : str, optional
        Variable name for column faceting.
    scales : str, default 'fixed'
        Should scales be fixed ('fixed'), or allowed to vary between facets ('free'),
        or only free in one dimension ('free_x', 'free_y')
    
    Returns
    -------
    FacetGrid
        A facet grid specification.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, facet_grid
    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...     'x': [1, 2, 3, 1, 2, 3],
    ...     'y': [1, 4, 9, 2, 5, 10],
    ...     'group': ['A', 'A', 'A', 'B', 'B', 'B']
    ... })
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .facet_grid(row='group')
    ... )
    """
    return FacetGrid(row=row, col=col, scales=scales)