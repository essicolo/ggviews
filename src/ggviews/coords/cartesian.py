"""
Cartesian coordinate system for ggviews.

This module implements the Cartesian coordinate system.
"""
from typing import Dict, Any, Optional, Tuple, Union

import holoviews as hv

from .base import CoordinateSystem


class CartesianCoord(CoordinateSystem):
    """Cartesian coordinate system.
    
    Parameters
    ----------
    xlim : tuple, optional
        The x-axis limits as (min, max).
    ylim : tuple, optional
        The y-axis limits as (min, max).
    expand : bool, default True
        If True, expand the limits by a small amount to ensure all data is visible.
    """
    
    def __init__(
        self,
        xlim: Optional[Tuple[float, float]] = None,
        ylim: Optional[Tuple[float, float]] = None,
        expand: bool = True,
    ):
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply cartesian coordinates to the plot.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the coordinate system to.
        
        Returns
        -------
        hv.Element
            The plot element with cartesian coordinates applied.
        """
        opts = {}
        
        if self.xlim is not None:
            opts['xlim'] = self.xlim
        if self.ylim is not None:
            opts['ylim'] = self.ylim
        
        if opts:
            return plot.opts(**opts)
        return plot