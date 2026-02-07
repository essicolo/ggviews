"""
Geographic mapping functionality for ggviews

Supports three rendering tiers, depending on available packages:

Tier 1 (geoviews + cartopy):  Full map projections, coastlines, borders.
Tier 2 (geopandas + shapely): Choropleth, world outlines, point maps using
                                HoloViews Polygons.  No projection support.
Tier 3 (bare holoviews):       Scatter plot with lon/lat as x/y.  Always works.

Key map types
-------------
simple      Scatter of lon/lat.  Always available.
points      Points overlaid on coastlines (tier 1) or world outline (tier 2).
world       World outline map with optional data points.
choropleth  Regions filled by a data variable.  Requires a GeoDataFrame
            (parameter ``geometry``).
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List
from .geoms import GeomLayer
import warnings

# ---------------------------------------------------------------------------
# Optional dependency detection
# ---------------------------------------------------------------------------

try:
    import geoviews as gv
    import geoviews.feature as gf
    GEOVIEWS_AVAILABLE = True
except ImportError:
    GEOVIEWS_AVAILABLE = False

try:
    import cartopy.crs as ccrs
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False

try:
    import geopandas as gpd
    from shapely.geometry import Polygon, MultiPolygon
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Built-in minimal world outline (approximate continent boundaries)
# ---------------------------------------------------------------------------

def _builtin_world_outline():
    """Return an hv.Path element with a rough world coastline.

    This is a very simplified approximation so that ``map_type='world'``
    can render *something* even without geoviews/cartopy or network access.
    The coordinates are (longitude, latitude) in EPSG:4326.
    """
    # Simplified continent outlines (rough bounding paths)
    continents = {
        'North America': [
            (-170, 65), (-168, 72), (-141, 70), (-130, 72), (-120, 75),
            (-85, 75), (-65, 82), (-60, 75), (-55, 52), (-65, 45),
            (-75, 35), (-80, 25), (-97, 18), (-105, 20), (-118, 33),
            (-125, 48), (-140, 60), (-165, 62), (-170, 65),
        ],
        'South America': [
            (-80, 10), (-65, 12), (-55, 5), (-35, -5), (-37, -12),
            (-38, -18), (-42, -23), (-48, -28), (-53, -33),
            (-58, -38), (-65, -42), (-68, -55), (-75, -50),
            (-72, -42), (-70, -30), (-70, -18), (-75, -10),
            (-77, 0), (-80, 5), (-80, 10),
        ],
        'Europe': [
            (-10, 36), (-8, 44), (-5, 48), (2, 51), (5, 53), (10, 55),
            (13, 55), (18, 58), (24, 60), (30, 62), (32, 70),
            (25, 71), (18, 70), (12, 65), (5, 62), (-5, 58),
            (-10, 52), (-10, 36),
        ],
        'Africa': [
            (-17, 15), (-15, 28), (-5, 36), (10, 37), (12, 33),
            (25, 32), (33, 30), (35, 20), (43, 12), (51, 12),
            (48, 5), (42, -2), (40, -10), (35, -22), (28, -33),
            (18, -35), (15, -28), (12, -18), (10, -5), (5, 5),
            (-5, 5), (-10, 8), (-17, 15),
        ],
        'Asia': [
            (28, 42), (30, 62), (40, 65), (50, 55), (60, 55),
            (68, 55), (80, 50), (90, 48), (100, 40), (105, 22),
            (110, 20), (115, 23), (120, 30), (125, 38), (130, 42),
            (135, 35), (140, 42), (145, 50), (155, 58), (170, 62),
            (175, 65), (180, 67), (180, 72), (170, 72), (145, 72),
            (120, 73), (80, 72), (65, 68), (50, 68), (40, 65),
            (28, 42),
        ],
        'Oceania': [
            (115, -15), (120, -18), (130, -13), (137, -12),
            (142, -10), (146, -18), (150, -23), (154, -28),
            (153, -32), (148, -37), (140, -38), (130, -32),
            (120, -22), (115, -15),
        ],
        'Antarctica': [
            (-180, -70), (-120, -72), (-60, -72), (0, -72),
            (60, -72), (120, -72), (180, -70),
        ],
    }
    paths = []
    for coords in continents.values():
        xs, ys = zip(*coords)
        paths.append({'x': list(xs), 'y': list(ys)})
    return hv.Path(paths).opts(color='gray', line_width=0.8)


# ---------------------------------------------------------------------------
# Utility: convert shapely geometry to HoloViews Polygons
# ---------------------------------------------------------------------------

def _geometry_to_hv_polygons(geom, **opts):
    """Convert a shapely geometry (Polygon or MultiPolygon) into a list of
    ``hv.Polygons`` elements with the given opts applied.
    """
    polys = []
    if geom is None or geom.is_empty:
        return polys

    if geom.geom_type == 'Polygon':
        parts = [geom]
    elif geom.geom_type == 'MultiPolygon':
        parts = list(geom.geoms)
    else:
        return polys

    for part in parts:
        xs, ys = part.exterior.coords.xy
        poly = hv.Polygons([{'x': list(xs), 'y': list(ys)}])
        if opts:
            poly = poly.opts(**opts)
        polys.append(poly)
    return polys


# ---------------------------------------------------------------------------
# geom_map
# ---------------------------------------------------------------------------

class geom_map(GeomLayer):
    """Geographic map layer

    Creates geographic visualizations using points, outlines, or
    choropleth fills.

    Parameters
    ----------
    mapping : aes, optional
        Aesthetic mappings.  ``x``/``y`` are interpreted as longitude/
        latitude.  ``fill`` or ``color`` can map to a data variable for
        choropleth coloring.
    data : DataFrame, optional
        Data for this layer.
    map_type : str
        ``'simple'``  -- scatter plot of lon/lat (always works).
        ``'points'``  -- points on a world outline.
        ``'world'``   -- world outline only (no data required).
        ``'choropleth'`` -- filled polygons colored by a variable.
    geometry : GeoDataFrame or str, optional
        Boundary data for choropleth.  Can be a ``GeoDataFrame`` or
        a file path / URL loadable by ``geopandas.read_file``.
    merge_on : str, optional
        Column used to join ``data`` with ``geometry``.  Required for
        choropleth when ``data`` and ``geometry`` are separate.
    projection : str
        Map projection name (requires cartopy).
    features : list of str
        Geographic features to overlay (requires geoviews).
    alpha, color, fill, size : various
        Visual parameters forwarded to HoloViews opts.

    Examples
    --------
    >>> geom_map(aes(x='lon', y='lat'), map_type='points')
    >>> geom_map(aes(fill='pop'), map_type='choropleth',
    ...          geometry=world_gdf, merge_on='name')
    """

    def __init__(self, mapping=None, data=None, map_type='points',
                 geometry=None, merge_on=None,
                 projection=None, features=None,
                 alpha=0.7, color=None, fill=None, size=6, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.map_type = map_type
        self.geometry = geometry
        self.merge_on = merge_on
        self.projection = projection or 'PlateCarree'
        self.features = features if features is not None else ['coastlines']

        self.params.update({
            'alpha': alpha,
            'color': color,
            'fill': fill,
            'size': size,
            'map_type': map_type,
        })

    # ------------------------------------------------------------------
    # projection helpers
    # ------------------------------------------------------------------

    def _get_projection(self):
        if not CARTOPY_AVAILABLE:
            return None
        proj_map = {
            'PlateCarree': ccrs.PlateCarree(),
            'Mollweide': ccrs.Mollweide(),
            'Robinson': ccrs.Robinson(),
            'Orthographic': ccrs.Orthographic(),
            'Mercator': ccrs.Mercator(),
            'Miller': ccrs.Miller(),
        }
        return proj_map.get(self.projection, ccrs.PlateCarree())

    # ------------------------------------------------------------------
    # coordinate auto-detection
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_lonlat(data, combined_aes):
        """Return (lon_col, lat_col) by inspecting aes mappings or column names."""
        lon_col = combined_aes.mappings.get('x')
        lat_col = combined_aes.mappings.get('y')

        if lon_col and lon_col in data.columns and lat_col and lat_col in data.columns:
            return lon_col, lat_col

        for candidate in ['longitude', 'lon', 'lng', 'x', 'long']:
            if candidate in data.columns:
                lon_col = candidate
                break
        for candidate in ['latitude', 'lat', 'y']:
            if candidate in data.columns:
                lat_col = candidate
                break

        if lon_col and lat_col and lon_col in data.columns and lat_col in data.columns:
            return lon_col, lat_col
        return None, None

    # ------------------------------------------------------------------
    # rendering dispatch
    # ------------------------------------------------------------------

    def _render(self, data, combined_aes, ggplot_obj):
        if self.map_type == 'choropleth':
            return self._render_choropleth(data, combined_aes, ggplot_obj)
        if self.map_type == 'world':
            return self._render_world(data, combined_aes, ggplot_obj)
        if self.map_type == 'points':
            return self._render_points(data, combined_aes, ggplot_obj)
        return self._render_simple(data, combined_aes, ggplot_obj)

    # ------------------------------------------------------------------
    # simple scatter (always works)
    # ------------------------------------------------------------------

    def _render_simple(self, data, combined_aes, ggplot_obj):
        lon_col, lat_col = self._detect_lonlat(data, combined_aes)
        if lon_col is None or lat_col is None:
            raise ValueError(
                "geom_map requires lon/lat data.  Use aes(x='lon', y='lat') "
                "or ensure columns named 'longitude'/'latitude' exist."
            )

        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        base_color = self.params.get('color') or '#1f77b4'

        if color_map and 'color' in combined_aes.mappings:
            color_col = combined_aes.mappings['color']
            layers = []
            for cat, clr in color_map.items():
                mask = data[color_col] == cat
                if mask.any():
                    cat_df = pd.DataFrame({'x': data.loc[mask, lon_col].values,
                                           'y': data.loc[mask, lat_col].values})
                    layers.append(
                        hv.Scatter(cat_df).opts(
                            color=clr, size=self.params['size'],
                            alpha=self.params['alpha'], tools=['hover'],
                            xlabel='Longitude', ylabel='Latitude',
                        )
                    )
            if layers:
                return hv.Overlay(layers)
        else:
            plot_df = pd.DataFrame({'x': data[lon_col].values,
                                    'y': data[lat_col].values})
            return hv.Scatter(plot_df).opts(
                color=base_color, size=self.params['size'],
                alpha=self.params['alpha'], tools=['hover'],
                xlabel='Longitude', ylabel='Latitude',
            )

    # ------------------------------------------------------------------
    # world outline
    # ------------------------------------------------------------------

    def _render_world(self, data, combined_aes, ggplot_obj):
        # Tier 1: geoviews
        if GEOVIEWS_AVAILABLE:
            proj = self._get_projection() if CARTOPY_AVAILABLE else None
            world = gf.coastline.opts(width=800, height=400,
                                      projection=proj)
            if data is not None and len(data) > 0:
                pts = self._render_points(data, combined_aes, ggplot_obj)
                if pts is not None:
                    return world * pts
            return world

        # Tier 2: built-in outline
        outline = _builtin_world_outline().opts(
            width=800, height=400,
            xlabel='Longitude', ylabel='Latitude',
        )
        if data is not None and len(data) > 0:
            pts = self._render_simple(data, combined_aes, ggplot_obj)
            if pts is not None:
                return outline * pts
        return outline

    # ------------------------------------------------------------------
    # point map (points on world outline)
    # ------------------------------------------------------------------

    def _render_points(self, data, combined_aes, ggplot_obj):
        if GEOVIEWS_AVAILABLE:
            return self._render_points_geoviews(data, combined_aes, ggplot_obj)

        # Tier 2 fallback: world outline + scatter
        outline = _builtin_world_outline()
        pts = self._render_simple(data, combined_aes, ggplot_obj)
        if pts is not None:
            return (outline * pts).opts(
                width=800, height=400,
                xlabel='Longitude', ylabel='Latitude',
            )
        return outline.opts(width=800, height=400)

    def _render_points_geoviews(self, data, combined_aes, ggplot_obj):
        lon_col, lat_col = self._detect_lonlat(data, combined_aes)
        if lon_col is None or lat_col is None:
            return self._render_simple(data, combined_aes, ggplot_obj)

        proj = self._get_projection() if CARTOPY_AVAILABLE else None
        base_map = gf.coastline.opts(projection=proj)

        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        if color_map and 'color' in combined_aes.mappings:
            color_col = combined_aes.mappings['color']
            layers = []
            for cat, clr in color_map.items():
                mask = data[color_col] == cat
                if mask.any():
                    pts_df = pd.DataFrame({
                        'longitude': data.loc[mask, lon_col].values,
                        'latitude': data.loc[mask, lat_col].values,
                    })
                    layers.append(gv.Points(pts_df).opts(
                        color=clr, size=self.params['size'],
                        alpha=self.params['alpha'], tools=['hover'],
                        projection=proj,
                    ))
            if layers:
                return base_map * hv.Overlay(layers)
        else:
            pts_df = pd.DataFrame({
                'longitude': data[lon_col].values,
                'latitude': data[lat_col].values,
            })
            clr = self.params.get('color') or '#1f77b4'
            points = gv.Points(pts_df).opts(
                color=clr, size=self.params['size'],
                alpha=self.params['alpha'], tools=['hover'],
                projection=proj,
            )
            return base_map * points

    # ------------------------------------------------------------------
    # choropleth
    # ------------------------------------------------------------------

    def _render_choropleth(self, data, combined_aes, ggplot_obj):
        """Render a choropleth map.

        Requires ``geometry`` (a GeoDataFrame or file path).  The ``fill``
        aesthetic (or ``color``) maps a data variable to polygon fill colour.
        If ``data`` is separate from the geometry, use ``merge_on`` to join.
        """
        if not GEOPANDAS_AVAILABLE:
            warnings.warn(
                "Choropleth maps require geopandas.  "
                "Install with: pip install geopandas"
            )
            return self._render_simple(data, combined_aes, ggplot_obj)

        # Resolve geometry source
        gdf = self._resolve_geometry(data)
        if gdf is None:
            warnings.warn("No geometry data available for choropleth.")
            return self._render_simple(data, combined_aes, ggplot_obj)

        # Determine fill variable
        fill_col = (combined_aes.mappings.get('fill')
                    or combined_aes.mappings.get('color')
                    or self.params.get('fill'))

        if fill_col and fill_col in gdf.columns:
            return self._render_choropleth_filled(gdf, fill_col, ggplot_obj)
        else:
            # No fill variable -> just draw outlines
            return self._render_choropleth_outline(gdf, ggplot_obj)

    def _resolve_geometry(self, data):
        """Return a GeoDataFrame ready for rendering."""
        geo = self.geometry

        if geo is None:
            # Check if data itself is a GeoDataFrame
            if GEOPANDAS_AVAILABLE and isinstance(data, gpd.GeoDataFrame):
                return data
            warnings.warn(
                "Choropleth requires a geometry parameter (GeoDataFrame or "
                "file path).  Example: geom_map(geometry=gdf, ...)"
            )
            return None

        # If it's already a GeoDataFrame, optionally merge with data
        if isinstance(geo, gpd.GeoDataFrame):
            gdf = geo
        elif isinstance(geo, str):
            # Treat as file path / URL
            try:
                gdf = gpd.read_file(geo)
            except Exception as exc:
                warnings.warn(f"Could not read geometry file: {exc}")
                return None
        else:
            warnings.warn("geometry must be a GeoDataFrame or file path.")
            return None

        # Merge user data onto geometry if merge_on is provided
        if self.merge_on and self.merge_on in gdf.columns:
            if isinstance(data, pd.DataFrame) and self.merge_on in data.columns:
                # Drop geometry-conflicting columns from data before merge
                data_cols = [c for c in data.columns if c != 'geometry']
                gdf = gdf.merge(data[data_cols], on=self.merge_on, how='left')

        return gdf

    def _render_choropleth_filled(self, gdf, fill_col, ggplot_obj):
        """Render filled polygons coloured by *fill_col*."""
        is_numeric = pd.api.types.is_numeric_dtype(gdf[fill_col])

        if is_numeric:
            return self._render_choropleth_continuous(gdf, fill_col, ggplot_obj)
        else:
            return self._render_choropleth_categorical(gdf, fill_col, ggplot_obj)

    def _render_choropleth_continuous(self, gdf, fill_col, ggplot_obj):
        """Colour polygons on a continuous scale (blue gradient)."""
        values = gdf[fill_col].dropna()
        if values.empty:
            return self._render_choropleth_outline(gdf, ggplot_obj)

        vmin, vmax = values.min(), values.max()
        if vmax == vmin:
            vmax = vmin + 1  # avoid division by zero

        elements = []
        for _, row in gdf.iterrows():
            geom = row.geometry
            val = row[fill_col]

            if pd.isna(val) or geom is None or geom.is_empty:
                polys = _geometry_to_hv_polygons(
                    geom, color='lightgray', alpha=0.4,
                    line_color='white', line_width=0.5,
                )
                elements.extend(polys)
                continue

            # Map value to blue intensity
            t = (val - vmin) / (vmax - vmin)  # 0 → 1
            r = int(220 - 180 * t)
            g = int(230 - 180 * t)
            b = int(255 - 50 * t)
            hex_color = f'#{r:02x}{g:02x}{b:02x}'

            polys = _geometry_to_hv_polygons(
                geom, color=hex_color,
                alpha=self.params['alpha'],
                line_color='white', line_width=0.5,
            )
            elements.extend(polys)

        if not elements:
            return hv.Path([]).opts(width=800, height=400)

        return hv.Overlay(elements).opts(
            width=800, height=400,
            xlabel='Longitude', ylabel='Latitude',
            xaxis=None, yaxis=None,
        )

    def _render_choropleth_categorical(self, gdf, fill_col, ggplot_obj):
        """Colour polygons by discrete categories."""
        categories = gdf[fill_col].dropna().unique()
        palette = ggplot_obj.default_colors
        cat_colors = {cat: palette[i % len(palette)]
                      for i, cat in enumerate(sorted(categories))}

        elements = []
        for _, row in gdf.iterrows():
            geom = row.geometry
            cat = row[fill_col]
            clr = cat_colors.get(cat, 'lightgray') if pd.notna(cat) else 'lightgray'

            polys = _geometry_to_hv_polygons(
                geom, color=clr,
                alpha=self.params['alpha'],
                line_color='white', line_width=0.5,
            )
            elements.extend(polys)

        if not elements:
            return hv.Path([]).opts(width=800, height=400)

        return hv.Overlay(elements).opts(
            width=800, height=400,
            xlabel='Longitude', ylabel='Latitude',
            xaxis=None, yaxis=None,
        )

    def _render_choropleth_outline(self, gdf, ggplot_obj):
        """Render geometry outlines only (no fill variable)."""
        elements = []
        for _, row in gdf.iterrows():
            geom = row.geometry
            polys = _geometry_to_hv_polygons(
                geom, color='lightblue',
                alpha=0.3, line_color='gray', line_width=0.5,
            )
            elements.extend(polys)

        if not elements:
            return hv.Path([]).opts(width=800, height=400)

        return hv.Overlay(elements).opts(
            width=800, height=400,
            xlabel='Longitude', ylabel='Latitude',
        )


# Export the geom
__all__ = ['geom_map']
