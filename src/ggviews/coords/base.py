"""
Base coordinate system class for ggviews.

This module defines the base CoordinateSystem class for all coordinate systems.
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