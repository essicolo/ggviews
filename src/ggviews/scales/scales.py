"""
Scale transformations for ggviews.

This module implements scale transformations, similar to ggplot2's scale_* functions.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

import holoviews as hv
import pandas as pd
import numpy as np


class Scale(ABC):
    """Base class for all scales."""
    
    @abstractmethod
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the scale to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the scale to.
        
        Returns
        -------
        hv.Element
            The plot element with the scale applied.
        """
        pass


class ScaleContinuous(Scale):
    """Base class for continuous scales.
    
    Parameters
    ----------
    name : str
        Name of the scale.
    breaks : list, optional
        Breaks (tick positions) to use.
    labels : list, optional
        Labels for the breaks.
    limits : tuple, optional
        Limits for the scale as (min, max).
    trans : callable, optional
        Transformation function to apply to the data.
    """
    
    def __init__(
        self,
        name: str,
        breaks: Optional[List[Union[int, float]]] = None,
        labels: Optional[List[str]] = None,
        limits: Optional[Tuple[float, float]] = None,
        trans: Optional[Callable] = None,
        log: bool = False,
        axis: str = 'x',
    ):
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.limits = limits
        self.trans = trans
        self.log = log
        self.axis = axis
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the continuous scale to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the scale to.
        
        Returns
        -------
        hv.Element
            The plot element with the scale applied.
        """
        opts = {}
        
        # Set the scale to log if requested
        if self.log:
            if self.axis == 'x':
                opts['logx'] = True
            elif self.axis == 'y':
                opts['logy'] = True
            else:
                raise ValueError(f"Invalid axis: {self.axis}")
        
        # Set the limits if specified
        if self.limits is not None:
            if self.axis == 'x':
                opts['xlim'] = self.limits
            elif self.axis == 'y':
                opts['ylim'] = self.limits
        
        # Set the breaks if specified
        if self.breaks is not None:
            if self.axis == 'x':
                opts['xticks'] = self.breaks
            elif self.axis == 'y':
                opts['yticks'] = self.breaks
        
        # TODO: Handle labels for breaks
        
        # Apply the options
        if opts:
            return plot.opts(**opts)
        
        return plot


class ScaleDiscreet(Scale):
    """Base class for discrete scales.
    
    Parameters
    ----------
    name : str
        Name of the scale.
    breaks : list, optional
        Breaks (tick positions) to use.
    labels : list, optional
        Labels for the breaks.
    limits : list, optional
        Limits for the scale (subset of values to display).
    """
    
    def __init__(
        self,
        name: str,
        breaks: Optional[List[Any]] = None,
        labels: Optional[List[str]] = None,
        limits: Optional[List[Any]] = None,
        axis: str = 'x',
    ):
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.limits = limits
        self.axis = axis
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the discrete scale to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the scale to.
        
        Returns
        -------
        hv.Element
            The plot element with the scale applied.
        """
        opts = {}
        
        # Set the breaks if specified
        if self.breaks is not None:
            if self.axis == 'x':
                opts['xticks'] = self.breaks
            elif self.axis == 'y':
                opts['yticks'] = self.breaks
        
        # TODO: Handle limits by filtering data
        
        # TODO: Handle labels for breaks
        
        # Apply the options
        if opts:
            return plot.opts(**opts)
        
        return plot


def scale_x_log10(
    breaks: Optional[List[Union[int, float]]] = None,
    labels: Optional[List[str]] = None,
    limits: Optional[Tuple[float, float]] = None,
) -> ScaleContinuous:
    """Create a log10 scale for the x-axis.
    
    Parameters
    ----------
    breaks : list, optional
        Breaks (tick positions) to use.
    labels : list, optional
        Labels for the breaks.
    limits : tuple, optional
        Limits for the scale as (min, max).
    
    Returns
    -------
    ScaleContinuous
        A log10 scale for the x-axis.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, scale_x_log10
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 10, 100], 'y': [1, 2, 3]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .scale_x_log10()
    ... )
    """
    return ScaleContinuous("log10", breaks=breaks, labels=labels, limits=limits, log=True, axis='x')


def scale_y_log10(
    breaks: Optional[List[Union[int, float]]] = None,
    labels: Optional[List[str]] = None,
    limits: Optional[Tuple[float, float]] = None,
) -> ScaleContinuous:
    """Create a log10 scale for the y-axis.
    
    Parameters
    ----------
    breaks : list, optional
        Breaks (tick positions) to use.
    labels : list, optional
        Labels for the breaks.
    limits : tuple, optional
        Limits for the scale as (min, max).
    
    Returns
    -------
    ScaleContinuous
        A log10 scale for the y-axis.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, scale_y_log10
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 10, 100]})
    >>> (ggplot(data, aes(x='x', y='y'))
    ...     .geom_point()
    ...     .scale_y_log10()
    ... )
    """
    return ScaleContinuous("log10", breaks=breaks, labels=labels, limits=limits, log=True, axis='y')
