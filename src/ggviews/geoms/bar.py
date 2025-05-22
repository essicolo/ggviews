import pandas as pd
from .base import Layer, Aesthetics, is_valid_dimension_name
from typing import Optional
import holoviews as hv


class GeomBar(Layer):
    """A layer with bar geometry.

    Parameters
    ----------
    data : pandas.DataFrame, optional
        Data for this layer. If None, the plot's data is used.
    mapping : Aesthetics, optional
        Aesthetic mappings for this layer. These override the plot's mappings.
    stat : str, default 'count'
        The statistic to use. Either 'count' or 'identity'.
    position : str, default 'stack'
        The position adjustment to use. One of 'stack', 'dodge', or 'identity'.
    **kwargs : Any
        Additional aesthetic mappings or options.

    Examples
    --------
    >>> from ggviews import ggplot, aes
    >>> import pandas as pd
    >>> data = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [1, 4, 9]})
    >>> (ggplot(data, aes(x='category', y='value'))
    ...     .geom_bar(stat='identity', fill='blue')
    ... )
    """

    def __init__(
        self,
        data: Optional[pd.DataFrame] = None,
        mapping: Optional[Aesthetics] = None,
        stat: str = 'count',
        position: str = 'stack',
        **kwargs
    ):
        super().__init__(data, mapping, **kwargs)
        self.stat_type = stat
        self.position_type = position

    def create_element(self, data: pd.DataFrame, mapping: Aesthetics) -> hv.Element:
        """Create a Holoviews Bars element.

        Parameters
        ----------
        data : pandas.DataFrame
            The data for this layer.
        mapping : Aesthetics
            The aesthetic mapping for this layer.

        Returns
        -------
        hv.Element
            A Holoviews Bars element.
        """
        mappings = mapping.get_mappings()

        # For bar plots, we need at least x
        if 'x' not in mappings:
            raise ValueError("x aesthetic must be specified for geom_bar")

        x = mappings['x']
        y = mappings.get('y')

        # If stat is count and y is not specified, we need to count the occurrences
        if self.stat_type == 'count' and y is None:
            counts = data[x].value_counts().reset_index()
            counts.columns = [x, 'count']
            data = counts
            y = 'count'
        elif self.stat_type == 'identity' and y is None:
            raise ValueError("y aesthetic must be specified for geom_bar with stat='identity'")
        # Get additional aesthetics for the bar plot
        kdims = [x]
        vdims = [y]
        opts = {}

        # Add color, fill, etc. to the options but only add column names to vdims
        if 'fill' in mappings:
            fill_val = mappings['fill']
            if is_valid_dimension_name(fill_val, data):
                vdims.append(fill_val)
            opts['fill_color'] = fill_val

        if 'color' in mappings:
            color_val = mappings['color']
            if is_valid_dimension_name(color_val, data):
                vdims.append(color_val)
            opts['line_color'] = color_val

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

        # Create the bar plot with only the necessary columns
        bars_data = data[all_dims].copy()
        bars = hv.Bars(bars_data, kdims=kdims, vdims=vdims)

        # Apply position adjustment
        if self.position_type == 'dodge':
            # Dodging would require grouping and offsetting bars
            pass
        elif self.position_type == 'stack':
            # Stacking is the default
            pass

        # Apply options if any were set
        if opts:
            bars = bars.opts(**opts)

        return bars