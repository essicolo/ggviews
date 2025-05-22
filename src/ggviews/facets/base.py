"""
Base facet class for ggviews.

This module defines the base Facet class for all faceting.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

import holoviews as hv


class Facet(ABC):
    """Base class for all facets."""
    
    @abstractmethod
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the faceting to a plot element.
        
        Parameters
        ----------
        plot : hv.Element
            The plot element to apply the faceting to.
        
        Returns
        -------
        hv.Element
            The plot element with the faceting applied.
        """
        pass