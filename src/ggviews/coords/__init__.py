"""
Coordinate systems for ggviews.

This module provides coordinate systems functionality, similar to ggplot2's coord_* functions.
"""

from .coords import CoordinateSystem, CartesianCoord, PolarCoord

__all__ = ["CoordinateSystem", "CartesianCoord", "PolarCoord"]
