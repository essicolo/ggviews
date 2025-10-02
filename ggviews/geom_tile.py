"""
Tile and raster geoms for heatmaps and image data
"""

import pandas as pd
import numpy as np
import holoviews as hv
from .geoms import GeomLayer
import warnings

class geom_tile(GeomLayer):
    """Rectangles with specified positions and dimensions
    
    Creates heatmap-like visualizations using rectangles (tiles). Each tile
    represents a data point with x, y coordinates and can be colored by a
    third variable.
    
    Args:
        mapping: Aesthetic mappings (aes object)
        data: Data for this layer
        width: Tile width (default: auto-calculated)
        height: Tile height (default: auto-calculated) 
        **kwargs: Additional parameters
        
    Examples:
        # Basic heatmap
        geom_tile(aes(x='x_var', y='y_var', fill='z_var'))
        
        # Custom tile size
        geom_tile(aes(x='x', y='y', fill='value'), width=1, height=1)
    """
    
    def __init__(self, mapping=None, data=None, width=None, height=None, **kwargs):
        super().__init__(mapping, data, **kwargs)
        
        self.params.update({
            'width': width,
            'height': height,
            'alpha': kwargs.get('alpha', 1.0),
            'color': kwargs.get('color', 'white'),  # Border color
            'size': kwargs.get('size', 0.5)  # Border size
        })
    
    def _calculate_tile_dimensions(self, x_data, y_data):
        """Calculate default tile dimensions based on data"""
        
        # Calculate spacing between points
        x_unique = np.sort(np.unique(x_data))
        y_unique = np.sort(np.unique(y_data))
        
        # Default width/height based on spacing
        if len(x_unique) > 1:
            x_diff = np.diff(x_unique)
            default_width = np.min(x_diff[x_diff > 0])
        else:
            default_width = 1.0
            
        if len(y_unique) > 1:
            y_diff = np.diff(y_unique)
            default_height = np.min(y_diff[y_diff > 0])
        else:
            default_height = 1.0
            
        return default_width, default_height
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render the tiles"""
        
        # Get aesthetic mappings
        x_col = combined_aes.mappings.get('x')
        y_col = combined_aes.mappings.get('y')
        fill_col = combined_aes.mappings.get('fill')
        
        if not x_col or not y_col:
            raise ValueError("geom_tile requires x and y aesthetics")
        
        if x_col not in data.columns or y_col not in data.columns:
            raise ValueError(f"Columns '{x_col}' or '{y_col}' not found in data")
        
        x_data = data[x_col].values
        y_data = data[y_col].values
        
        # Calculate tile dimensions
        if self.params['width'] is None or self.params['height'] is None:
            default_width, default_height = self._calculate_tile_dimensions(x_data, y_data)
            tile_width = self.params['width'] or default_width
            tile_height = self.params['height'] or default_height
        else:
            tile_width = self.params['width']
            tile_height = self.params['height']
        
        # Handle fill colors
        if fill_col and fill_col in data.columns:
            fill_data = data[fill_col].values
            
            # Check if continuous or discrete
            if np.issubdtype(fill_data.dtype, np.number):
                # Continuous data - create color mapping
                vmin, vmax = np.nanmin(fill_data), np.nanmax(fill_data)
                
                # Create rectangles with color mapping
                rectangles_data = []
                
                for i in range(len(x_data)):
                    if pd.isna(fill_data[i]):
                        continue
                        
                    # Calculate rectangle bounds
                    left = x_data[i] - tile_width/2
                    bottom = y_data[i] - tile_height/2
                    right = x_data[i] + tile_width/2
                    top = y_data[i] + tile_height/2
                    
                    # Normalize color value
                    color_val = fill_data[i]
                    
                    rectangles_data.append((left, bottom, right, top, color_val))
                
                if rectangles_data:
                    # Convert to DataFrame for HeatMap
                    rect_df = pd.DataFrame(rectangles_data, 
                                         columns=['left', 'bottom', 'right', 'top', 'value'])
                    
                    # Create HeatMap using holoviews
                    pivot_data = data.pivot_table(
                        values=fill_col, 
                        index=y_col, 
                        columns=x_col, 
                        aggfunc='mean'
                    )
                    
                    heatmap = hv.HeatMap(pivot_data).opts(
                        cmap='viridis',
                        width=500,
                        height=400,
                        colorbar=True,
                        tools=['hover']
                    )
                    
                    return heatmap
                    
            else:
                # Discrete data - use discrete colors
                color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
                
                elements = []
                
                for category in data[fill_col].unique():
                    mask = data[fill_col] == category
                    cat_x = x_data[mask]
                    cat_y = y_data[mask]
                    
                    rectangles_data = []
                    for i in range(len(cat_x)):
                        left = cat_x[i] - tile_width/2
                        bottom = cat_y[i] - tile_height/2
                        right = cat_x[i] + tile_width/2
                        top = cat_y[i] + tile_height/2
                        
                        rectangles_data.append((left, bottom, right, top))
                    
                    if rectangles_data:
                        color = color_map.get(category, '#1f77b4')
                        rect_element = hv.Rectangles(rectangles_data).opts(
                            color=color,
                            alpha=self.params['alpha'],
                            line_color=self.params['color'],
                            line_width=self.params['size']
                        )
                        elements.append(rect_element)
                
                if elements:
                    return hv.Overlay(elements)
        
        else:
            # No fill mapping - single color
            rectangles_data = []
            
            for i in range(len(x_data)):
                left = x_data[i] - tile_width/2
                bottom = y_data[i] - tile_height/2
                right = x_data[i] + tile_width/2
                top = y_data[i] + tile_height/2
                
                rectangles_data.append((left, bottom, right, top))
            
            if rectangles_data:
                return hv.Rectangles(rectangles_data).opts(
                    color='lightblue',
                    alpha=self.params['alpha'],
                    line_color=self.params['color'],
                    line_width=self.params['size'],
                    width=500,
                    height=400
                )
        
        # Fallback empty plot
        return hv.Rectangles([]).opts(width=500, height=400)


class geom_raster(geom_tile):
    """High performance rectangular tiles for large datasets
    
    Similar to geom_tile but optimized for large regular grids.
    Better performance for image-like data.
    
    Args:
        mapping: Aesthetic mappings (aes object) 
        data: Data for this layer
        interpolate: Whether to interpolate between points
        **kwargs: Additional parameters
        
    Examples:
        # Large heatmap
        geom_raster(aes(x='x', y='y', fill='value'))
        
        # Image-like data
        geom_raster(aes(x='x', y='y', fill='intensity'), interpolate=True)
    """
    
    def __init__(self, mapping=None, data=None, interpolate=False, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params['interpolate'] = interpolate
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render the raster (optimized for regular grids)"""
        
        # Get aesthetic mappings
        x_col = combined_aes.mappings.get('x')
        y_col = combined_aes.mappings.get('y')
        fill_col = combined_aes.mappings.get('fill')
        
        if not x_col or not y_col or not fill_col:
            raise ValueError("geom_raster requires x, y, and fill aesthetics")
        
        if (x_col not in data.columns or y_col not in data.columns or 
            fill_col not in data.columns):
            raise ValueError("Required columns not found in data")
        
        try:
            # Try to create a proper raster using holoviews Image
            pivot_data = data.pivot_table(
                values=fill_col,
                index=y_col, 
                columns=x_col,
                aggfunc='mean'
            )
            
            # Create holoviews Image (raster)
            image = hv.Image(pivot_data).opts(
                cmap='viridis',
                width=500,
                height=400,
                colorbar=True,
                tools=['hover']
            )
            
            return image
            
        except Exception:
            # Fallback to tile rendering
            return super()._render(data, combined_aes, ggplot_obj)


# Export
__all__ = ['geom_tile', 'geom_raster']