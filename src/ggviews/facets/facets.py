"""
Facet implementations for ggviews.

This module implements faceting functionality, similar to ggplot2's facet_* functions.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

import holoviews as hv
import pandas as pd
import numpy as np


class Facet(ABC):
    """Base class for all facets."""
    
    @abstractmethod
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the faceting to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the faceting to.
        
        Returns
        -------
        hv.Element
            The plot element with the faceting applied.
        """
        pass


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


class FacetWrap(Facet):
    """Wrap a 1d sequence of panels into a 2d grid to save space.
    
    Parameters
    ----------
    facets : str or list of str
        Variables to facet by.
    nrow : int, optional
        Number of rows.
    ncol : int, optional
        Number of columns.
    scales : str, default 'fixed'
        Should scales be fixed ('fixed'), or allowed to vary ('free')
    """
    
    def __init__(
        self,
        facets: Union[str, List[str]],
        nrow: Optional[int] = None,
        ncol: Optional[int] = None,
        scales: str = 'fixed'
    ):
        if isinstance(facets, str):
            self.facets = [facets]
        else:
            self.facets = facets
        self.nrow = nrow
        self.ncol = ncol
        self.scales = scales
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the wrap faceting to a plot element.
        
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
        
        # For each facet variable, get unique values
        if len(self.facets) == 1:
            # Simple case with a single facet variable
            facet_var = self.facets[0]
            unique_vals = sorted(data[facet_var].unique())
            
            # Create individual plots for each value
            facet_plots = [
                plot.clone(data[data[facet_var] == val]).relabel(f"{facet_var}={val}")
                for val in unique_vals
            ]
            
        else:
            # Complex case with multiple facet variables
            # Create a new column with combined facet values
            data = data.copy()
            data['__facet__'] = ''
            
            for var in self.facets:
                data['__facet__'] += var + '=' + data[var].astype(str) + ', '
            
            # Remove trailing comma and space
            data['__facet__'] = data['__facet__'].str[:-2]
            
            # Get unique facet combinations
            unique_vals = sorted(data['__facet__'].unique())
            
            # Create individual plots for each facet combination
            facet_plots = [
                plot.clone(data[data['__facet__'] == val]).relabel(val)
                for val in unique_vals
            ]
        
        # Determine grid layout
        n_facets = len(facet_plots)
        
        if self.ncol is None and self.nrow is None:
            # Default to a square-ish grid
            ncols = int(np.ceil(np.sqrt(n_facets)))
        elif self.ncol is None:
            # Set cols based on rows
            ncols = int(np.ceil(n_facets / self.nrow))
        else:
            # Use specified number of columns
            ncols = self.ncol
        
        # Create the facet layout
        facet_layout = hv.Layout(facet_plots).cols(ncols)
        
        # Apply shared scales if requested
        if self.scales == 'fixed':
            # For fixed scales, we need to set the same limits for all plots
            facet_layout = facet_layout.opts(shared_axes=True)
        
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


def facet_wrap(
    facets: Union[str, List[str]],
    nrow: Optional[int] = None,
    ncol: Optional[int] = None,
    scales: str = 'fixed'
) -> FacetWrap:
    """Wrap a 1d sequence of panels into a 2d grid to save space.
    
    Parameters
    ----------
    facets : str or list of str
        Variables to facet by.
    nrow : int, optional
        Number of rows.
    ncol : int, optional
        Number of columns.
    scales : str, default 'fixed'
        Should scales be fixed ('fixed'), or allowed to vary ('free')
    
    Returns
    -------
    FacetWrap
        A facet wrap specification.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, facet_wrap
    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...     'x': [1, 2, 3, 1, 2, 3, 1, 2, 3],
    ...     'y': [1, 4, 9, 2, 5, 10, 3, 6, 11],
    ...     'group': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']
    ... })
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .facet_wrap('group', ncol=2)
    ... )
    """
    return FacetWrap(facets=facets, nrow=nrow, ncol=ncol, scales=scales)