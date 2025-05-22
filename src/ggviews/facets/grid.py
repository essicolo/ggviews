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
        scales: str = 'fixed',
        space: str = 'fixed',
    ):
        """
        Parameters
        ----------
        row : str, optional
            Variable name for row faceting.
        col : str, optional
            Variable name for column faceting.
        scales : str, default 'fixed'
            Should scales be fixed ('fixed'), or allowed to vary between facets ('free'),
            or only free in one dimension ('free_x', 'free_y')
        space : str, default 'fixed'
            Not implemented. In ggplot2, controls whether panel sizes vary with data range.
            Only 'fixed' is supported in ggviews. Any other value will raise NotImplementedError.
        """
        self.row = row
        self.col = col
        self.scales = scales
        self.space = space
        # Validate input
        if row is None and col is None:
            raise ValueError("At least one of 'row' or 'col' must be specified")
        if space != 'fixed':
            raise NotImplementedError(
                "The 'space' argument is not supported in ggviews. All panels have equal size."
            )
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the grid faceting to a plot element using Holoviews groupby/layout."""
        data = getattr(self, '_data', None)
        if data is None:
            data = getattr(plot, '_gv_data', plot.data)

        # Validate facet columns
        facet_vars = [v for v in [self.row, self.col] if v is not None]
        missing = [var for var in facet_vars if var not in data.columns]
        if missing:
            raise KeyError(f"Facet variables not found in data columns: {missing}. Available columns: {list(data.columns)}")


        # Ensure all facet variables are present as columns in the DataFrame used for the Holoviews element
        facet_vars = [v for v in [self.row, self.col] if v is not None]
        def ensure_facet_columns(df, original_data):
            import pandas as pd
            if not isinstance(df, pd.DataFrame):
                try:
                    df = pd.DataFrame(df)
                except Exception:
                    return df
            missing = [v for v in facet_vars if v not in df.columns]
            if missing:
                for v in missing:
                    if v in original_data.columns:
                        df[v] = original_data[v]
                    else:
                        raise KeyError(f"Facet variable '{v}' is not present in the data passed to the plot or in the original DataFrame. Faceting requires all facet variables to be present as columns in the data.")
            return df

        original_data = getattr(self, '_data', data)

        def add_facet_dims(element, data):
            try:
                element_columns = set(data.columns)
            except Exception:
                return element
            kdims = [str(d) for d in getattr(element, 'kdims', [])]
            vdims = [str(d) for d in getattr(element, 'vdims', [])]
            all_dims = set(kdims) | set(vdims)
            addable = [v for v in facet_vars if v in element_columns and v not in all_dims]
            if not addable:
                return element
            import holoviews as hv
            chart_types = (hv.Scatter, hv.Histogram, hv.Curve, hv.Area, hv.Bars)
            if isinstance(element, chart_types):
                if len(kdims) < 1:
                    try:
                        new_kdims = kdims + [addable[0]]
                        return element.clone(kdims=new_kdims, new_type=type(element))
                    except Exception:
                        pass
                return element
            try:
                new_kdims = kdims + addable
                return element.clone(kdims=new_kdims, new_type=type(element))
            except Exception:
                pass
            try:
                new_vdims = vdims + addable
                return element.clone(vdims=new_vdims, new_type=type(element))
            except Exception:
                return element
            return element

        if hasattr(plot, '_gv_layers') and hasattr(plot, '_gv_mapping'):
            layer_plots = []
            for layer in plot._gv_layers:
                layer_data = ensure_facet_columns(layer.data if layer.data is not None else data.copy(), original_data)
                layer_plot = layer.build(layer_data, plot._gv_mapping)
                layer_plot = add_facet_dims(layer_plot, layer_data)
                layer_plots.append(layer_plot)
            base_plot = layer_plots[0]
            for p in layer_plots[1:]:
                base_plot = base_plot * p
        else:
            try:
                data_with_facets = ensure_facet_columns(data.copy(), original_data)
                base_plot = plot.clone(data_with_facets)
                base_plot = add_facet_dims(base_plot, data_with_facets)
            except Exception:
                data_with_facets = ensure_facet_columns(data.copy(), original_data)
                base_plot = hv.Scatter(data_with_facets, vdims=list(getattr(plot, 'vdims', [])) + facet_vars)

        # Use Holoviews groupby/layout for faceting
        if self.row and self.col:
            facet_layout = base_plot.groupby([self.row, self.col]).layout(self.row, self.col)
        elif self.row:
            facet_layout = base_plot.groupby(self.row).layout()
        elif self.col:
            facet_layout = base_plot.groupby(self.col).layout()
        else:
            raise ValueError("At least one of 'row' or 'col' must be specified")

        # Apply shared scales if requested
        if self.scales == 'fixed':
            facet_layout = facet_layout.opts(shared_axes=True)
        elif self.scales == 'free':
            facet_layout = facet_layout.opts(shared_axes=False)
        elif self.scales == 'free_x':
            facet_layout = facet_layout.opts(shared_axes={'y': True, 'x': False})
        elif self.scales == 'free_y':
            facet_layout = facet_layout.opts(shared_axes={'x': True, 'y': False})
        else:
            raise ValueError(f"Unknown scales option: {self.scales}. Use 'fixed', 'free', 'free_x', or 'free_y'.")

        return facet_layout


def facet_grid(
    row: Optional[str] = None,
    col: Optional[str] = None,
    scales: str = 'fixed',
    space: str = 'fixed',
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
    
    Notes
    -----
    The 'space' argument is not implemented in ggviews. All panels have equal size, regardless of scale settings.
    
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
    return FacetGrid(row=row, col=col, scales=scales, space=space)