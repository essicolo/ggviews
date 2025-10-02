"""
Geometric objects (geoms) for ggviews

This module contains all the geom classes that represent different
ways of displaying data (points, lines, bars, etc.)
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List
from .core import aes
import warnings


class GeomLayer:
    """Base class for all geom layers"""
    
    def __init__(self, mapping=None, data=None, stat='identity', position='identity', **kwargs):
        self.mapping = mapping
        self.data = data
        self.stat = stat  # Statistical transformation
        self.position = position  # Position adjustment
        self.params = kwargs  # Additional parameters (color, size, alpha, etc.)
        self.geom_type = self.__class__.__name__.lower().replace('geom_', '')
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this geom to a ggplot object"""
        new_plot = ggplot_obj._copy()
        new_plot.layers.append(self)
        return new_plot
    
    def _get_aesthetic_value(self, aes_name, combined_aes, data, default_value):
        """Get aesthetic value - either mapped from data or constant"""
        if aes_name in combined_aes.mappings:
            col_name = combined_aes.mappings[aes_name]
            if col_name in data.columns:
                return data[col_name]
            else:
                available_cols = list(data.columns)
                # Check for case-sensitive matches
                case_matches = [col for col in available_cols if col.lower() == col_name.lower()]
                if case_matches:
                    print(f"⚠️  WARNING: Column '{col_name}' not found. Did you mean '{case_matches[0]}'?")
                    print(f"   Available columns: {available_cols}")
                else:
                    print(f"⚠️  WARNING: Column '{col_name}' not found in data for aesthetic '{aes_name}'")
                    print(f"   Available columns: {available_cols}")
                return default_value
        elif aes_name in self.params:
            return self.params[aes_name]
        else:
            return default_value
    
    def _get_color_mapping(self, combined_aes, data, ggplot_obj):
        """Get color mapping for the data"""
        if 'color' in combined_aes.mappings:
            color_col = combined_aes.mappings['color']
            if color_col in data.columns:
                # Check if viridis or other scale mapping exists first
                if hasattr(ggplot_obj, 'viridis_discrete_map') and ggplot_obj.viridis_discrete_map:
                    return ggplot_obj.viridis_discrete_map
                elif hasattr(ggplot_obj, 'viridis_color_map') and ggplot_obj.viridis_color_map:
                    return ggplot_obj.viridis_color_map
                elif hasattr(ggplot_obj, 'brewer_discrete_map') and ggplot_obj.brewer_discrete_map:
                    return ggplot_obj.brewer_discrete_map
                else:
                    # Use default colors if no scale is applied
                    unique_vals = data[color_col].unique()
                    n_colors = len(unique_vals)
                    colors = ggplot_obj.default_colors[:n_colors] if n_colors <= len(ggplot_obj.default_colors) else ggplot_obj.default_colors * ((n_colors // len(ggplot_obj.default_colors)) + 1)
                    return dict(zip(unique_vals, colors[:n_colors]))
            else:
                # Column not found - provide helpful error message  
                available_cols = list(data.columns)
                case_matches = [col for col in available_cols if col.lower() == color_col.lower()]
                if case_matches:
                    print(f"🔴 ERROR: Color mapping failed! Column '{color_col}' not found.")
                    print(f"   💡 Did you mean '{case_matches[0]}'? (Note the different capitalization)")
                    print(f"   Available columns: {available_cols}")
                else:
                    print(f"🔴 ERROR: Color mapping failed! Column '{color_col}' not found.")
                    print(f"   Available columns: {available_cols}")
        return {}
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render this geom - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement _render method")


class geom_point(GeomLayer):
    """Scatter plot points
    
    Args:
        mapping: Aesthetic mappings (aes object)
        data: Data for this layer (overrides ggplot data)
        size: Point size
        alpha: Transparency (0-1)
        color: Point color  
        shape: Point shape
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, size=6, alpha=1.0, color=None, shape='circle', **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'size': size,
            'alpha': alpha, 
            'color': color,
            'shape': shape
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("geom_point requires both x and y aesthetics")
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Required columns not found: {x_col}, {y_col}")
            return None
        
        x_data = data[x_col]
        y_data = data[y_col]
        
        # Handle color mapping
        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        
        # Handle size mapping
        size_col = combined_aes.mappings.get('size')
        size_data = None
        if size_col and size_col in data.columns:
            size_data = data[size_col]
        
        if color_map and 'color' in combined_aes.mappings:
            color_col = combined_aes.mappings['color']
            plot_data = []
            for category, color in color_map.items():
                mask = data[color_col] == category
                if mask.any():
                    cat_data = pd.DataFrame({
                        'x': x_data[mask],
                        'y': y_data[mask]
                    })
                    
                    # Handle size mapping for this category
                    if size_data is not None:
                        # Scale size data to reasonable range (5-25 pixels)
                        cat_sizes = size_data[mask]
                        size_min, size_max = cat_sizes.min(), cat_sizes.max()
                        if size_max > size_min:
                            # Normalize to 5-25 range
                            normalized_sizes = 5 + 20 * (cat_sizes - size_min) / (size_max - size_min)
                        else:
                            normalized_sizes = pd.Series([self.params['size']] * len(cat_sizes))
                        cat_data['size'] = normalized_sizes
                        
                        # Create scatter with size mapping
                        scatter = hv.Scatter(cat_data, vdims=['size'], label=str(category)).opts(
                            color=color,
                            size='size',
                            alpha=self.params['alpha'],
                            tools=['hover'],
                            show_legend=True
                        )
                    else:
                        # Create scatter with proper label for legend
                        scatter = hv.Scatter(cat_data, label=str(category)).opts(
                            color=color,
                            size=self.params['size'],
                            alpha=self.params['alpha'],
                            tools=['hover'],
                            show_legend=True
                        )
                    
                    plot_data.append(scatter)
            
            if plot_data:
                # Create overlay with legend
                overlay = hv.Overlay(plot_data).opts(
                    legend_position='right',
                    show_legend=True
                )
                return overlay
            
        else:
            # Single color (no color mapping)
            plot_data = pd.DataFrame({'x': x_data, 'y': y_data})
            
            # Handle size mapping for single color case
            if size_data is not None:
                # Scale size data to reasonable range (5-25 pixels)
                size_min, size_max = size_data.min(), size_data.max()
                if size_max > size_min:
                    # Normalize to 5-25 range
                    normalized_sizes = 5 + 20 * (size_data - size_min) / (size_max - size_min)
                else:
                    normalized_sizes = pd.Series([self.params['size']] * len(size_data))
                plot_data['size'] = normalized_sizes
                
                color = self.params.get('color')
                if color is None:
                    color = '#1f77b4'  # Default blue color
                
                return hv.Scatter(plot_data, vdims=['size']).opts(
                    color=color,
                    size='size',
                    alpha=self.params['alpha'],
                    tools=['hover']
                )
            else:
                # No size mapping
                color = self.params.get('color')
                if color is None:
                    color = '#1f77b4'  # Default blue color
                return hv.Scatter(plot_data).opts(
                    color=color,
                    size=self.params['size'],
                    alpha=self.params['alpha'],
                    tools=['hover']
                )


class geom_line(GeomLayer):
    """Line plots
    
    Args:
        mapping: Aesthetic mappings
        data: Data for this layer
        color: Line color
        size: Line width
        alpha: Transparency
        linetype: Line type ('solid', 'dashed', 'dotted')
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, color=None, size=2, alpha=1.0, linetype='solid', **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'color': color,
            'size': size,
            'alpha': alpha,
            'linetype': linetype
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("geom_line requires both x and y aesthetics")
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Required columns not found: {x_col}, {y_col}")
            return None
        
        # Sort by x for proper line plotting
        data_sorted = data.sort_values(x_col)
        x_data = data_sorted[x_col]
        y_data = data_sorted[y_col]
        
        # Handle color mapping
        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        
        if color_map and 'color' in combined_aes.mappings:
            color_col = combined_aes.mappings['color']
            plot_data = []
            for category, color in color_map.items():
                mask = data_sorted[color_col] == category
                if mask.any():
                    cat_data = pd.DataFrame({
                        'x': x_data[mask],
                        'y': y_data[mask]
                    }).sort_values('x')
                    curve = hv.Curve(cat_data).opts(
                        color=color,
                        line_width=self.params['size'],
                        alpha=self.params['alpha']
                    )
                    plot_data.append(curve)
            
            if plot_data:
                return hv.Overlay(plot_data)
                
        else:
            # Single color  
            plot_data = pd.DataFrame({'x': x_data, 'y': y_data})
            color = self.params.get('color', '#1f77b4')
            return hv.Curve(plot_data).opts(
                color=color,
                line_width=self.params['size'],
                alpha=self.params['alpha']
            )


class geom_bar(GeomLayer):
    """Bar charts
    
    Args:
        mapping: Aesthetic mappings
        data: Data for this layer
        stat: Statistical transformation ('count' or 'identity')
        color: Bar border color
        fill: Bar fill color
        alpha: Transparency
        width: Bar width
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, stat='count', color=None, fill=None, alpha=1.0, width=0.8, **kwargs):
        super().__init__(mapping, data, stat=stat, **kwargs)
        self.params.update({
            'color': color,
            'fill': fill,
            'alpha': alpha,
            'width': width
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        if 'x' not in combined_aes.mappings:
            raise ValueError("geom_bar requires x aesthetic")
        
        x_col = combined_aes.mappings['x']
        
        if x_col not in data.columns:
            warnings.warn(f"Column '{x_col}' not found in data")
            return None
        
        if self.stat == 'count':
            # Count occurrences
            counts = data[x_col].value_counts().sort_index()
            plot_data = pd.DataFrame({
                'x': counts.index,
                'y': counts.values
            })
        else:
            # Use y values directly
            if 'y' not in combined_aes.mappings:
                raise ValueError("geom_bar with stat='identity' requires y aesthetic")
            
            y_col = combined_aes.mappings['y']
            if y_col not in data.columns:
                warnings.warn(f"Column '{y_col}' not found in data")
                return None
            
            plot_data = data.groupby(x_col)[y_col].sum().reset_index()
            plot_data.columns = ['x', 'y']
        
        color = self.params.get('fill') or self.params.get('color') or '#1f77b4'
        
        return hv.Bars(plot_data).opts(
            color=color,
            alpha=self.params['alpha'],
            tools=['hover']
        )


class geom_histogram(GeomLayer):
    """Histograms
    
    Args:
        mapping: Aesthetic mappings
        data: Data for this layer
        bins: Number of bins or bin edges
        alpha: Transparency
        fill: Fill color
        color: Border color
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, bins=30, alpha=1.0, fill=None, color=None, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'bins': bins,
            'alpha': alpha,
            'fill': fill,
            'color': color
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        if 'x' not in combined_aes.mappings:
            raise ValueError("geom_histogram requires x aesthetic")
        
        x_col = combined_aes.mappings['x']
        
        if x_col not in data.columns:
            warnings.warn(f"Column '{x_col}' not found in data")
            return None
        
        x_data = data[x_col].dropna()
        
        color = self.params.get('fill') or self.params.get('color') or '#1f77b4'
        
        return hv.Histogram(np.histogram(x_data, bins=self.params['bins'])).opts(
            color=color,
            alpha=self.params['alpha'],
            tools=['hover']
        )


class geom_smooth(GeomLayer):
    """Smoothed conditional means
    
    Args:
        mapping: Aesthetic mappings
        data: Data for this layer
        method: Smoothing method ('lm' for linear, 'loess' for local regression)
        se: Show confidence interval
        color: Line color
        fill: Confidence band color
        alpha: Transparency
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, method='loess', se=True, color=None, fill=None, alpha=1.0, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'method': method,
            'se': se,
            'color': color,
            'fill': fill,
            'alpha': alpha
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("geom_smooth requires both x and y aesthetics")
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Required columns not found: {x_col}, {y_col}")
            return None
        
        # Remove NaN values
        clean_data = data[[x_col, y_col]].dropna()
        
        if len(clean_data) < 2:
            warnings.warn("Not enough data points for smoothing")
            return None
        
        x_data = clean_data[x_col]
        y_data = clean_data[y_col]
        
        color = self.params.get('color', '#1f77b4')
        
        if self.params['method'] == 'lm':
            # Linear regression
            coeffs = np.polyfit(x_data, y_data, 1)
            x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
            y_smooth = np.polyval(coeffs, x_smooth)
            
            smooth_data = pd.DataFrame({'x': x_smooth, 'y': y_smooth})
            return hv.Curve(smooth_data).opts(
                color=color,
                alpha=self.params['alpha'],
                line_width=2
            )
        else:
            # Simple smoothing (moving average approximation)
            sorted_data = clean_data.sort_values(x_col)
            
            # Use rolling mean for smoothing
            window_size = max(1, len(sorted_data) // 10)
            smoothed = sorted_data.rolling(window=window_size, center=True).mean().dropna()
            
            return hv.Curve(smoothed[[x_col, y_col]].rename(columns={x_col: 'x', y_col: 'y'})).opts(
                color=color,
                alpha=self.params['alpha'],
                line_width=2
            )


class geom_boxplot(GeomLayer):
    """Box plots
    
    Args:
        mapping: Aesthetic mappings  
        data: Data for this layer
        alpha: Transparency
        fill: Fill color
        color: Border color
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, alpha=1.0, fill=None, color=None, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'alpha': alpha,
            'fill': fill,
            'color': color
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("geom_boxplot requires both x and y aesthetics")
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Required columns not found: {x_col}, {y_col}")
            return None
        
        # Group data by x variable
        grouped = data.groupby(x_col)[y_col]
        
        boxplot_data = []
        for name, group in grouped:
            values = group.dropna()
            if len(values) > 0:
                boxplot_data.append((name, values.tolist()))
        
        if not boxplot_data:
            return None
        
        color = self.params.get('fill') or self.params.get('color') or '#1f77b4'
        
        return hv.BoxWhisker(boxplot_data).opts(
            box_color=color,
            alpha=self.params['alpha'],
            tools=['hover']
        )


class geom_density(GeomLayer):
    """Density plots
    
    Args:
        mapping: Aesthetic mappings
        data: Data for this layer  
        alpha: Transparency
        fill: Fill color
        color: Line color
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, alpha=0.5, fill=None, color=None, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'alpha': alpha,
            'fill': fill,
            'color': color
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Apply density plots"""
        if 'x' not in combined_aes.mappings:
            raise ValueError("geom_density requires x aesthetic")
        
        x_col = combined_aes.mappings['x']
        
        if x_col not in data.columns:
            warnings.warn(f"Column '{x_col}' not found in data")
            return None
        
        x_data = data[x_col].dropna()
        
        if len(x_data) == 0:
            return None
        
        # Simple kernel density estimation using histogram
        hist, edges = np.histogram(x_data, bins=50, density=True)
        centers = (edges[:-1] + edges[1:]) / 2
        
        density_data = pd.DataFrame({'x': centers, 'y': hist})
        
        color = self.params.get('color', '#1f77b4')
        
        return hv.Area(density_data).opts(
            color=color,
            alpha=self.params['alpha'],
            tools=['hover']
        )


class geom_area(GeomLayer):
    """Area plots
    
    Draws an area plot where the area under the curve is filled.
    Useful for showing cumulative values or stacked areas.
    
    Args:
        mapping: Aesthetic mappings (x, y, fill, color, group, alpha)
        data: Data for this layer
        stat: Statistical transformation ('identity' or 'count')
        position: Position adjustment ('identity', 'stack', 'fill')
        alpha: Transparency (0-1)
        fill: Fill color
        color: Outline color
        size: Outline width
        **kwargs: Additional parameters
        
    Examples:
        geom_area(aes(x='year', y='value'))
        geom_area(aes(x='year', y='value', fill='category'))
        geom_area(position='stack')  # Stacked areas
    """
    
    def __init__(self, mapping=None, data=None, stat='identity', position='identity',
                 alpha=0.7, fill=None, color=None, size=1, **kwargs):
        super().__init__(mapping, data, stat=stat, position=position, **kwargs)
        self.params.update({
            'alpha': alpha,
            'fill': fill,
            'color': color,
            'size': size
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render area plot"""
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("geom_area requires both x and y aesthetics")
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Required columns not found: {x_col}, {y_col}")
            return None
        
        # Sort by x for proper area plotting
        data_sorted = data.sort_values(x_col)
        x_data = data_sorted[x_col]
        y_data = data_sorted[y_col]
        
        # Handle grouping/fill aesthetic
        if 'fill' in combined_aes.mappings or 'group' in combined_aes.mappings:
            group_col = combined_aes.mappings.get('fill') or combined_aes.mappings.get('group')
            
            if group_col and group_col in data.columns:
                # Create separate areas for each group
                plot_data = []
                color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
                
                if not color_map and 'fill' in combined_aes.mappings:
                    # Generate colors for unique groups
                    unique_groups = sorted(data[group_col].unique())
                    colors = ggplot_obj.default_colors[:len(unique_groups)]
                    color_map = dict(zip(unique_groups, colors))
                
                for group_val in data_sorted[group_col].unique():
                    group_mask = data_sorted[group_col] == group_val
                    if group_mask.any():
                        group_data = data_sorted[group_mask].copy()
                        
                        # Create area data (x, y pairs)
                        area_data = pd.DataFrame({
                            'x': group_data[x_col],
                            'y': group_data[y_col]
                        }).sort_values('x')
                        
                        # Get color for this group
                        if color_map and group_val in color_map:
                            area_color = color_map[group_val]
                        else:
                            area_color = self.params.get('fill') or ggplot_obj.default_colors[0]
                        
                        area_plot = hv.Area(area_data).opts(
                            color=area_color,
                            alpha=self.params['alpha'],
                            tools=['hover']
                        )
                        
                        plot_data.append(area_plot)
                
                if plot_data:
                    return hv.Overlay(plot_data)
            
        else:
            # Single area
            area_data = pd.DataFrame({
                'x': x_data,
                'y': y_data
            })
            
            area_color = self.params.get('fill') or self.params.get('color') or ggplot_obj.default_colors[0]
            
            return hv.Area(area_data).opts(
                color=area_color,
                alpha=self.params['alpha'],
                tools=['hover']
            )
        
        return None


# Export all geom classes
__all__ = [
    'GeomLayer',
    'geom_point', 
    'geom_line',
    'geom_bar',
    'geom_histogram',
    'geom_smooth',
    'geom_boxplot',
    'geom_density',
    'geom_area',
]