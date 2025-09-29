"""
Advanced color scales for ggviews

This module implements the complete viridis family and other advanced
color scales to achieve visual parity with ggplot2.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Union, List
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from .scales import Scale


# Viridis color palettes (copied from matplotlib/viridis)
VIRIDIS_PALETTES = {
    'viridis': [
        '#440154', '#482777', '#3f4a8a', '#31678e', '#26838f', 
        '#1f9d8a', '#6cce5a', '#b6de2b', '#fee825'
    ],
    'plasma': [
        '#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786',
        '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'
    ],
    'inferno': [
        '#000004', '#1b0c41', '#4a0c6b', '#781c6d', '#a52c60',
        '#cf4446', '#ed6925', '#fb9b06', '#f7d03c', '#fcffa4'
    ],
    'magma': [
        '#000004', '#180f3d', '#440f76', '#721f81', '#9f2f7f',
        '#cd4071', '#f1605d', '#fd9668', '#feca57', '#fcfdbf'
    ],
    'cividis': [
        '#00224e', '#123570', '#3b496c', '#575d6d', '#707173',
        '#8a8678', '#a59c74', '#c3b369', '#e1cc55', '#fde725'
    ]
}


class scale_colour_viridis_c(Scale):
    """Continuous viridis color scale
    
    The viridis color scales are perceptually-uniform color scales that are
    designed to be colorblind-friendly and print well in grayscale.
    
    Args:
        alpha: Transparency level (0-1)
        begin: Starting point in palette (0-1) 
        end: Ending point in palette (0-1)
        direction: Direction of colors (1=normal, -1=reversed)
        option: Color palette ('A'=magma, 'B'=inferno, 'C'=plasma, 'D'=viridis, 'E'=cividis)
        name: Legend title
        guide: Legend guide specification
        **kwargs: Additional parameters
        
    Examples:
        scale_colour_viridis_c()  # Default viridis
        scale_colour_viridis_c(option='plasma')
        scale_colour_viridis_c(direction=-1)  # Reversed
        scale_colour_viridis_c(begin=0.2, end=0.8)  # Subset
    """
    
    def __init__(self, alpha=None, begin=0, end=1, direction=1, option='viridis', 
                 name=None, guide='colorbar', **kwargs):
        super().__init__('color', **kwargs)
        self.alpha = alpha
        self.begin = begin
        self.end = end
        self.direction = direction
        self.option = option
        self.name = name
        self.guide = guide
        
        # Map option letters to palette names
        option_map = {
            'A': 'magma',
            'B': 'inferno', 
            'C': 'plasma',
            'D': 'viridis',
            'E': 'cividis'
        }
        
        if option in option_map:
            self.palette_name = option_map[option]
        elif option in VIRIDIS_PALETTES:
            self.palette_name = option
        else:
            self.palette_name = 'viridis'
            
        self.colors = VIRIDIS_PALETTES[self.palette_name]
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply viridis continuous color scale"""
        if not hasattr(ggplot_obj, 'mapping') or 'color' not in ggplot_obj.mapping.mappings:
            return plot
            
        color_col = ggplot_obj.mapping.mappings['color']
        if color_col not in data.columns:
            return plot
            
        values = data[color_col].dropna()
        if len(values) == 0:
            return plot
            
        # Normalize values to [0, 1]
        vmin, vmax = values.min(), values.max()
        if vmax > vmin:
            normalized = (values - vmin) / (vmax - vmin)
        else:
            normalized = np.ones_like(values) * 0.5
            
        # Apply begin/end trimming
        normalized = normalized * (self.end - self.begin) + self.begin
        
        # Apply direction
        if self.direction == -1:
            normalized = 1 - normalized
            
        # Create color mapping
        n_colors = len(self.colors)
        color_indices = (normalized * (n_colors - 1)).astype(int)
        color_indices = np.clip(color_indices, 0, n_colors - 1)
        
        # Map to hex colors
        hex_colors = [self.colors[i] for i in color_indices]
        
        # Store color mapping
        ggplot_obj.viridis_color_map = dict(zip(values.index, hex_colors))
        
        return plot


class scale_colour_viridis_d(Scale):
    """Discrete viridis color scale
    
    Args:
        alpha: Transparency level (0-1)
        begin: Starting point in palette (0-1)
        end: Ending point in palette (0-1) 
        direction: Direction of colors (1=normal, -1=reversed)
        option: Color palette ('A'=magma, 'B'=inferno, 'C'=plasma, 'D'=viridis, 'E'=cividis)
        name: Legend title
        guide: Legend guide specification
        **kwargs: Additional parameters
    """
    
    def __init__(self, alpha=None, begin=0, end=1, direction=1, option='viridis',
                 name=None, guide='legend', **kwargs):
        super().__init__('color', **kwargs)
        self.alpha = alpha
        self.begin = begin
        self.end = end
        self.direction = direction
        self.option = option
        self.name = name
        self.guide = guide
        
        # Map option letters to palette names
        option_map = {
            'A': 'magma',
            'B': 'inferno',
            'C': 'plasma', 
            'D': 'viridis',
            'E': 'cividis'
        }
        
        if option in option_map:
            self.palette_name = option_map[option]
        elif option in VIRIDIS_PALETTES:
            self.palette_name = option
        else:
            self.palette_name = 'viridis'
            
        self.colors = VIRIDIS_PALETTES[self.palette_name]
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply viridis discrete color scale"""
        if not hasattr(ggplot_obj, 'mapping') or 'color' not in ggplot_obj.mapping.mappings:
            return plot
            
        color_col = ggplot_obj.mapping.mappings['color']
        if color_col not in data.columns:
            return plot
            
        unique_vals = sorted(data[color_col].dropna().unique())
        n_vals = len(unique_vals)
        
        if n_vals == 0:
            return plot
            
        # Select colors from palette
        n_palette = len(self.colors)
        
        # Apply begin/end trimming to palette
        start_idx = int(self.begin * (n_palette - 1))
        end_idx = int(self.end * (n_palette - 1))
        
        if end_idx > start_idx:
            selected_colors = self.colors[start_idx:end_idx + 1]
        else:
            selected_colors = self.colors
            
        # Apply direction
        if self.direction == -1:
            selected_colors = selected_colors[::-1]
            
        # Distribute colors evenly across unique values
        if n_vals <= len(selected_colors):
            # Use evenly spaced colors
            indices = np.linspace(0, len(selected_colors) - 1, n_vals, dtype=int)
            assigned_colors = [selected_colors[i] for i in indices]
        else:
            # Repeat colors if needed
            assigned_colors = (selected_colors * ((n_vals // len(selected_colors)) + 1))[:n_vals]
            
        # Create color mapping
        color_mapping = dict(zip(unique_vals, assigned_colors))
        ggplot_obj.viridis_discrete_map = color_mapping
        
        return plot


# Convenience functions for different viridis options
def scale_colour_viridis(**kwargs):
    """Alias for scale_colour_viridis_c"""
    return scale_colour_viridis_c(**kwargs)


def scale_color_viridis_c(**kwargs):
    """American spelling alias"""
    return scale_colour_viridis_c(**kwargs)


def scale_color_viridis_d(**kwargs):
    """American spelling alias"""
    return scale_colour_viridis_d(**kwargs)


def scale_color_viridis(**kwargs):
    """American spelling alias"""
    return scale_colour_viridis_c(**kwargs)


# Fill scale variants
def scale_fill_viridis_c(**kwargs):
    """Continuous viridis fill scale"""
    scale = scale_colour_viridis_c(**kwargs)
    scale.aesthetic = 'fill'
    return scale


def scale_fill_viridis_d(**kwargs):
    """Discrete viridis fill scale"""
    scale = scale_colour_viridis_d(**kwargs)
    scale.aesthetic = 'fill'
    return scale


def scale_fill_viridis(**kwargs):
    """Alias for scale_fill_viridis_c"""
    return scale_fill_viridis_c(**kwargs)


# Specific palette functions
def scale_colour_plasma_c(**kwargs):
    """Continuous plasma color scale"""
    return scale_colour_viridis_c(option='plasma', **kwargs)


def scale_colour_plasma_d(**kwargs):
    """Discrete plasma color scale"""
    return scale_colour_viridis_d(option='plasma', **kwargs)


def scale_colour_inferno_c(**kwargs):
    """Continuous inferno color scale"""
    return scale_colour_viridis_c(option='inferno', **kwargs)


def scale_colour_inferno_d(**kwargs):
    """Discrete inferno color scale"""
    return scale_colour_viridis_d(option='inferno', **kwargs)


def scale_colour_magma_c(**kwargs):
    """Continuous magma color scale"""
    return scale_colour_viridis_c(option='magma', **kwargs)


def scale_colour_magma_d(**kwargs):
    """Discrete magma color scale"""
    return scale_colour_viridis_d(option='magma', **kwargs)


def scale_colour_cividis_c(**kwargs):
    """Continuous cividis color scale"""
    return scale_colour_viridis_c(option='cividis', **kwargs)


def scale_colour_cividis_d(**kwargs):
    """Discrete cividis color scale"""
    return scale_colour_viridis_d(option='cividis', **kwargs)


# Export all viridis scales
__all__ = [
    'scale_colour_viridis_c',
    'scale_colour_viridis_d', 
    'scale_colour_viridis',
    'scale_color_viridis_c',
    'scale_color_viridis_d',
    'scale_color_viridis',
    'scale_fill_viridis_c',
    'scale_fill_viridis_d',
    'scale_fill_viridis',
    'scale_colour_plasma_c',
    'scale_colour_plasma_d',
    'scale_colour_inferno_c',
    'scale_colour_inferno_d',
    'scale_colour_magma_c',
    'scale_colour_magma_d',
    'scale_colour_cividis_c',
    'scale_colour_cividis_d',
]