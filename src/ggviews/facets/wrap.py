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
        scales: str = 'fixed',
        space: str = 'fixed',
    ):
        """
        Parameters
        ----------
        facets : str or list of str
            Variables to facet by.
        nrow : int, optional
            Number of rows.
        ncol : int, optional
            Number of columns.
        scales : str, default 'fixed'
            Should scales be fixed ('fixed'), or allowed to vary ('free'), or only free in one dimension ('free_x', 'free_y')
        space : str, default 'fixed'
            Not implemented. In ggplot2, controls whether panel sizes vary with data range.
            Only 'fixed' is supported in ggviews. Any other value will raise NotImplementedError.
        """
        if isinstance(facets, str):
            self.facets = [facets]
        else:
            self.facets = facets
        self.nrow = nrow
        self.ncol = ncol
        self.scales = scales
        self.space = space
        if space != 'fixed':
            raise NotImplementedError(
                "The 'space' argument is not supported in ggviews. All panels have equal size."
            )
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the wrap faceting to a plot element using Holoviews groupby/layout."""
        data = getattr(self, '_data', None)
        if data is None:
            data = getattr(plot, '_gv_data', plot.data)

        # Validate facet columns
        missing = [var for var in self.facets if var not in data.columns]
        if missing:            raise KeyError(f"Facet variables not found in data columns: {missing}. Available columns: {list(data.columns)}")

        # Ensure all facet variables are present as columns in the DataFrame used for the Holoviews element
        facet_vars = self.facets
        
        def ensure_facet_columns(df, original_data):
            # Always return a DataFrame with all facet columns present
            import pandas as pd
            # Convert to DataFrame if not already
            if not isinstance(df, pd.DataFrame):
                try:
                    df = pd.DataFrame(df)
                except Exception:
                    return df
            # Add missing facet columns from original_data
            missing = [v for v in facet_vars if v not in df.columns]
            if missing:
                for v in missing:
                    if v in original_data.columns:
                        # Broadcast the column to the correct length if needed
                        if len(original_data[v]) == len(df):
                            df[v] = original_data[v].values
                        else:
                            # Try to align by index if possible
                            try:
                                df[v] = original_data[v].reindex(df.index).values
                            except Exception:
                                # Fallback: fill with NaN
                                import numpy as np
                                df[v] = np.nan                    
                    else:
                        raise KeyError(f"Facet variable '{v}' is not present in the data passed to the plot or in the original DataFrame. Faceting requires all facet variables to be present as columns in the data.")
            return df

        # Use the original data to fill in missing facet columns if needed
        original_data = getattr(self, '_data', data)

        def add_facet_dims(element, data):
            """Add facet dimensions to a HoloViews element.

            This function ensures that all facet variables are added as dimensions
            to the HoloViews element, either as kdims or vdims.
            
            Parameters
            ----------
            element : holoviews.Element
                The HoloViews element to add dimensions to
            data : pandas.DataFrame
                The DataFrame containing the data with facet columns
                
            Returns
            -------
            holoviews.Element
                The element with facet dimensions added
            """
            try:
                element_columns = set(data.columns)
            except Exception:
                return element
                
            kdims = [str(d) for d in getattr(element, 'kdims', [])]
            vdims = [str(d) for d in getattr(element, 'vdims', [])]
            all_dims = set(kdims) | set(vdims)
            
            # Identify facet variables that need to be added to dimensions
            addable = [v for v in facet_vars if v in element_columns and v not in all_dims]
            if not addable:
                return element
                
            # Add facet variables to vdims
            new_vdims = vdims + [v for v in addable if v not in vdims]
            
            try:
                # Try adding as vdims first (most compatible approach)
                return element.clone(vdims=new_vdims, new_type=type(element))
            except Exception:
                # If that fails, try adding first facet var as kdim
                try:
                    new_kdims = kdims + [addable[0]]
                    return element.clone(kdims=new_kdims, vdims=vdims, new_type=type(element))
                except Exception:
                    pass
            
            return element

        if hasattr(plot, '_gv_layers') and hasattr(plot, '_gv_mapping'):
            import holoviews as hv
            layer_plots = []
            # Determine kdims/vdims for each layer based on geom type and mapping
            for layer in plot._gv_layers:
                mapping = plot._gv_mapping.get_mappings() if hasattr(plot._gv_mapping, 'get_mappings') else {}
                x = mapping.get('x')
                y = mapping.get('y')
                # Prepare data
                layer_data = layer.data if layer.data is not None else data.copy()
                # Ensure all facet columns are present after all transformations/stat operations
                # Use the index of layer_data and original_data to align
                import pandas as pd
                if not isinstance(layer_data, pd.DataFrame):
                    try:
                        layer_data = pd.DataFrame(layer_data)
                    except Exception:
                        pass
                if isinstance(layer_data, pd.DataFrame):
                    missing = [v for v in facet_vars if v not in layer_data.columns]
                    if missing:
                        # Try to align by index, fallback to reset index
                        for v in missing:
                            if v in original_data.columns:
                                if len(original_data[v]) == len(layer_data):
                                    layer_data[v] = original_data[v].values
                                else:
                                    try:
                                        # Try to align by index
                                        layer_data[v] = original_data[v].reindex(layer_data.index).values
                                    except Exception:
                                        # Fallback: reset index and align by row order
                                        layer_data = layer_data.reset_index(drop=True)
                                        orig_reset = original_data.reset_index(drop=True)
                                        layer_data[v] = orig_reset[v].values[:len(layer_data)]
                            else:
                                import numpy as np
                                layer_data[v] = np.nan
                # Determine kdims/vdims smartly
                geom_type = type(layer).__name__.lower()
                kdims = []
                vdims = []
                if geom_type in ['geompoint', 'geomline', 'geombar', 'geomboxplot', 'geomviolin', 'geomhistogram', 'geombar', 'geomdensity']:
                    if x: kdims.append(x)
                    if y: vdims.append(y)
                # For future tile/heatmap: if geom_type in ['geomtile', 'geomheatmap']:
                #     if x: kdims.append(x)
                #     if y: vdims.append(y)
                # Add facet vars to vdims if not already in kdims
                for v in facet_vars:
                    if v not in kdims:
                        vdims.append(v)
                # Add any other columns in the data not already in kdims/vdims
                if isinstance(layer_data, pd.DataFrame):
                    for col in layer_data.columns:
                        if col not in kdims and col not in vdims:
                            vdims.append(col)
                # Remove duplicates
                kdims = list(dict.fromkeys(kdims))
                vdims = list(dict.fromkeys(vdims))
                # Build the element with correct dims
                try:
                    layer_plot = layer.build(layer_data, plot._gv_mapping)
                    layer_plot = layer_plot.clone(kdims=kdims, vdims=vdims, new_type=type(layer_plot))
                except Exception:
                    layer_plot = layer.build(layer_data, plot._gv_mapping)
                layer_plots.append(layer_plot)
            # Overlay all layers (all have the same kdims/vdims)
            base_plot = layer_plots[0]
            for p in layer_plots[1:]:
                base_plot = base_plot * p
        else:              
            try:
                # Create a DataFrame that includes all necessary columns for faceting
                import pandas as pd
                
                # Start with the original data and update with transformed data
                # This preserves all columns from original data, including facet columns
                if isinstance(data, pd.DataFrame) and isinstance(original_data, pd.DataFrame):
                    data_copy = original_data.copy()
                    # Update with transformed data for aesthetics
                    common_cols = [col for col in data.columns if col in data_copy.columns]
                    data_copy[common_cols] = data[common_cols]
                    data_with_facets = data_copy
                else:
                    # If not DataFrames, use the ensure_facet_columns helper
                    data_with_facets = ensure_facet_columns(data.copy(), original_data)
                
                # Clone the plot with complete data including facet columns
                base_plot = plot.clone(data_with_facets)
                
                # Ensure facet columns are available as dimensions
                if isinstance(data_with_facets, pd.DataFrame):
                    all_dims = [str(d) for d in base_plot.dimensions()]
                    
                    # Add missing facet columns as dimensions
                    for facet_var in facet_vars:
                        if facet_var in data_with_facets.columns and facet_var not in all_dims:
                            # Use redim.values to add the column as a dimension
                            base_plot = base_plot.redim.values(**{
                                facet_var: data_with_facets[facet_var]
                            })
            except Exception:
                # Fallback: create a new plot with all necessary dimensions
                data_with_facets = ensure_facet_columns(data.copy(), original_data)
                
                # Get x/y from mapping
                x_col = y_col = None
                if hasattr(plot, '_gv_mapping'):
                    mapping = plot._gv_mapping
                    x_col = mapping.x if hasattr(mapping, 'x') else mapping.get('x')
                    y_col = mapping.y if hasattr(mapping, 'y') else mapping.get('y')
                
                # Set up dimensions
                kdims = [x_col] if x_col else []
                vdims = [y_col] if y_col else []
                
                # Add facet variables to dimensions
                for var in facet_vars:
                    if var not in kdims and var not in vdims:
                        vdims.append(var)
                
                # Add other columns
                if isinstance(data_with_facets, pd.DataFrame):
                    for col in data_with_facets.columns:
                        if col not in kdims and col not in vdims:
                            vdims.append(col)
                
                # Create a plot with all needed dimensions
                import holoviews as hv
                base_plot = hv.Scatter(data_with_facets, kdims=kdims, vdims=vdims)        # Use Holoviews groupby/layout for faceting
        import holoviews as hv
        import numpy as np
        import pandas as pd
        
        # Final check before groupby operation
        if len(self.facets) == 1:
            facet_col = self.facets[0]
            
            # Ensure the facet column is in the data before groupby
            if hasattr(base_plot, 'data') and isinstance(base_plot.data, pd.DataFrame):
                if facet_col not in base_plot.data.columns:
                    # Add missing facet column from original data
                    if isinstance(original_data, pd.DataFrame) and facet_col in original_data.columns:
                        # Create a new DataFrame with facet column
                        df = base_plot.data.copy()
                        df[facet_col] = original_data[facet_col].iloc[:len(df)]
                        
                        # Get axis columns from mapping
                        x_col = y_col = None
                        if hasattr(plot, '_gv_mapping'):
                            mapping = plot._gv_mapping
                            x_col = mapping.x if hasattr(mapping, 'x') else mapping.get('x')
                            y_col = mapping.y if hasattr(mapping, 'y') else mapping.get('y')
                        
                        # Set up proper dimensions for the new plot
                        kdims = [x_col] if x_col else []
                        vdims = [y_col] if y_col else []
                        if facet_col not in kdims and facet_col not in vdims:
                            vdims.append(facet_col)
                        
                        # Add other columns as dimensions
                        for col in df.columns:
                            if col not in kdims and col not in vdims:
                                vdims.append(col)
                        
                        # Create a new plot with all columns
                        base_plot = hv.Scatter(df, kdims=kdims, vdims=vdims)
            
            # Create facet layout
            facet_layout = base_plot.groupby(facet_col).layout()
        else:        # Handle multiple facet variables - ensure all facet columns exist
            # Check all facet columns exist
            if hasattr(base_plot, 'data') and isinstance(base_plot.data, pd.DataFrame):
                missing_cols = [col for col in self.facets if col not in base_plot.data.columns]
                if missing_cols:
                    # Add missing columns from original data
                    if isinstance(original_data, pd.DataFrame):
                        df = base_plot.data.copy()
                        for col in missing_cols:
                            if col in original_data.columns:
                                df[col] = original_data[col].iloc[:len(df)]
                        
                        # Create a new plot with all required dimensions
                        x_col = y_col = None
                        if hasattr(plot, '_gv_mapping'):
                            mapping = plot._gv_mapping
                            x_col = mapping.x if hasattr(mapping, 'x') else mapping.get('x')
                            y_col = mapping.y if hasattr(mapping, 'y') else mapping.get('y')
                        
                        # Set up dimensions
                        kdims = [x_col] if x_col else []
                        vdims = [y_col] if y_col else []
                        
                        # Add facet columns to vdims
                        for col in self.facets:
                            if col not in kdims and col not in vdims:
                                vdims.append(col)
                        
                        # Add remaining columns
                        for col in df.columns:
                            if col not in kdims and col not in vdims:
                                vdims.append(col)
                        
                        # Create a new plot
                        base_plot = hv.Scatter(df, kdims=kdims, vdims=vdims)
            
            # Now try groupby with the list of facet columns
            facet_layout = base_plot.groupby(self.facets).layout()

        # Determine number of columns
        n_facets = len(data.groupby(self.facets))
        if self.ncol is None and self.nrow is None:
            ncols = int(np.ceil(np.sqrt(n_facets)))
        elif self.ncol is None:
            ncols = int(np.ceil(n_facets / self.nrow))
        else:
            ncols = self.ncol
        facet_layout = facet_layout.cols(ncols)

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


def facet_wrap(
    facets: Union[str, List[str]],
    nrow: Optional[int] = None,
    ncol: Optional[int] = None,
    scales: str = 'fixed',
    space: str = 'fixed',
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
    
    Notes
    -----
    The 'space' argument is not implemented in ggviews. All panels have equal size, regardless of scale settings.
    
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
    return FacetWrap(facets=facets, nrow=nrow, ncol=ncol, scales=scales, space=space)