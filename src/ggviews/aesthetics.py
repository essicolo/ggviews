"""
Aesthetics module for ggviews.

This module implements functionality for mapping aesthetic attributes to data variables.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any, Callable


@dataclass
class Aesthetics:
    """Class representing aesthetic mappings from data variables to visual elements.
    
    Parameters
    ----------
    x : Optional[str], default=None
        Data variable to map to the x-axis position.
    y : Optional[str], default=None
        Data variable to map to the y-axis position.
    color : Optional[str], default=None
        Data variable to map to color.
    fill : Optional[str], default=None
        Data variable to map to fill color.
    alpha : Optional[str], default=None
        Data variable to map to opacity.
    size : Optional[str], default=None
        Data variable to map to size.
    shape : Optional[str], default=None
        Data variable to map to shape.
    linetype : Optional[str], default=None
        Data variable to map to line type.
    linewidth : Optional[str], default=None
        Data variable to map to line width.
    group : Optional[str], default=None
        Data variable to use for grouping.
    label : Optional[str], default=None
        Data variable to use for labels.
    **kwargs : Any
        Additional aesthetic mappings.
    
    Examples
    --------
    >>> aes = Aesthetics(x='mpg', y='hp', color='cyl')
    >>> aes.get_mappings()
    {'x': 'mpg', 'y': 'hp', 'color': 'cyl'}
    """
    
    x: Optional[str] = None
    y: Optional[str] = None
    color: Optional[str] = None
    fill: Optional[str] = None
    alpha: Optional[str] = None
    size: Optional[str] = None
    shape: Optional[str] = None
    linetype: Optional[str] = None
    linewidth: Optional[str] = None
    group: Optional[str] = None
    label: Optional[str] = None
    _extra_mappings: Dict[str, Any] = field(default_factory=dict)
    
    def __init__(self, **kwargs):
        """Initialize the Aesthetics object with the provided mappings."""
        # Initialize _extra_mappings explicitly
        self._extra_mappings = {}
        
        for key, value in kwargs.items():
            if hasattr(self, key) and key != '_extra_mappings':
                setattr(self, key, value)
            else:
                self._extra_mappings[key] = value
    
    def get_mappings(self) -> Dict[str, Any]:
        """Get all aesthetic mappings.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary of aesthetic mappings.
        """
        mappings = {}
        for key in ['x', 'y', 'color', 'fill', 'alpha', 'size', 'shape', 
                   'linetype', 'linewidth', 'group', 'label']:
            value = getattr(self, key)
            if value is not None:
                mappings[key] = value
        
        mappings.update(self._extra_mappings)
        return mappings
    
    def to_holoviews(self) -> Dict[str, Any]:
        """Convert the aesthetic mappings to Holoviews kdims/vdims format.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary with 'kdims' and 'vdims' keys containing lists of dimensions.
        """
        mappings = self.get_mappings()
        
        # In Holoviews, dimensions used for positioning are kdims (key dimensions)
        # and dimensions used for other visual attributes are vdims (value dimensions)
        kdims = []
        vdims = []
        
        # Handle x and y as kdims
        if 'x' in mappings:
            kdims.append(mappings['x'])
        if 'y' in mappings:
            kdims.append(mappings['y'])
        
        # Handle all other aesthetics as vdims
        for key, value in mappings.items():
            if key not in ['x', 'y'] and value is not None:
                vdims.append(value)
        
        return {'kdims': kdims, 'vdims': vdims}


def aes(**kwargs) -> Aesthetics:
    """Create an Aesthetics object with the provided mappings.
    
    Parameters
    ----------
    **kwargs : Any
        Aesthetic mappings.
    
    Returns
    -------
    Aesthetics
        An Aesthetics object with the provided mappings.
    
    Examples
    --------
    >>> aes(x='mpg', y='hp', color='cyl')
    Aesthetics(x='mpg', y='hp', color='cyl', fill=None, alpha=None, size=None, 
              shape=None, linetype=None, linewidth=None, group=None, label=None)
    """
    return Aesthetics(**kwargs)