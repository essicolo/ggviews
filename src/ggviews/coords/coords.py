"""
Coordinate systems for ggviews.

This module provides coordinate systems functionality, similar to ggplot2's coord_* functions.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, Union

import holoviews as hv


class CoordinateSystem(ABC):
    """Base class for all coordinate systems."""
    
    @abstractmethod
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the coordinate system to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the coordinate system to.
        
        Returns
        -------
        hv.Element
            The plot element with the coordinate system applied.
        """
        pass


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


class PolarCoord(CoordinateSystem):
    """Polar coordinate system.
    
    Parameters
    ----------
    theta : str, optional
        The name of the column to map to the angle (theta).
    r : str, optional
        The name of the column to map to the radius (r).
    start_theta : float, default 0
        The starting angle (in radians) for the polar coordinates.
    direction : str, default 'counterclockwise'
        The direction of rotation, either 'counterclockwise' or 'clockwise'.
    """
    
    def __init__(
        self,
        theta: Optional[str] = None,
        r: Optional[str] = None,
        start_theta: float = 0,
        direction: str = 'counterclockwise',
    ):
        self.theta = theta
        self.r = r
        self.start_theta = start_theta
        self.direction = direction
        
        if direction not in ['counterclockwise', 'clockwise']:
            raise ValueError("direction must be 'counterclockwise' or 'clockwise'")
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply polar coordinates to the plot.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the coordinate system to.
        
        Returns
        -------
        hv.Element
            The plot element with polar coordinates applied.
        """
        # Implementing polar coordinates in Holoviews requires more transformation
        # than just applying opts; we would need to transform the data
        # This is a placeholder that would need further implementation
        opts = {'projection': 'polar'}
        
        if self.start_theta != 0 or self.direction == 'clockwise':
            # Custom handling would be needed here
            pass
        
        return plot.opts(**opts)
