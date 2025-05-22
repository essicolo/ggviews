"""
Violin plot geometry for ggviews.

This module implements the violin plot geometry.
"""
from typing import Dict, List, Optional, Union, Any, Tuple

import holoviews as hv
import pandas as pd
import numpy as np
from holoviews.element.stats import Violin

from .base import Layer


class GeomViolin(Layer):
    """Violin plot geometry.
    
    Parameters
    ----------
    mapping : dict, optional
        Aesthetic mappings.
    data : pd.DataFrame, optional
        Data to use for the geometry.
    stat : str, default 'violin'
        Statistical transformation to use.
    position : str, default 'dodge'
        Position adjustment to use.
    scale : str, default 'area'
        How to scale the violin width. Options: 'area', 'count', 'width'.
    trim : bool, default True
        Whether to trim the tails of the violin.
    kernel : str, default 'gaussian'
        Kernel to use for density estimation.
    bw : str or float, default 'scott'
        Bandwidth method or value for density estimation.
    **kwargs : dict
        Additional parameters passed to the plot.
    """
    
    def __init__(
        self,
        mapping: Optional[Dict[str, str]] = None,
        data: Optional[pd.DataFrame] = None,
        scale: str = 'area',
        trim: bool = True,
        kernel: str = 'gaussian',
        bw: Union[str, float] = 'scott',
        **kwargs
    ):
        super().__init__(data, mapping, **kwargs)
        self.scale = scale
        self.trim = trim
        self.kernel = kernel
        self.bw = bw
    
    def create_element(self, data: pd.DataFrame, mapping: Dict[str, str]) -> hv.Element:
        """Create a violin plot.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data to use for the plot.
        mapping : dict
            Aesthetic mappings.
        
        Returns
        -------
        hv.Element
            A Holoviews violin plot element.
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
        
        # Create violin plot options
        violin_opts = {
            'fill_color': mapping.get('fill', 'blue'),
            'line_color': mapping.get('color', 'black'),
            'alpha': mapping.get('alpha', 0.7),
        }
        
        # Add other style options from kwargs
        violin_opts.update(self._aes_kwargs)
        
        # Create the violin plot
        if group is not None:
            # Group by both x and group
            # First create a distribution element
            dist = hv.Distribution(data, y, [x, group])
            # Then convert to violin plot
            violinplot = Violin(dist)
        else:
            # Group by x only
            # First create a distribution element
            dist = hv.Distribution(data, y, x)
            # Then convert to violin plot
            violinplot = Violin(dist)
        
        # Apply options
        violinplot = violinplot.opts(**violin_opts)
        
        return violinplot