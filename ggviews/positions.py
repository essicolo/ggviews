"""
Position adjustments for ggviews

This module implements position adjustments that modify the position
of geoms to avoid overplotting or create specific arrangements.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List, Tuple
import warnings


class Position:
    """Base class for position adjustments"""
    
    def __init__(self, **kwargs):
        self.params = kwargs
    
    def adjust(self, data, combined_aes, layer_params):
        """Adjust positions - to be implemented by subclasses"""
        return data
    
    def __repr__(self):
        params_str = ', '.join([f"{k}={v}" for k, v in self.params.items()])
        return f"{self.__class__.__name__}({params_str})"


class position_identity(Position):
    """Identity position adjustment (no adjustment)
    
    This is the default position adjustment that leaves
    data coordinates unchanged.
    """
    
    def __init__(self):
        super().__init__()
    
    def adjust(self, data, combined_aes, layer_params):
        """Return data unchanged"""
        return data


class position_stack(Position):
    """Stack overlapping objects on top of each other
    
    Useful for bar charts and area plots where you want to show
    the cumulative effect of different groups.
    
    Args:
        vjust: Vertical justification (1=top, 0=bottom, 0.5=center)
        reverse: Reverse the stacking order
    """
    
    def __init__(self, vjust=1, reverse=False):
        super().__init__(vjust=vjust, reverse=reverse)
        self.vjust = vjust
        self.reverse = reverse
    
    def adjust(self, data, combined_aes, layer_params):
        """Stack values based on grouping variable"""
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            return data
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        # Determine grouping variable
        group_col = None
        for aes_name in ['fill', 'color', 'group']:
            if aes_name in combined_aes.mappings:
                group_col = combined_aes.mappings[aes_name]
                break
        
        if group_col is None or group_col not in data.columns:
            return data
        
        # Stack by x and group
        adjusted_data = data.copy()
        
        for x_val in data[x_col].unique():
            x_mask = data[x_col] == x_val
            x_data = data[x_mask].copy()
            
            if len(x_data) <= 1:
                continue
            
            # Sort by group for consistent stacking
            x_data = x_data.sort_values(group_col)
            
            if self.reverse:
                x_data = x_data.iloc[::-1]
            
            # Calculate cumulative positions
            cumulative_y = 0
            for idx, (_, row) in enumerate(x_data.iterrows()):
                original_y = row[y_col]
                
                if self.vjust == 1:  # Stack on top
                    new_y = cumulative_y + original_y
                elif self.vjust == 0:  # Stack from bottom
                    new_y = cumulative_y
                    cumulative_y += original_y
                else:  # Center
                    new_y = cumulative_y + original_y * self.vjust
                
                adjusted_data.loc[row.name, y_col] = new_y
                
                if self.vjust == 1:
                    cumulative_y = new_y
        
        return adjusted_data


class position_fill(position_stack):
    """Stack overlapping objects and standardize to fill the plot
    
    Similar to position_stack but normalizes so that the total height
    is always 1, showing proportions rather than absolute values.
    
    Args:
        vjust: Vertical justification
        reverse: Reverse the stacking order
    """
    
    def __init__(self, vjust=1, reverse=False):
        super().__init__(vjust=vjust, reverse=reverse)
    
    def adjust(self, data, combined_aes, layer_params):
        """Stack and normalize to proportions"""
        # First apply regular stacking
        stacked_data = super().adjust(data, combined_aes, layer_params)
        
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            return stacked_data
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        # Normalize by x group totals
        adjusted_data = stacked_data.copy()
        
        for x_val in stacked_data[x_col].unique():
            x_mask = stacked_data[x_col] == x_val
            x_group = stacked_data[x_mask]
            
            total = x_group[y_col].sum()
            if total > 0:
                adjusted_data.loc[x_mask, y_col] = stacked_data.loc[x_mask, y_col] / total
        
        return adjusted_data


class position_dodge(Position):
    """Dodge overlapping objects side-to-side
    
    Places overlapping objects beside each other, useful for
    grouped bar charts and similar plots.
    
    Args:
        width: Dodging width (0.9 = use 90% of resolution)
        preserve: Preserve total or single widths ('total', 'single')
    """
    
    def __init__(self, width=0.9, preserve='total'):
        super().__init__(width=width, preserve=preserve)
        self.width = width
        self.preserve = preserve
    
    def adjust(self, data, combined_aes, layer_params):
        """Dodge positions side-by-side"""
        if 'x' not in combined_aes.mappings:
            return data
        
        x_col = combined_aes.mappings['x']
        
        # Determine grouping variable
        group_col = None
        for aes_name in ['fill', 'color', 'group']:
            if aes_name in combined_aes.mappings:
                group_col = combined_aes.mappings[aes_name]
                break
        
        if group_col is None or group_col not in data.columns:
            return data
        
        adjusted_data = data.copy()
        
        for x_val in data[x_col].unique():
            x_mask = data[x_col] == x_val
            x_group = data[x_mask]
            
            unique_groups = x_group[group_col].unique()
            n_groups = len(unique_groups)
            
            if n_groups <= 1:
                continue
            
            # Calculate dodge positions
            dodge_width = self.width / n_groups
            start_offset = -self.width / 2 + dodge_width / 2
            
            for i, group_val in enumerate(unique_groups):
                group_mask = x_mask & (data[group_col] == group_val)
                offset = start_offset + i * dodge_width
                adjusted_data.loc[group_mask, x_col] = x_val + offset
        
        return adjusted_data


class position_jitter(Position):
    """Jitter points to reduce overplotting
    
    Adds small random offsets to points to make overlapping
    points visible.
    
    Args:
        width: Amount of horizontal jittering
        height: Amount of vertical jittering  
        seed: Random seed for reproducible jittering
    """
    
    def __init__(self, width=None, height=None, seed=None):
        super().__init__(width=width, height=height, seed=seed)
        self.width = width
        self.height = height
        self.seed = seed
    
    def adjust(self, data, combined_aes, layer_params):
        """Add random jitter to positions"""
        if self.seed is not None:
            np.random.seed(self.seed)
        
        adjusted_data = data.copy()
        
        # Jitter x positions
        if 'x' in combined_aes.mappings and self.width is not None:
            x_col = combined_aes.mappings['x']
            if x_col in data.columns:
                jitter_x = np.random.uniform(-self.width/2, self.width/2, len(data))
                adjusted_data[x_col] = data[x_col] + jitter_x
        
        # Jitter y positions  
        if 'y' in combined_aes.mappings and self.height is not None:
            y_col = combined_aes.mappings['y']
            if y_col in data.columns:
                jitter_y = np.random.uniform(-self.height/2, self.height/2, len(data))
                adjusted_data[y_col] = data[y_col] + jitter_y
        
        return adjusted_data


class position_nudge(Position):
    """Nudge points a fixed distance
    
    Moves all points by a fixed offset, useful for adjusting
    text labels or avoiding overlaps.
    
    Args:
        x: Horizontal nudge distance
        y: Vertical nudge distance
    """
    
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y)
        self.x = x
        self.y = y
    
    def adjust(self, data, combined_aes, layer_params):
        """Nudge all positions by fixed amounts"""
        adjusted_data = data.copy()
        
        if 'x' in combined_aes.mappings and self.x != 0:
            x_col = combined_aes.mappings['x']
            if x_col in data.columns:
                adjusted_data[x_col] = data[x_col] + self.x
        
        if 'y' in combined_aes.mappings and self.y != 0:
            y_col = combined_aes.mappings['y']
            if y_col in data.columns:
                adjusted_data[y_col] = data[y_col] + self.y
        
        return adjusted_data


class position_jitterdodge(Position):
    """Dodge and jitter to separate overlapping points
    
    Combines dodging and jittering for grouped data with overplotting.
    
    Args:
        dodge_width: Width for dodging groups
        jitter_width: Width for jittering within groups
        jitter_height: Height for vertical jittering
        seed: Random seed
    """
    
    def __init__(self, dodge_width=0.9, jitter_width=0.4, jitter_height=0, seed=None):
        super().__init__(dodge_width=dodge_width, jitter_width=jitter_width,
                         jitter_height=jitter_height, seed=seed)
        self.dodge = position_dodge(width=dodge_width)
        self.jitter = position_jitter(width=jitter_width, height=jitter_height, seed=seed)
    
    def adjust(self, data, combined_aes, layer_params):
        """Apply dodging then jittering"""
        # First dodge
        dodged_data = self.dodge.adjust(data, combined_aes, layer_params)
        
        # Then jitter
        return self.jitter.adjust(dodged_data, combined_aes, layer_params)


# The classes above serve as both the class definition and the callable constructor.
# No separate convenience functions needed -- instantiate classes directly:
#   position_identity(), position_stack(), position_dodge(width=0.9), etc.


# Export all position classes and functions
__all__ = [
    'Position',
    'position_identity',
    'position_stack', 
    'position_fill',
    'position_dodge',
    'position_jitter',
    'position_nudge',
    'position_jitterdodge',
]