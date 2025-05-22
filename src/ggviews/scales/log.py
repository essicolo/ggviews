"""
Log scale functions for ggviews.

This module defines log scale functions for ggviews.
"""
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

from .continuous import ScaleContinuous


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