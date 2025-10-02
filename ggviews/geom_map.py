"""
Geographic mapping functionality for ggviews

This module implements geom_map for creating geographic visualizations.
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List
from .geoms import GeomLayer
import warnings

try:
    # Try to import geoviews for advanced mapping
    import geoviews as gv
    import geoviews.feature as gf
    GEOVIEWS_AVAILABLE = True
except ImportError:
    GEOVIEWS_AVAILABLE = False

try:
    # Try to import cartopy for projections
    import cartopy.crs as ccrs
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False


class geom_map(GeomLayer):
    """Geographic map layer
    
    Creates geographic visualizations using points, polygons, or choropleth maps.
    Requires geoviews and cartopy for full functionality.
    
    Args:
        mapping: Aesthetic mappings (aes object)
        data: Data for this layer (should contain lat/lon or geometry)
        map_type: Type of map ('points', 'polygons', 'choropleth', 'world')
        projection: Map projection (default: PlateCarree)
        features: List of map features to add ('coastlines', 'borders', 'land', 'ocean')
        alpha: Transparency (0-1)
        color: Point/line color
        fill: Fill color for polygons
        size: Point size
        **kwargs: Additional parameters
        
    Examples:
        # World map with points
        geom_map(aes(x='longitude', y='latitude'), map_type='points')
        
        # Choropleth map
        geom_map(aes(fill='population'), map_type='choropleth')
        
        # Custom projection
        geom_map(map_type='world', projection='Mollweide')
    """
    
    def __init__(self, mapping=None, data=None, map_type='points', projection=None,
                 features=['coastlines'], alpha=0.7, color=None, fill=None, 
                 size=6, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.map_type = map_type
        self.projection = projection or 'PlateCarree'
        self.features = features
        
        self.params.update({
            'alpha': alpha,
            'color': color,
            'fill': fill,
            'size': size,
            'map_type': map_type,
            'projection': projection,
            'features': features
        })
    
    def _get_projection(self):
        """Get the cartopy projection"""
        if not CARTOPY_AVAILABLE:
            return None
            
        projection_map = {
            'PlateCarree': ccrs.PlateCarree(),
            'Mollweide': ccrs.Mollweide(),
            'Robinson': ccrs.Robinson(),
            'Orthographic': ccrs.Orthographic(),
            'Mercator': ccrs.Mercator(),
            'Miller': ccrs.Miller(),
        }
        
        return projection_map.get(self.projection, ccrs.PlateCarree())
    
    def _add_map_features(self, plot):
        """Add geographic features to the map"""
        if not GEOVIEWS_AVAILABLE:
            return plot
            
        feature_map = {
            'coastlines': gf.coastline,
            'borders': gf.borders,
            'land': gf.land,
            'ocean': gf.ocean,
            'rivers': gf.rivers,
            'lakes': gf.lakes
        }
        
        features = []
        for feature_name in self.features:
            if feature_name in feature_map:
                feature = feature_map[feature_name].opts(
                    line_color='gray',
                    line_width=0.5
                )
                features.append(feature)
        
        if features:
            return hv.Overlay([plot] + features)
        return plot
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render the geographic map"""
        
        # Check for required libraries
        if not GEOVIEWS_AVAILABLE and self.map_type != 'simple':
            warnings.warn("geoviews not available. Install with: pip install geoviews")
            return self._render_simple_map(data, combined_aes, ggplot_obj)
        
        if self.map_type == 'world':
            return self._render_world_map(data, combined_aes, ggplot_obj)
        elif self.map_type == 'points':
            return self._render_point_map(data, combined_aes, ggplot_obj)
        elif self.map_type == 'choropleth':
            return self._render_choropleth_map(data, combined_aes, ggplot_obj)
        else:
            return self._render_simple_map(data, combined_aes, ggplot_obj)
    
    def _render_simple_map(self, data, combined_aes, ggplot_obj):
        """Render a simple scatter plot as fallback"""
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            # Try common longitude/latitude column names
            lon_cols = ['longitude', 'lon', 'lng', 'x']
            lat_cols = ['latitude', 'lat', 'y']
            
            lon_col = None
            lat_col = None
            
            for col in lon_cols:
                if col in data.columns:
                    lon_col = col
                    break
            
            for col in lat_cols:
                if col in data.columns:
                    lat_col = col
                    break
            
            if not lon_col or not lat_col:
                raise ValueError("geom_map requires longitude/latitude data. Use aes(x='longitude', y='latitude') or ensure columns named 'longitude'/'latitude' exist.")
            
            # Create temporary aesthetics
            temp_aes = combined_aes
            temp_aes.mappings['x'] = lon_col
            temp_aes.mappings['y'] = lat_col
            combined_aes = temp_aes
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        x_data = data[x_col]
        y_data = data[y_col]
        
        # Handle color mapping
        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        
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
                    scatter = hv.Scatter(cat_data).opts(
                        color=color,
                        size=self.params['size'],
                        alpha=self.params['alpha'],
                        tools=['hover'],
                        xlabel='Longitude',
                        ylabel='Latitude'
                    )
                    plot_data.append(scatter)
            
            if plot_data:
                return hv.Overlay(plot_data)
        else:
            # Single color
            plot_data = pd.DataFrame({'x': x_data, 'y': y_data})
            color = self.params.get('color')
            if color is None:
                color = '#1f77b4'
            return hv.Scatter(plot_data).opts(
                color=color,
                size=self.params['size'],
                alpha=self.params['alpha'],
                tools=['hover'],
                xlabel='Longitude',
                ylabel='Latitude'
            )
    
    def _render_world_map(self, data, combined_aes, ggplot_obj):
        """Render a world map with optional data points"""
        if not GEOVIEWS_AVAILABLE:
            return self._render_simple_map(data, combined_aes, ggplot_obj)
        
        # Create base world map
        world_map = gf.coastline.opts(
            width=800, height=400,
            projection=self._get_projection() if CARTOPY_AVAILABLE else None
        )
        
        # Add features
        world_map = self._add_map_features(world_map)
        
        # If there's data, add it as points
        if data is not None and len(data) > 0:
            points_map = self._render_point_map(data, combined_aes, ggplot_obj)
            if points_map is not None:
                return world_map * points_map
        
        return world_map
    
    def _render_point_map(self, data, combined_aes, ggplot_obj):
        """Render points on a geographic map"""
        if not GEOVIEWS_AVAILABLE:
            return self._render_simple_map(data, combined_aes, ggplot_obj)
        
        # Determine coordinate columns
        x_col = combined_aes.mappings.get('x', 'longitude')
        y_col = combined_aes.mappings.get('y', 'latitude')
        
        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Coordinate columns not found: {x_col}, {y_col}")
            return None
        
        x_data = data[x_col]
        y_data = data[y_col]
        
        # Create geographic points
        points_data = pd.DataFrame({
            'longitude': x_data,
            'latitude': y_data
        })
        
        # Handle color mapping
        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        
        if color_map and 'color' in combined_aes.mappings:
            color_col = combined_aes.mappings['color']
            plot_data = []
            for category, color in color_map.items():
                mask = data[color_col] == category
                if mask.any():
                    cat_data = pd.DataFrame({
                        'longitude': x_data[mask],
                        'latitude': y_data[mask]
                    })
                    points = gv.Points(cat_data).opts(
                        color=color,
                        size=self.params['size'],
                        alpha=self.params['alpha'],
                        tools=['hover'],
                        projection=self._get_projection() if CARTOPY_AVAILABLE else None
                    )
                    plot_data.append(points)
            
            if plot_data:
                base_map = gf.coastline.opts(projection=self._get_projection() if CARTOPY_AVAILABLE else None)
                return base_map * hv.Overlay(plot_data)
        else:
            color = self.params.get('color', '#1f77b4')
            points = gv.Points(points_data).opts(
                color=color,
                size=self.params['size'],
                alpha=self.params['alpha'],
                tools=['hover'],
                projection=self._get_projection() if CARTOPY_AVAILABLE else None
            )
            
            base_map = gf.coastline.opts(projection=self._get_projection() if CARTOPY_AVAILABLE else None)
            return base_map * points
    
    def _render_choropleth_map(self, data, combined_aes, ggplot_obj):
        """Render a choropleth (filled region) map"""
        # This would require shape data - placeholder for now
        warnings.warn("Choropleth maps require additional shape data. Using point map as fallback.")
        return self._render_point_map(data, combined_aes, ggplot_obj)


# Export the geom
__all__ = ['geom_map']