import pandas as pd
from .base import Layer, Aesthetics, is_valid_dimension_name
from typing import Optional
import holoviews as hv


class GeomPoint(Layer):
    """A layer with point geometry.

    Parameters
    ----------
    data : pandas.DataFrame, optional
        Data for this layer. If None, the plot's data is used.
    mapping : Aesthetics, optional
        Aesthetic mappings for this layer. These override the plot's mappings.
    **kwargs : Any
        Additional aesthetic mappings or options.

    Examples
    --------
    >>> from ggviews import ggplot, aes
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point(color='blue', size=10)
    ... )
    """

    def __init__(
        self,
        data: Optional[pd.DataFrame] = None,
        mapping: Optional[Aesthetics] = None,
        **kwargs
    ):
        super().__init__(data, mapping, **kwargs)

    def create_element(self, data: pd.DataFrame, mapping: Aesthetics) -> hv.Element:
        """Create a Holoviews Scatter or Points element.

        Parameters
        ----------
        data : pandas.DataFrame
            The data for this layer.
        mapping : Aesthetics
            The aesthetic mapping for this layer.

        Returns
        -------
        hv.Element
            A Holoviews Scatter or Points element.
        """
        # Make sure data is actually a DataFrame
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"Expected a pandas DataFrame, got {type(data).__name__} instead.")

        mappings = mapping.get_mappings()

        # We need at least x and y for a scatter plot
        if 'x' not in mappings or 'y' not in mappings:
            raise ValueError("Both x and y aesthetics must be specified for geom_point")

        x = mappings['x']
        y = mappings['y']

        # Get additional aesthetics for the scatter plot
        kdims = [x]
        vdims = [y]
        opts = {}

        # Prepare data for HoloViews
        # Make a copy to avoid modifying the original
        plot_data = data.copy()

        # Add color, size, etc. to the options but only add column names to vdims
        if 'color' in mappings:
            color_val = mappings['color']
            if is_valid_dimension_name(color_val, data):
                vdims.append(color_val)
            opts['color'] = color_val

        if 'size' in mappings:
            size_val = mappings['size']
            if is_valid_dimension_name(size_val, data):
                vdims.append(size_val)
            opts['size'] = size_val

        if 'alpha' in mappings:
            alpha_val = mappings['alpha']
            if is_valid_dimension_name(alpha_val, data):
                vdims.append(alpha_val)
            opts['alpha'] = alpha_val

        # Check that all dimensions are valid column names
        all_dims = kdims + vdims
        for dim in all_dims:
            if dim not in plot_data.columns:
                raise ValueError(f"Column '{dim}' not found in data. Available columns: {list(plot_data.columns)}")

        # Create the scatter plot with only the necessary columns
        scatter_data = plot_data[all_dims].copy()
        scatter = hv.Scatter(scatter_data, kdims=kdims, vdims=vdims)

        # Apply options if any were set
        if opts:
            scatter = scatter.opts(**opts)

        return scatter