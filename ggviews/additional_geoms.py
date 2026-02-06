"""
Additional geometric objects for ggviews

This module implements additional geoms commonly used in ggplot2
including ribbon, violin, text, and more specialized plot types.
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List
import warnings
from .geoms import GeomLayer


class geom_ribbon(GeomLayer):
    """Ribbon plots (confidence bands, error ribbons)
    
    Creates ribbons between ymin and ymax values, commonly used
    for confidence intervals around trend lines.
    
    Args:
        mapping: Aesthetic mappings (x, ymin, ymax, fill, color, alpha)
        data: Data for this layer
        alpha: Transparency (0-1)
        fill: Fill color
        color: Border color  
        size: Border width
        **kwargs: Additional parameters
        
    Examples:
        geom_ribbon(aes(x='x', ymin='lower', ymax='upper'), alpha=0.3)
        geom_ribbon(aes(x='x', ymin='y-se', ymax='y+se', fill='group'))
    """
    
    def __init__(self, mapping=None, data=None, alpha=0.5, fill=None, 
                 color=None, size=0, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'alpha': alpha,
            'fill': fill,
            'color': color,
            'size': size
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render ribbon plot"""
        required_aes = ['x', 'ymin', 'ymax']
        for aes_name in required_aes:
            if aes_name not in combined_aes.mappings:
                raise ValueError(f"geom_ribbon requires {aes_name} aesthetic")
        
        x_col = combined_aes.mappings['x']
        ymin_col = combined_aes.mappings['ymin']
        ymax_col = combined_aes.mappings['ymax']
        
        missing_cols = [col for col in [x_col, ymin_col, ymax_col] 
                       if col not in data.columns]
        if missing_cols:
            warnings.warn(f"Required columns not found: {missing_cols}")
            return None
        
        # Sort by x for proper ribbon
        data_sorted = data.sort_values(x_col)
        x_data = data_sorted[x_col]
        ymin_data = data_sorted[ymin_col] 
        ymax_data = data_sorted[ymax_col]
        
        # Handle grouping/fill
        if 'fill' in combined_aes.mappings or 'group' in combined_aes.mappings:
            group_col = combined_aes.mappings.get('fill') or combined_aes.mappings.get('group')
            
            if group_col and group_col in data.columns:
                plot_data = []
                color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
                
                for group_val in data_sorted[group_col].unique():
                    mask = data_sorted[group_col] == group_val
                    if mask.any():
                        group_data = data_sorted[mask].sort_values(x_col)
                        
                        # Create ribbon coordinates (x, y pairs for area)
                        x_ribbon = np.concatenate([
                            group_data[x_col].values,
                            group_data[x_col].values[::-1]
                        ])
                        y_ribbon = np.concatenate([
                            group_data[ymax_col].values,
                            group_data[ymin_col].values[::-1]
                        ])
                        
                        ribbon_data = pd.DataFrame({'x': x_ribbon, 'y': y_ribbon})
                        
                        # Get color for this group
                        if color_map and group_val in color_map:
                            ribbon_color = color_map[group_val]
                        else:
                            ribbon_color = self.params.get('fill', ggplot_obj.default_colors[0])
                        
                        ribbon = hv.Area(ribbon_data).opts(
                            color=ribbon_color,
                            alpha=self.params['alpha'],
                            tools=['hover']
                        )
                        plot_data.append(ribbon)
                
                if plot_data:
                    return hv.Overlay(plot_data)
        else:
            # Single ribbon
            x_ribbon = np.concatenate([x_data.values, x_data.values[::-1]])
            y_ribbon = np.concatenate([ymax_data.values, ymin_data.values[::-1]])
            
            ribbon_data = pd.DataFrame({'x': x_ribbon, 'y': y_ribbon})
            ribbon_color = self.params.get('fill', self.params.get('color', '#1f77b4'))
            
            return hv.Area(ribbon_data).opts(
                color=ribbon_color,
                alpha=self.params['alpha'],
                tools=['hover']
            )


class geom_violin(GeomLayer):
    """Violin plots
    
    Shows the distribution of data through kernel density estimation
    on each side, creating a violin-like shape.
    
    Args:
        mapping: Aesthetic mappings (x, y, fill, color)
        data: Data for this layer
        trim: Trim the violin to data range
        scale: How to scale violins ('area', 'count', 'width')
        alpha: Transparency
        fill: Fill color
        color: Border color
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, trim=True, scale='area',
                 alpha=0.7, fill=None, color=None, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'trim': trim,
            'scale': scale,
            'alpha': alpha,
            'fill': fill,
            'color': color
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render violin plot using HoloViews Violin element"""
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("geom_violin requires both x and y aesthetics")

        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']

        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Required columns not found: {x_col}, {y_col}")
            return None

        # Use HoloViews Violin element which handles categorical x properly
        violin_data = data[[x_col, y_col]].dropna()
        if violin_data.empty:
            return None

        color = self.params.get('fill') or self.params.get('color') or ggplot_obj.default_colors[0]

        try:
            return hv.Violin(violin_data, kdims=[x_col], vdims=[y_col]).opts(
                violin_fill_color=color,
                violin_fill_alpha=self.params['alpha'],
                inner='box',
                tools=['hover'],
            )
        except Exception:
            # Fallback: use BoxWhisker if Violin is not available
            return hv.BoxWhisker(violin_data, kdims=[x_col], vdims=[y_col]).opts(
                box_fill_color=color,
                box_alpha=self.params['alpha'],
                tools=['hover'],
            )


class geom_text(GeomLayer):
    """Text annotations
    
    Add text labels to plots at specified positions.
    
    Args:
        mapping: Aesthetic mappings (x, y, label, color, size, angle)
        data: Data for this layer
        nudge_x: Horizontal adjustment
        nudge_y: Vertical adjustment  
        size: Text size
        color: Text color
        alpha: Text transparency
        fontface: Font face ('plain', 'bold', 'italic')
        family: Font family
        hjust: Horizontal justification (0=left, 0.5=center, 1=right)
        vjust: Vertical justification (0=bottom, 0.5=center, 1=top)
        check_overlap: Whether to avoid overlapping text
        **kwargs: Additional parameters
        
    Examples:
        geom_text(aes(x='x', y='y', label='name'))
        geom_text(aes(x='x', y='y', label='value'), nudge_y=0.1)
    """
    
    def __init__(self, mapping=None, data=None, nudge_x=0, nudge_y=0,
                 size=12, color='black', alpha=1, fontface='plain',
                 family='Arial', hjust=0.5, vjust=0.5, check_overlap=False,
                 **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'nudge_x': nudge_x,
            'nudge_y': nudge_y,
            'size': size,
            'color': color,
            'alpha': alpha,
            'fontface': fontface,
            'family': family,
            'hjust': hjust,
            'vjust': vjust,
            'check_overlap': check_overlap
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render text annotations using hv.Labels"""
        required_aes = ['x', 'y', 'label']
        for aes_name in required_aes:
            if aes_name not in combined_aes.mappings:
                raise ValueError(f"geom_text requires {aes_name} aesthetic")

        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        label_col = combined_aes.mappings['label']

        missing_cols = [col for col in [x_col, y_col, label_col]
                       if col not in data.columns]
        if missing_cols:
            warnings.warn(f"Required columns not found: {missing_cols}")
            return None

        # Apply nudging
        x_data = data[x_col] + self.params['nudge_x']
        y_data = data[y_col] + self.params['nudge_y']
        labels = data[label_col].astype(str)

        text_color = self.params.get('color', 'black')
        text_size = self.params.get('size', 12)

        # Build label data
        label_data = pd.DataFrame({'x': x_data, 'y': y_data, 'text': labels}).dropna()

        if label_data.empty:
            return None

        # Use hv.Labels for proper text rendering
        return hv.Labels(label_data, kdims=['x', 'y'], vdims=['text']).opts(
            text_color=text_color,
            text_font_size=f'{text_size}pt',
            text_alpha=self.params['alpha'],
        )


class geom_errorbar(GeomLayer):
    """Error bars
    
    Display error bars showing uncertainty or variation in data.
    
    Args:
        mapping: Aesthetic mappings (x, ymin, ymax, width, color)
        data: Data for this layer  
        width: Width of error bar caps
        color: Error bar color
        size: Line width
        alpha: Transparency
        **kwargs: Additional parameters
        
    Examples:
        geom_errorbar(aes(x='treatment', ymin='lower', ymax='upper'))
        geom_errorbar(aes(x='x', ymin='y-se', ymax='y+se'), width=0.2)
    """
    
    def __init__(self, mapping=None, data=None, width=0.1, color='black',
                 size=1, alpha=1, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'width': width,
            'color': color,
            'size': size,
            'alpha': alpha
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render error bars"""
        required_aes = ['x', 'ymin', 'ymax']
        for aes_name in required_aes:
            if aes_name not in combined_aes.mappings:
                raise ValueError(f"geom_errorbar requires {aes_name} aesthetic")
        
        x_col = combined_aes.mappings['x']
        ymin_col = combined_aes.mappings['ymin']
        ymax_col = combined_aes.mappings['ymax']
        
        missing_cols = [col for col in [x_col, ymin_col, ymax_col] 
                       if col not in data.columns]
        if missing_cols:
            warnings.warn(f"Required columns not found: {missing_cols}")
            return None
        
        # Create error bar elements
        error_elements = []
        width = self.params['width']
        color = self.params.get('color', 'black')
        
        for _, row in data.iterrows():
            x = row[x_col]
            ymin = row[ymin_col] 
            ymax = row[ymax_col]
            
            if pd.notna(x) and pd.notna(ymin) and pd.notna(ymax):
                # Vertical line from ymin to ymax
                vline_data = pd.DataFrame({'x': [x, x], 'y': [ymin, ymax]})
                vline = hv.Curve(vline_data).opts(color=color, line_width=self.params['size'])
                
                # Bottom cap
                bottom_cap = pd.DataFrame({
                    'x': [x - width/2, x + width/2], 
                    'y': [ymin, ymin]
                })
                bottom = hv.Curve(bottom_cap).opts(color=color, line_width=self.params['size'])
                
                # Top cap
                top_cap = pd.DataFrame({
                    'x': [x - width/2, x + width/2], 
                    'y': [ymax, ymax]
                })
                top = hv.Curve(top_cap).opts(color=color, line_width=self.params['size'])
                
                error_elements.extend([vline, bottom, top])
        
        if error_elements:
            return hv.Overlay(error_elements)
        return None


class geom_label(geom_text):
    """Text labels with background boxes
    
    Similar to geom_text but with background rectangles for better readability.
    
    Args:
        mapping: Aesthetic mappings (x, y, label, color, fill)  
        data: Data for this layer
        label_padding: Padding around text
        label_r: Corner radius of label box
        fill: Background fill color
        color: Text color
        **kwargs: Additional parameters inherited from geom_text
    """
    
    def __init__(self, mapping=None, data=None, label_padding=0.25, 
                 label_r=0.15, fill='white', color='black', **kwargs):
        super().__init__(mapping, data, color=color, **kwargs)
        self.params.update({
            'label_padding': label_padding,
            'label_r': label_r,
            'fill': fill
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render labels with background boxes"""
        # For now, use the same implementation as geom_text
        # A full implementation would add background rectangles
        return super()._render(data, combined_aes, ggplot_obj)


# Export all additional geoms
__all__ = [
    'geom_ribbon',
    'geom_violin',
    'geom_text',
    'geom_label',
    'geom_errorbar',
]