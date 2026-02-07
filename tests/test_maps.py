"""Tests for geom_map: point maps, world outlines, and choropleth."""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import ggplot, aes, geom_map

# Conditionally import geopandas (tests that need it are marked)
gpd = pytest.importorskip("geopandas", reason="geopandas required for choropleth tests")
from shapely.geometry import Polygon, MultiPolygon, box


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def cities_data():
    """Simple city lon/lat dataset."""
    return pd.DataFrame({
        'city': ['Paris', 'London', 'Berlin', 'Rome', 'Madrid'],
        'longitude': [2.35, -0.12, 13.40, 12.50, -3.70],
        'latitude': [48.86, 51.51, 52.52, 41.90, 40.42],
        'population': [2.16, 8.98, 3.75, 2.87, 3.22],
        'country': ['France', 'UK', 'Germany', 'Italy', 'Spain'],
    })


@pytest.fixture
def cities_auto_detect():
    """Data with common auto-detect column names."""
    return pd.DataFrame({
        'lon': [2.35, -0.12, 13.40],
        'lat': [48.86, 51.51, 52.52],
        'name': ['Paris', 'London', 'Berlin'],
    })


@pytest.fixture
def region_gdf():
    """Small GeoDataFrame with rectangular 'countries' for testing choropleth."""
    return gpd.GeoDataFrame({
        'name': ['A', 'B', 'C', 'D'],
        'value': [10.0, 40.0, 25.0, 5.0],
        'category': ['Low', 'High', 'Mid', 'Low'],
        'geometry': [
            box(0, 0, 1, 1),
            box(1, 0, 2, 1),
            box(0, 1, 1, 2),
            box(1, 1, 2, 2),
        ],
    })


@pytest.fixture
def multi_polygon_gdf():
    """GeoDataFrame with a MultiPolygon entry."""
    mp = MultiPolygon([box(0, 0, 0.5, 0.5), box(0.6, 0.6, 1, 1)])
    return gpd.GeoDataFrame({
        'name': ['Islands'],
        'value': [99.0],
        'geometry': [mp],
    })


# ---------------------------------------------------------------------------
# Simple map (scatter)
# ---------------------------------------------------------------------------

class TestSimpleMap:
    def test_simple_scatter(self, cities_data):
        p = ggplot(cities_data, aes(x='longitude', y='latitude')).geom_map(map_type='simple')
        result = p._render()
        assert result is not None
        assert isinstance(result, (hv.Scatter, hv.Overlay))

    def test_simple_with_color(self, cities_data):
        p = ggplot(cities_data, aes(x='longitude', y='latitude', color='country')).geom_map(map_type='simple')
        result = p._render()
        assert result is not None

    def test_auto_detect_columns(self, cities_auto_detect):
        """Auto-detects 'lon'/'lat' column names."""
        p = ggplot(cities_auto_detect, aes()).geom_map(map_type='simple')
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# World outline
# ---------------------------------------------------------------------------

class TestWorldMap:
    def test_world_outline(self, cities_data):
        """World outline should render even without geoviews (using built-in paths)."""
        p = ggplot(cities_data, aes(x='longitude', y='latitude')).geom_map(map_type='world')
        result = p._render()
        assert result is not None

    def test_world_with_data_points(self, cities_data):
        p = ggplot(cities_data, aes(x='longitude', y='latitude')).geom_map(map_type='world')
        result = p._render()
        # Should contain both Path (outline) and Scatter (points) in an Overlay
        assert result is not None

    def test_world_via_plus(self, cities_data):
        p = ggplot(cities_data, aes(x='longitude', y='latitude')) + geom_map(map_type='world')
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Point map (points on outline)
# ---------------------------------------------------------------------------

class TestPointMap:
    def test_points_on_outline(self, cities_data):
        p = ggplot(cities_data, aes(x='longitude', y='latitude')).geom_map(map_type='points')
        result = p._render()
        assert result is not None

    def test_points_with_color(self, cities_data):
        p = ggplot(cities_data, aes(x='longitude', y='latitude', color='country')).geom_map(map_type='points')
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Choropleth (the new feature)
# ---------------------------------------------------------------------------

class TestChoropleth:
    def test_choropleth_continuous(self, region_gdf):
        """Continuous fill variable -> gradient-coloured polygons."""
        p = ggplot(region_gdf, aes(fill='value')).geom_map(
            map_type='choropleth', geometry=region_gdf,
        )
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Overlay)

    def test_choropleth_categorical(self, region_gdf):
        """Categorical fill variable -> discrete-coloured polygons."""
        p = ggplot(region_gdf, aes(fill='category')).geom_map(
            map_type='choropleth', geometry=region_gdf,
        )
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Overlay)

    def test_choropleth_outline_only(self, region_gdf):
        """No fill aesthetic -> just outlines."""
        p = ggplot(region_gdf, aes()).geom_map(
            map_type='choropleth', geometry=region_gdf,
        )
        result = p._render()
        assert result is not None

    def test_choropleth_data_is_geodataframe(self, region_gdf):
        """If data itself is a GeoDataFrame, geometry param can be omitted."""
        p = ggplot(region_gdf, aes(fill='value')).geom_map(map_type='choropleth')
        result = p._render()
        assert result is not None

    def test_choropleth_multipolygon(self, multi_polygon_gdf):
        """MultiPolygon geometries should render multiple polygon pieces."""
        p = ggplot(multi_polygon_gdf, aes(fill='value')).geom_map(
            map_type='choropleth', geometry=multi_polygon_gdf,
        )
        result = p._render()
        assert result is not None

    def test_choropleth_merge_on(self, region_gdf):
        """Separate data + geometry joined via merge_on."""
        data = pd.DataFrame({
            'name': ['A', 'B', 'C', 'D'],
            'score': [100, 200, 150, 50],
        })
        p = ggplot(data, aes(fill='score')).geom_map(
            map_type='choropleth',
            geometry=region_gdf,
            merge_on='name',
        )
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Overlay)

    def test_choropleth_polygon_count(self, region_gdf):
        """Should produce at least as many Polygons elements as rows."""
        p = ggplot(region_gdf, aes(fill='value')).geom_map(
            map_type='choropleth', geometry=region_gdf,
        )
        result = p._render()
        # Collect all Polygons from the Overlay
        poly_count = sum(1 for el in result if isinstance(el, hv.Polygons))
        assert poly_count >= len(region_gdf)

    def test_choropleth_via_plus(self, region_gdf):
        p = (ggplot(region_gdf, aes(fill='value'))
             + geom_map(map_type='choropleth', geometry=region_gdf))
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Built-in world outline helper
# ---------------------------------------------------------------------------

class TestBuiltinOutline:
    def test_builtin_world_outline_returns_path(self):
        from ggviews.geom_map import _builtin_world_outline
        path = _builtin_world_outline()
        assert isinstance(path, hv.Path)

    def test_builtin_world_outline_has_data(self):
        from ggviews.geom_map import _builtin_world_outline
        path = _builtin_world_outline()
        # Should contain 7 continents as separate path segments
        df = path.dframe()
        assert len(df) > 50  # plenty of coordinate points


# ---------------------------------------------------------------------------
# Geometry-to-HV helper
# ---------------------------------------------------------------------------

class TestGeometryConversion:
    def test_polygon_to_hv(self):
        from ggviews.geom_map import _geometry_to_hv_polygons
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        hv_polys = _geometry_to_hv_polygons(poly, color='red')
        assert len(hv_polys) == 1
        assert isinstance(hv_polys[0], hv.Polygons)

    def test_multipolygon_to_hv(self):
        from ggviews.geom_map import _geometry_to_hv_polygons
        mp = MultiPolygon([
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(2, 2), (3, 2), (3, 3), (2, 3)]),
        ])
        hv_polys = _geometry_to_hv_polygons(mp, color='blue')
        assert len(hv_polys) == 2

    def test_empty_geometry(self):
        from ggviews.geom_map import _geometry_to_hv_polygons
        from shapely.geometry import Polygon as ShapelyPolygon
        empty = ShapelyPolygon()
        assert _geometry_to_hv_polygons(empty) == []

    def test_none_geometry(self):
        from ggviews.geom_map import _geometry_to_hv_polygons
        assert _geometry_to_hv_polygons(None) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
