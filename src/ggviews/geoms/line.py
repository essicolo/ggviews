import pandas as pd
from .base import Layer, Aesthetics, is_valid_dimension_name
from typing import Optional
import holoviews as hv

class GeomLine(Layer):
    """A layer with line geometry.

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
    ...     .geom_line(color='blue', linewidth=2)
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
        """Create a Holoviews Curve element.

        Parameters
        ----------
        data : pandas.DataFrame
            The data for this layer.
        mapping : Aesthetics
            The aesthetic mapping for this layer.

        Returns
        -------
        hv.Element
            A Holoviews Curve element.
        """
        mappings = mapping.get_mappings()

        # We need at least x and y for a line plot
        if 'x' not in mappings or 'y' not in mappings:
            raise ValueError("Both x and y aesthetics must be specified for geom_line")

        x = mappings['x']
        y = mappings['y']
        # Get additional aesthetics for the line plot
        kdims = [x]
        vdims = [y]
        opts = {}

        # Add color, linetype, etc. to the options but only add column names to vdims
        if 'color' in mappings:
            color_val = mappings['color']
            if is_valid_dimension_name(color_val, data):
                vdims.append(color_val)
            opts['color'] = color_val

        if 'linewidth' in mappings:
            linewidth_val = mappings['linewidth']
            if is_valid_dimension_name(linewidth_val, data):
                vdims.append(linewidth_val)
            opts['linewidth'] = linewidth_val

        if 'linetype' in mappings:
            linetype_val = mappings['linetype']
            if is_valid_dimension_name(linetype_val, data):
                vdims.append(linetype_val)
            opts['dash'] = linetype_val

        if 'alpha' in mappings:
            alpha_val = mappings['alpha']
            if is_valid_dimension_name(alpha_val, data):
                vdims.append(alpha_val)
            opts['alpha'] = alpha_val

        # Check that all dimensions are valid column names
        all_dims = kdims + vdims
        for dim in all_dims:
            if dim not in data.columns:
                raise ValueError(f"Column '{dim}' not found in data. Available columns: {list(data.columns)}")

        # Create the line plot with only the necessary columns
        curve_data = data[all_dims].copy()
        curve = hv.Curve(curve_data, kdims=kdims, vdims=vdims)

        # Apply options if any were set
        if opts:
            curve = curve.opts(**opts)

        return curve