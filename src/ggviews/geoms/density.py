"""
Density plot geometry for ggviews.

This module implements the density plot geometry.
"""
from typing import Dict, List, Optional, Union, Any, Tuple

import holoviews as hv
import pandas as pd
import numpy as np

from .base import Layer


class GeomDensity(Layer):
    """Density plot geometry.
    
    Parameters
    ----------
    mapping : dict, optional
        Aesthetic mappings.
    data : pd.DataFrame, optional
        Data to use for the geometry.
    stat : str, default 'density'
        Statistical transformation to use.
    position : str, default 'identity'
        Position adjustment to use.
    kernel : str, default 'gaussian'
        Kernel to use for density estimation.
    bw : str or float, default 'scott'
        Bandwidth method or value for density estimation.
    n : int, default 512
        Number of points to use for density estimation.
    trim : bool, default False
        Whether to trim the tails of the density.
    fill : bool, default False
        Whether to fill the area under the density curve.
    **kwargs : dict
        Additional parameters passed to the plot.
    """
    
    def __init__(
        self,
        mapping: Optional[Dict[str, str]] = None,
        data: Optional[pd.DataFrame] = None,
        kernel: str = 'gaussian',
        bw: Union[str, float] = 'scott',
        n: int = 512,
        trim: bool = False,
        fill: bool = False,
        **kwargs
    ):
        super().__init__(data, mapping, **kwargs)
        self.kernel = kernel
        self.bw = bw
        self.n = n
        self.trim = trim
        self.fill = fill
    
    def create_element(self, data: pd.DataFrame, mapping: Dict[str, str]) -> hv.Element:
        """Create a density plot.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data to use for the plot.
        mapping : dict
            Aesthetic mappings.
        
        Returns
        -------
        hv.Element
            A Holoviews density plot element.
        """
        # Validate required aesthetics
        required_aes = ['x']
        # Skip validation for now
        
        # Get aesthetics
        x = mapping.get('x')
        group = mapping.get('group', mapping.get('color', mapping.get('fill')))
        
        # Create density plot options
        density_opts = {
            'color': mapping.get('color', 'blue'),
            'alpha': mapping.get('alpha', 1.0),
            'line_width': mapping.get('size', 1.0),
        }
        
        # Add fill options if requested
        if self.fill:
            density_opts['fill_color'] = mapping.get('fill', 'blue')
            density_opts['fill_alpha'] = mapping.get('alpha', 0.3)
        
        # Add other style options from kwargs
        density_opts.update(self._aes_kwargs)
        
        # Create the density plot
        if group is not None:
            # Group by group
            densityplot = hv.Distribution(data, x, group)
        else:
            # No grouping
            densityplot = hv.Distribution(data, x)
        
        # Apply options
        densityplot = densityplot.opts(**density_opts)
        
        return densityplot