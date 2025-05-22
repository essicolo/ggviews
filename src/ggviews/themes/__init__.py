"""
Themes for ggviews.

This module provides theming functionality, similar to ggplot2's theme_* functions.
"""

from .base import Theme
from .presets import theme_default, theme_minimal, theme_bw, theme_ggplot2

__all__ = ["Theme", "theme_default", "theme_minimal", "theme_bw", "theme_ggplot2"]
