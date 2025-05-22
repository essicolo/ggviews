"""
Geometry layers for ggviews.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple, Callable

from ..aes import Aesthetics


def is_valid_dimension_name(value, data):
    """Check if a value is a valid dimension name (column name in the DataFrame).
    
    Parameters
    ----------
    value : Any
        The value to check.
    data : pandas.DataFrame
        The DataFrame to check against.
        
    Returns
    -------
    bool
        True if the value is a string and is a column name in the DataFrame.
    """
    # Check if value is a string and is a column name in the DataFrame
    if isinstance(value, str) and hasattr(data, 'columns') and value in data.columns:
        return True
    return False


class Layer(ABC):
    """Base class for all layers."""
    
    def __init__(
        self,
        data: Optional[pd.DataFrame] = None,
        mapping: Optional[Aesthetics] = None,
        **aes_kwargs
    ):
        # Enhanced fix for case when an Aesthetics object is passed as the first argument (data)
        # This happens when users call geom_point(aes(color='cyl'), size=5) etc.
        if isinstance(data, Aesthetics) and mapping is None:
            mapping = data
            data = None
        
        self.data = data
        self._mapping = mapping if mapping is not None else Aesthetics()
        
        # Handle aes() objects and regular kwargs
        self._aes_kwargs = {}
        for key, value in aes_kwargs.items():
            if isinstance(value, Aesthetics):
                # Merge mappings from the aes() object into _mapping
                for aes_key, aes_value in value.get_mappings().items():
                    setattr(self._mapping, aes_key, aes_value)
            else:
                # Store regular key-value pairs in _aes_kwargs
                self._aes_kwargs[key] = value
                
        self.stat = None
        self.position = None
        self.opts = {}
    
    def get_mapping(self, plot_mapping: Optional[Aesthetics] = None) -> Aesthetics:
        """Get the aesthetic mapping for this layer.
        
        If the layer has its own mapping, it is used. Otherwise, the plot's mapping is used.
        Layer-specific kwargs override both.
        
        Parameters
        ----------
        plot_mapping : Aesthetics, optional
            The plot's aesthetic mapping.
        
        Returns
        -------
        Aesthetics
            The aesthetic mapping for this layer.
        """
        # Start with plot mapping
        mapping = Aesthetics()
        
        # If a plot mapping is provided, use it as the base
        if plot_mapping is not None:
            for key, value in plot_mapping.get_mappings().items():
                setattr(mapping, key, value)
        
        # If the layer has its own mapping, it overrides the plot mapping
        if self._mapping is not None:
            for key, value in self._mapping.get_mappings().items():
                setattr(mapping, key, value)
        
        # If the layer has additional aesthetic kwargs, they override both
        for key, value in self._aes_kwargs.items():
            if hasattr(mapping, key):
                setattr(mapping, key, value)
            else:
                mapping._extra_mappings[key] = value
        
        return mapping
    
    def get_data(self, plot_data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Get the data for this layer.
        
        If the layer has its own data, it is used. Otherwise, the plot's data is used.
        
        Parameters
        ----------
        plot_data : pandas.DataFrame, optional
            The plot's data.
        
        Returns
        -------
        pandas.DataFrame
            The data for this layer.
        """
        return self.data if self.data is not None else plot_data
    
    @abstractmethod
    def create_element(self, data: pd.DataFrame, mapping: Aesthetics) -> hv.Element:
        """Create the Holoviews element for this layer.
        
        Parameters
        ----------
        data : pandas.DataFrame
            The data for this layer.
        mapping : Aesthetics
            The aesthetic mapping for this layer.
        
        Returns
        -------
        hv.Element
            The Holoviews element for this layer.
        """
        pass
    
    def build(
        self, plot_data: Optional[pd.DataFrame] = None, plot_mapping: Optional[Aesthetics] = None
    ) -> hv.Element:
        """Build the Holoviews element for this layer.

        Parameters
        ----------
        plot_data : pandas.DataFrame, optional
            The plot's data.
        plot_mapping : Aesthetics, optional
            The plot's aesthetic mapping.

        Returns
        -------
        hv.Element
            The Holoviews element for this layer.
        """
        data = self.get_data(plot_data)

        # Safety check to ensure data is a DataFrame
        if data is None:
            raise ValueError("No data provided for the layer. Make sure to pass data to the plot or layer.")
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"Expected a pandas DataFrame, got {type(data).__name__} instead.")

        mapping = self.get_mapping(plot_mapping)

        # Apply the stat transformation if one is specified
        if self.stat is not None:
            data = self.stat.transform(data, mapping)

        # Create the element
        element = self.create_element(data, mapping)

        # Apply the position adjustment if one is specified
        if self.position is not None:
            element = self.position.apply(element)

        # Apply any options
        if self.opts:
            element = element.opts(**self.opts)

        return element