"""
Scales for ggviews.

This module provides scale transformation functionality, similar to ggplot2's scale_* functions.
"""

from .scales import Scale, ScaleContinuous, ScaleDiscreet, scale_x_log10, scale_y_log10

__all__ = ["Scale", "ScaleContinuous", "ScaleDiscreet", "scale_x_log10", "scale_y_log10"]
