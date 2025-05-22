"""
Base scale classes for ggviews.

This module defines the base Scale class for all scale transformations.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

import holoviews as hv


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