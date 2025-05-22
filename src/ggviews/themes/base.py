"""
Base theme class for ggviews.

This module defines the base Theme class for all themes.
"""
from typing import Dict, List, Optional, Union, Any, Tuple

import holoviews as hv


class Theme:
    """Base class for all themes.
    
    Parameters
    ----------
    name : str
        Name of the theme.
    opts : dict
        Options to apply for the theme.
    """
    
    def __init__(self, name: str, opts: Dict[str, Any]):
        self.name = name
        self.opts = opts
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the theme to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the theme to.
        
        Returns
        -------
        hv.Element
            The plot element with the theme applied.
        """
        return plot.opts(**self.opts)