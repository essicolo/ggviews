"""
Wrap faceting for ggviews.

This module implements wrap faceting functionality.
"""
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

import holoviews as hv
import pandas as pd
import numpy as np

from .base import Facet


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