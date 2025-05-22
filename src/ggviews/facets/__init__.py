"""
Facet functions for ggviews.

This module provides faceting functionality, similar to ggplot2's facet_* functions.
"""

from .facets import Facet, FacetGrid, FacetWrap, facet_grid, facet_wrap

__all__ = ["Facet", "FacetGrid", "FacetWrap", "facet_grid", "facet_wrap"]
