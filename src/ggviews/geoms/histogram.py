import pandas as pd
import numpy as np
from .base import Layer, Aesthetics, is_valid_dimension_name
from typing import Optional
import holoviews as hv


class GeomHistogram(Layer):
    """A layer with histogram geometry.

    Parameters
    ----------
    data : pandas.DataFrame, optional
        Data for this layer. If None, the plot's data is used.
    mapping : Aesthetics, optional
        Aesthetic mappings for this layer. These override the plot's mappings.
    bins : int, default 30
        Number of bins.
    **kwargs : Any
        Additional aesthetic mappings or options.

    Examples
    --------
    >>> from ggviews import ggplot, aes
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame({'x': np.random.normal(size=100)})
    >>> (ggplot(data, aes(x='x'))
    ...     .geom_histogram(bins=20, fill='blue', color='black')
    ... )
    """

    def __init__(
        self,
        data: Optional[pd.DataFrame] = None,
        mapping: Optional[Aesthetics] = None,
        bins: int = 30,
        **kwargs
    ):
        super().__init__(data, mapping, **kwargs)
        self.bins = bins

    def create_element(self, data: pd.DataFrame, mapping: Aesthetics) -> hv.Element:
        """Create a Holoviews Histogram element.

        Parameters
        ----------
        data : pandas.DataFrame
            The data for this layer.
        mapping : Aesthetics
            The aesthetic mapping for this layer.

        Returns
        -------
        hv.Element
            A Holoviews Histogram element.
        """
        mappings = mapping.get_mappings()

        # For histograms, we need at least x
        if 'x' not in mappings:
            raise ValueError("x aesthetic must be specified for geom_histogram")

        x = mappings['x']

        # Validate that the x column exists in the data
        if x not in data.columns:
            raise ValueError(f"Column '{x}' not found in data. Available columns: {list(data.columns)}")

        # Prepare options for styling the histogram
        opts = {}

        # Add color, fill, etc.
        if 'fill' in mappings:
            fill_val = mappings['fill']
            if is_valid_dimension_name(fill_val, data):
                # For histograms, we can't use column mappings for fill color
                # We'll warn about this and use a fixed color
                import warnings
                warnings.warn(f"Column-based fill mapping '{fill_val}' not supported for histograms. Using a fixed color.")
            opts['fill_color'] = fill_val

        if 'color' in mappings:
            color_val = mappings['color']
            if is_valid_dimension_name(color_val, data):
                # Similar warning for color mapping
                import warnings
                warnings.warn(f"Column-based color mapping '{color_val}' not supported for histograms. Using a fixed color.")
            opts['line_color'] = color_val

        if 'alpha' in mappings:
            alpha_val = mappings['alpha']
            if is_valid_dimension_name(alpha_val, data):
                # Similar warning for alpha mapping
                import warnings
                warnings.warn(f"Column-based alpha mapping '{alpha_val}' not supported for histograms. Using a fixed alpha.")
            opts['alpha'] = alpha_val

        # Create the histogram by computing bin counts
        hist_data = data[x].dropna().values
        counts, edges = np.histogram(hist_data, bins=self.bins)
        # edges has length bins+1; HoloViews expects (edges, counts)
        hist = hv.Histogram((edges, counts))

        # Apply options if any were set
        if opts:
            hist = hist.opts(**opts)

        return hist