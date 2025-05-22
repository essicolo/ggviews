"""
Scales for ggviews.

This module provides scale transformation functionality, similar to ggplot2's scale_* functions.
"""

from .base import Scale
from .continuous import ScaleContinuous
from .discrete import ScaleDiscreet
from .log import scale_x_log10, scale_y_log10
from .color import (
    ScaleColorContinuous, 
    ScaleColorDiscreet,
    scale_color_continuous,
    scale_fill_continuous,
    scale_color_discrete,
    scale_fill_discrete
)

__all__ = [
    "Scale", 
    "ScaleContinuous", 
    "ScaleDiscreet", 
    "scale_x_log10", 
    "scale_y_log10",
    "ScaleColorContinuous",
    "ScaleColorDiscreet",
    "scale_color_continuous",
    "scale_fill_continuous",
    "scale_color_discrete",
    "scale_fill_discrete"
]
