"""
Facet functions for ggviews.

This module provides faceting functionality, similar to ggplot2's facet_* functions.
"""

from .base import Facet
from .grid import FacetGrid, facet_grid
from .wrap import FacetWrap, facet_wrap

__all__ = ["Facet", "FacetGrid", "FacetWrap", "facet_grid", "facet_wrap"]
