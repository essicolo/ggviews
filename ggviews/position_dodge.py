"""
Position dodge implementation for side-by-side positioning
"""

import pandas as pd
import numpy as np
from .positions import PositionAdjustment

class position_dodge(PositionAdjustment):
    """Dodge overlapping objects side-by-side
    
    Adjusts position by dodging overlaps to the side. Useful for bar charts,
    box plots, and other geoms where you want to display multiple groups
    side-by-side rather than stacked.
    
    Args:
        width: Dodging width (default: 0.9)
        preserve: How to treat groups ('total' or 'single')
        
    Examples:
        # Side-by-side bars
        geom_bar(position=position_dodge(width=0.9))
        
        # Side-by-side boxplots  
        geom_boxplot(position=position_dodge(width=0.8))
    """
    
    def __init__(self, width=0.9, preserve='total'):
        self.width = width
        self.preserve = preserve
    
    def _adjust_positions(self, data, combined_aes, geom_type='bar'):
        """Adjust positions for dodging"""
        
        # Find grouping variables
        x_col = combined_aes.mappings.get('x')
        group_col = combined_aes.mappings.get('fill') or combined_aes.mappings.get('color')
        
        if not x_col or not group_col:
            return data  # No adjustment needed
        
        if x_col not in data.columns or group_col not in data.columns:
            return data
        
        # Create adjusted data
        adjusted_data = data.copy()
        
        # Group by x values
        for x_val in data[x_col].unique():
            mask = data[x_col] == x_val
            subset = data[mask]
            
            if group_col in subset.columns:
                groups = subset[group_col].unique()
                n_groups = len(groups)
                
                if n_groups <= 1:
                    continue
                
                # Calculate dodge positions
                total_width = self.width
                group_width = total_width / n_groups
                
                # Center the groups around the original x position
                start_offset = -(total_width - group_width) / 2
                
                for i, group in enumerate(groups):
                    group_mask = mask & (data[group_col] == group)
                    
                    # Calculate new x position
                    offset = start_offset + i * group_width
                    
                    if geom_type == 'bar':
                        # For bars, adjust the x position
                        adjusted_data.loc[group_mask, x_col + '_dodge'] = x_val + offset
                    else:
                        # For other geoms, might need different adjustment
                        adjusted_data.loc[group_mask, x_col + '_dodge'] = x_val + offset
        
        return adjusted_data
    
    def _apply_to_geom(self, geom, data, combined_aes):
        """Apply dodging to a specific geom"""
        
        # Determine geom type
        geom_type = 'bar'  # Default assumption
        if hasattr(geom, '__class__'):
            class_name = geom.__class__.__name__.lower()
            if 'box' in class_name:
                geom_type = 'box'
            elif 'point' in class_name:
                geom_type = 'point'
            elif 'line' in class_name:
                geom_type = 'line'
        
        # Adjust positions
        adjusted_data = self._adjust_positions(data, combined_aes, geom_type)
        
        return adjusted_data


# Export
__all__ = ['position_dodge']