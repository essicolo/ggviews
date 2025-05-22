"""
Box plot geometry for ggviews.

This module implements the box plot geometry.
"""
from typing import Dict, List, Optional, Union, Any, Tuple

import holoviews as hv
import pandas as pd
import numpy as np

from .base import Layer


class GeomBoxplot(Layer):
    """Box plot geometry.
    
    Parameters
    ----------
    mapping : dict, optional
        Aesthetic mappings.
    data : pd.DataFrame, optional
        Data to use for the geometry.
    stat : str, default 'boxplot'
        Statistical transformation to use.
    position : str, default 'dodge'
        Position adjustment to use.
    outlier_color : str, default 'black'
        Color for outlier points.
    outlier_shape : str, default 'circle'
        Shape for outlier points.
    outlier_size : float, default 1.5
        Size for outlier points.
    outlier_alpha : float, default 1.0
        Alpha transparency for outlier points.
    notch : bool, default False
        Whether to draw a notched box plot.
    notchwidth : float, default 0.5
        Width of the notch relative to the box.
    varwidth : bool, default False
        Whether to vary the box width by the number of observations.
    **kwargs : dict
        Additional parameters passed to the plot.
    """
    
    def __init__(
        self,
        mapping: Optional[Dict[str, str]] = None,
        data: Optional[pd.DataFrame] = None,
        outlier_color: str = 'black',
        outlier_shape: str = 'circle',
        outlier_size: float = 1.5,
        outlier_alpha: float = 1.0,
        notch: bool = False,
        notchwidth: float = 0.5,
        varwidth: bool = False,
        **kwargs
    ):
        super().__init__(data, mapping, **kwargs)
        self.outlier_color = outlier_color
        self.outlier_shape = outlier_shape
        self.outlier_size = outlier_size
        self.outlier_alpha = outlier_alpha
        self.notch = notch
        self.notchwidth = notchwidth
        self.varwidth = varwidth
    
    def create_element(self, data: pd.DataFrame, mapping: Dict[str, str]) -> hv.Element:
        """Create a box plot.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data to use for the plot.
        mapping : dict
            Aesthetic mappings.
        
        Returns
        -------
        hv.Element
            A Holoviews box plot element.
        """
        # Validate required aesthetics
        required_aes = ['y']
        # Skip validation for now
        
        # Get aesthetics
        y = mapping.get('y')
        x = mapping.get('x')
        group = mapping.get('group', mapping.get('color', mapping.get('fill')))
        
        # If x is not provided, use a constant
        if x is None:
            data = data.copy()
            data['__x__'] = 1
            x = '__x__'
        
        # Create box plot options
        box_opts = {
            'box_fill_color': mapping.get('fill', 'blue'),
            'box_line_color': mapping.get('color', 'black'),
            'box_alpha': mapping.get('alpha', 0.7),
            'outlier_color': self.outlier_color,
            'outlier_size': self.outlier_size,
            'outlier_alpha': self.outlier_alpha,
        }
        
        # Add other style options from kwargs
        box_opts.update(self._aes_kwargs)
        
        # Create the box plot
        if group is not None:
            # Group by both x and group
            boxplot = hv.BoxWhisker(data, [x, group], y)
        else:
            # Group by x only
            boxplot = hv.BoxWhisker(data, x, y)
        
        # Apply options
        boxplot = boxplot.opts(**box_opts)
        
        return boxplot