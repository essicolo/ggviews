"""
Flipped coordinate system for ggviews.

This module implements the flipped coordinate system.
"""
from typing import Dict, Any, Optional, Tuple, Union

import holoviews as hv

from .base import CoordinateSystem


class FlippedCoord(CoordinateSystem):
    """Flipped coordinate system.
    
    This coordinate system flips the x and y axes.
    """
    
    def __init__(self):
        pass
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply flipped coordinates to the plot.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the coordinate system to.
        
        Returns
        -------
        hv.Element
            The plot element with flipped coordinates.
        """
        # In Holoviews, we can use the opts method to flip the axes
        return plot.opts(invert_axes=True)


def coord_flip() -> FlippedCoord:
    """Create a flipped coordinate system.
    
    Returns
    -------
    FlippedCoord
        A flipped coordinate system.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, coord_flip
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .coord_flip()
    ... )
    """
    return FlippedCoord()