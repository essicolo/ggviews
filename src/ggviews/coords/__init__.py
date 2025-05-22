"""
Coordinate systems for ggviews.

This module provides coordinate systems functionality, similar to ggplot2's coord_* functions.
"""

from .base import CoordinateSystem
from .cartesian import CartesianCoord
from .polar import PolarCoord
from .flip import FlippedCoord, coord_flip

__all__ = [
    "CoordinateSystem", 
    "CartesianCoord", 
    "PolarCoord",
    "FlippedCoord",
    "coord_flip"
]
