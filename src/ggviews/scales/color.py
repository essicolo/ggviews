"""
Color scales for ggviews.

This module implements color scales for ggviews.
"""
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

import holoviews as hv
import pandas as pd
import numpy as np
import colorcet as cc
import param

from .base import Scale
from .continuous import ScaleContinuous
from .discrete import ScaleDiscreet


class ScaleColorContinuous(ScaleContinuous):
    """Continuous color scale.
    
    Parameters
    ----------
    aesthetic : str
        The aesthetic to scale.
    name : str, optional
        Name of the scale.
    breaks : list, optional
        Breaks for the scale.
    labels : list, optional
        Labels for the breaks.
    limits : tuple, optional
        Limits for the scale as (min, max).
    trans : callable, optional
        Transformation function for the scale.
    palette : str or list, default 'viridis'
        Color palette to use. Can be a named palette or a list of colors.
    na_value : Any, default None
        Value to use for missing values.
    guide : str, default 'colorbar'
        Type of guide to use for the scale.
    """
    
    def __init__(
        self,
        aesthetic: str,
        name: Optional[str] = None,
        breaks: Optional[List[Any]] = None,
        labels: Optional[List[str]] = None,
        limits: Optional[Tuple[float, float]] = None,
        trans: Optional[Callable] = None,
        palette: Union[str, List[str]] = 'viridis',
        na_value: Any = None,
        guide: str = 'colorbar',
    ):
        super().__init__(
            aesthetic=aesthetic,
            name=name,
            breaks=breaks,
            labels=labels,
            limits=limits,
            trans=trans,
            na_value=na_value,
            guide=guide,
        )
        self.palette = palette
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the color scale to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the scale to.
        
        Returns
        -------
        hv.Element
            The plot element with the scale applied.
        """
        # Get the aesthetic name
        aes_name = self.aesthetic
        
        # Create options dictionary
        opts = {}
        
        # Apply color map based on the aesthetic
        if aes_name == 'color':
            opts['color'] = self.palette
        elif aes_name == 'fill':
            opts['fill_color'] = self.palette
        
        # Apply limits if provided
        if self.limits is not None:
            if aes_name == 'color':
                opts['color_levels'] = self.limits
            elif aes_name == 'fill':
                opts['fill_color_levels'] = self.limits
        
        # Apply the options to the plot
        return plot.opts(**opts)


class ScaleColorDiscreet(ScaleDiscreet):
    """Discrete color scale.
    
    Parameters
    ----------
    aesthetic : str
        The aesthetic to scale.
    name : str, optional
        Name of the scale.
    breaks : list, optional
        Breaks for the scale.
    labels : list, optional
        Labels for the breaks.
    limits : list, optional
        Limits for the scale as a list of values.
    palette : str or list, default 'Category10'
        Color palette to use. Can be a named palette or a list of colors.
    na_value : Any, default None
        Value to use for missing values.
    guide : str, default 'legend'
        Type of guide to use for the scale.
    """
    
    def __init__(
        self,
        aesthetic: str,
        name: Optional[str] = None,
        breaks: Optional[List[Any]] = None,
        labels: Optional[List[str]] = None,
        limits: Optional[List[Any]] = None,
        palette: Union[str, List[str]] = 'Category10',
        na_value: Any = None,
        guide: str = 'legend',
    ):
        super().__init__(
            aesthetic=aesthetic,
            name=name,
            breaks=breaks,
            labels=labels,
            limits=limits,
            na_value=na_value,
            guide=guide,
        )
        self.palette = palette
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the color scale to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the scale to.
        
        Returns
        -------
        hv.Element
            The plot element with the scale applied.
        """
        # Get the aesthetic name
        aes_name = self.aesthetic
        
        # Create options dictionary
        opts = {}
        
        # Apply color map based on the aesthetic
        if aes_name == 'color':
            opts['color'] = self.palette
        elif aes_name == 'fill':
            opts['fill_color'] = self.palette
        
        # Apply the options to the plot
        return plot.opts(**opts)


def scale_color_continuous(
    name: Optional[str] = None,
    breaks: Optional[List[Any]] = None,
    labels: Optional[List[str]] = None,
    limits: Optional[Tuple[float, float]] = None,
    trans: Optional[Callable] = None,
    palette: Union[str, List[str]] = 'viridis',
    na_value: Any = None,
    guide: str = 'colorbar',
) -> ScaleColorContinuous:
    """Create a continuous color scale.
    
    Parameters
    ----------
    name : str, optional
        Name of the scale.
    breaks : list, optional
        Breaks for the scale.
    labels : list, optional
        Labels for the breaks.
    limits : tuple, optional
        Limits for the scale as (min, max).
    trans : callable, optional
        Transformation function for the scale.
    palette : str or list, default 'viridis'
        Color palette to use. Can be a named palette or a list of colors.
    na_value : Any, default None
        Value to use for missing values.
    guide : str, default 'colorbar'
        Type of guide to use for the scale.
    
    Returns
    -------
    ScaleColorContinuous
        A continuous color scale.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, scale_color_continuous
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9], 'z': [10, 20, 30]})
    >>> (ggplot(data, aes(x='x', y='y', color='z'))
    ...     .geom_point()
    ...     .scale_color_continuous(palette='viridis')
    ... )
    """
    return ScaleColorContinuous(
        aesthetic='color',
        name=name,
        breaks=breaks,
        labels=labels,
        limits=limits,
        trans=trans,
        palette=palette,
        na_value=na_value,
        guide=guide,
    )


def scale_fill_continuous(
    name: Optional[str] = None,
    breaks: Optional[List[Any]] = None,
    labels: Optional[List[str]] = None,
    limits: Optional[Tuple[float, float]] = None,
    trans: Optional[Callable] = None,
    palette: Union[str, List[str]] = 'viridis',
    na_value: Any = None,
    guide: str = 'colorbar',
) -> ScaleColorContinuous:
    """Create a continuous fill scale.
    
    Parameters
    ----------
    name : str, optional
        Name of the scale.
    breaks : list, optional
        Breaks for the scale.
    labels : list, optional
        Labels for the breaks.
    limits : tuple, optional
        Limits for the scale as (min, max).
    trans : callable, optional
        Transformation function for the scale.
    palette : str or list, default 'viridis'
        Color palette to use. Can be a named palette or a list of colors.
    na_value : Any, default None
        Value to use for missing values.
    guide : str, default 'colorbar'
        Type of guide to use for the scale.
    
    Returns
    -------
    ScaleColorContinuous
        A continuous fill scale.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, scale_fill_continuous
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9], 'z': [10, 20, 30]})
    >>> (ggplot(data, aes(x='x', y='y', fill='z'))
    ...     .geom_point()
    ...     .scale_fill_continuous(palette='viridis')
    ... )
    """
    return ScaleColorContinuous(
        aesthetic='fill',
        name=name,
        breaks=breaks,
        labels=labels,
        limits=limits,
        trans=trans,
        palette=palette,
        na_value=na_value,
        guide=guide,
    )


def scale_color_discrete(
    name: Optional[str] = None,
    breaks: Optional[List[Any]] = None,
    labels: Optional[List[str]] = None,
    limits: Optional[List[Any]] = None,
    palette: Union[str, List[str]] = 'Category10',
    na_value: Any = None,
    guide: str = 'legend',
) -> ScaleColorDiscreet:
    """Create a discrete color scale.
    
    Parameters
    ----------
    name : str, optional
        Name of the scale.
    breaks : list, optional
        Breaks for the scale.
    labels : list, optional
        Labels for the breaks.
    limits : list, optional
        Limits for the scale as a list of values.
    palette : str or list, default 'Category10'
        Color palette to use. Can be a named palette or a list of colors.
    na_value : Any, default None
        Value to use for missing values.
    guide : str, default 'legend'
        Type of guide to use for the scale.
    
    Returns
    -------
    ScaleColorDiscreet
        A discrete color scale.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, scale_color_discrete
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9], 'group': ['A', 'B', 'C']})
    >>> (ggplot(data, aes(x='x', y='y', color='group'))
    ...     .geom_point()
    ...     .scale_color_discrete(palette='Category20')
    ... )
    """
    return ScaleColorDiscreet(
        aesthetic='color',
        name=name,
        breaks=breaks,
        labels=labels,
        limits=limits,
        palette=palette,
        na_value=na_value,
        guide=guide,
    )


def scale_fill_discrete(
    name: Optional[str] = None,
    breaks: Optional[List[Any]] = None,
    labels: Optional[List[str]] = None,
    limits: Optional[List[Any]] = None,
    palette: Union[str, List[str]] = 'Category10',
    na_value: Any = None,
    guide: str = 'legend',
) -> ScaleColorDiscreet:
    """Create a discrete fill scale.
    
    Parameters
    ----------
    name : str, optional
        Name of the scale.
    breaks : list, optional
        Breaks for the scale.
    labels : list, optional
        Labels for the breaks.
    limits : list, optional
        Limits for the scale as a list of values.
    palette : str or list, default 'Category10'
        Color palette to use. Can be a named palette or a list of colors.
    na_value : Any, default None
        Value to use for missing values.
    guide : str, default 'legend'
        Type of guide to use for the scale.
    
    Returns
    -------
    ScaleColorDiscreet
        A discrete fill scale.
    
    Examples
    --------
    >>> from ggviews import ggplot, aes, scale_fill_discrete
    >>> import pandas as pd
    >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9], 'group': ['A', 'B', 'C']})
    >>> (ggplot(data, aes(x='x', y='y', fill='group'))
    ...     .geom_point()
    ...     .scale_fill_discrete(palette='Category20')
    ... )
    """
    return ScaleColorDiscreet(
        aesthetic='fill',
        name=name,
        breaks=breaks,
        labels=labels,
        limits=limits,
        palette=palette,
        na_value=na_value,
        guide=guide,
    )