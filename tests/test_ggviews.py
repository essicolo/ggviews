"""Comprehensive test suite for ggviews."""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import (
    ggplot, aes,
    geom_point, geom_line, geom_bar, geom_histogram, geom_smooth,
    geom_area, geom_boxplot, geom_density, geom_text, geom_violin,
    geom_ribbon, geom_errorbar,
    theme_minimal, theme_classic, theme_bw, theme_dark, theme_void,
    facet_wrap, facet_grid,
    coord_fixed, coord_equal, coord_flip, coord_cartesian,
    scale_color_manual, scale_x_continuous, scale_y_continuous,
    labs,
    position_identity, position_stack, position_dodge, position_jitter,
)


# ---------------------------------------------------------------------------
# Core: ggplot + aes
# ---------------------------------------------------------------------------

class TestCore:
    def test_ggplot_creates_object(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y'))
        assert p is not None
        assert p.data is sample_data

    def test_aes_stores_mappings(self):
        a = aes(x='col_a', y='col_b', color='col_c')
        assert a.mappings['x'] == 'col_a'
        assert a.mappings['y'] == 'col_b'
        assert a.mappings['color'] == 'col_c'

    def test_repr(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point()
        r = repr(p)
        assert 'ggplot' in r
        assert '1' in r  # 1 layer

    def test_copy_immutability(self, sample_data):
        """Adding a layer should return a new object (copy)."""
        p1 = ggplot(sample_data, aes(x='x', y='y'))
        p2 = p1.geom_point()
        # p2 should have a layer, p1 should not
        assert len(p1.layers) == 0
        assert len(p2.layers) == 1

    def test_plus_operator(self, sample_data):
        """The + operator should work like ggplot2."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point()
        assert len(p.layers) == 1


# ---------------------------------------------------------------------------
# Geoms -- basic rendering
# ---------------------------------------------------------------------------

class TestGeoms:
    def test_geom_point_basic(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point()
        result = p._render()
        assert result is not None

    def test_geom_point_with_color(self, categorical_data):
        p = ggplot(categorical_data, aes(x='value', y='value', color='group')).geom_point()
        result = p._render()
        assert result is not None

    def test_geom_line(self, timeseries_data):
        p = ggplot(timeseries_data, aes(x='x', y='y')).geom_line()
        result = p._render()
        assert result is not None

    def test_geom_bar_count(self, categorical_data):
        p = ggplot(categorical_data, aes(x='category')).geom_bar()
        result = p._render()
        assert result is not None

    def test_geom_bar_identity(self, categorical_data):
        summary = categorical_data.groupby('category')['value'].mean().reset_index()
        p = ggplot(summary, aes(x='category', y='value')).geom_bar(stat='identity')
        result = p._render()
        assert result is not None

    def test_geom_histogram(self, sample_data):
        p = ggplot(sample_data, aes(x='x')).geom_histogram()
        result = p._render()
        assert result is not None

    def test_geom_smooth_lm(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_smooth(method='lm')
        result = p._render()
        assert result is not None

    def test_geom_smooth_loess(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_smooth(method='loess')
        result = p._render()
        assert result is not None

    def test_geom_area(self, timeseries_data):
        p = ggplot(timeseries_data, aes(x='x', y='y')).geom_area()
        result = p._render()
        assert result is not None

    def test_geom_boxplot(self, categorical_data):
        p = ggplot(categorical_data, aes(x='category', y='value')).geom_boxplot()
        result = p._render()
        assert result is not None

    def test_geom_density(self, sample_data):
        p = ggplot(sample_data, aes(x='x')).geom_density()
        result = p._render()
        assert result is not None

    def test_geom_text(self, labeled_data):
        p = ggplot(labeled_data, aes(x='x', y='y')).geom_text(mapping=aes(label='label'))
        result = p._render()
        assert result is not None
        # Should render as Labels, not Scatter
        assert isinstance(result, hv.Labels) or isinstance(result, hv.Overlay)

    def test_geom_violin(self, categorical_data):
        p = ggplot(categorical_data, aes(x='category', y='value')).geom_violin()
        result = p._render()
        assert result is not None

    def test_geom_ribbon(self, timeseries_data):
        p = ggplot(timeseries_data, aes(x='x')).geom_ribbon(
            mapping=aes(ymin='ymin', ymax='ymax')
        )
        result = p._render()
        assert result is not None

    def test_geom_errorbar(self, timeseries_data):
        subset = timeseries_data.iloc[::10]  # every 10th row
        p = ggplot(subset, aes(x='x')).geom_errorbar(
            mapping=aes(ymin='ymin', ymax='ymax')
        )
        result = p._render()
        assert result is not None

    def test_multiple_layers(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().geom_smooth(method='lm')
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

class TestThemes:
    def test_theme_minimal(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().theme_minimal()
        result = p._render()
        assert result is not None

    def test_theme_classic(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().theme_classic()
        result = p._render()
        assert result is not None

    def test_theme_bw(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().theme_bw()
        result = p._render()
        assert result is not None

    def test_theme_dark(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().theme_dark()
        result = p._render()
        assert result is not None

    def test_theme_void(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().theme_void()
        result = p._render()
        assert result is not None

    def test_theme_via_plus(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + theme_minimal()
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Scales
# ---------------------------------------------------------------------------

class TestScales:
    def test_scale_color_manual(self, categorical_data):
        p = (ggplot(categorical_data, aes(x='value', y='value', color='group'))
             .geom_point()
             .scale_color_manual(values=['red', 'blue']))
        result = p._render()
        assert result is not None

    def test_scale_x_continuous(self, sample_data):
        p = (ggplot(sample_data, aes(x='x', y='y'))
             .geom_point()
             + scale_x_continuous(name='My X', limits=(-5, 5)))
        result = p._render()
        assert result is not None

    def test_scale_y_continuous(self, sample_data):
        p = (ggplot(sample_data, aes(x='x', y='y'))
             .geom_point()
             + scale_y_continuous(name='My Y', limits=(-5, 5)))
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Facets
# ---------------------------------------------------------------------------

class TestFacets:
    def test_facet_wrap(self, categorical_data):
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('~group'))
        result = p._render()
        assert result is not None

    def test_facet_grid(self, categorical_data):
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_grid('category~group'))
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Coordinate systems
# ---------------------------------------------------------------------------

class TestCoordinateSystems:
    def test_coord_fixed(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + coord_fixed()
        assert p.coord_system is not None
        assert hasattr(p.coord_system, 'ratio')
        assert p.coord_system.ratio == 1

    def test_coord_fixed_custom_ratio(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + coord_fixed(ratio=2)
        assert p.coord_system is not None
        assert p.coord_system.ratio == 2

    def test_coord_equal(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + coord_equal()
        assert p.coord_system is not None
        assert p.coord_system.ratio == 1

    def test_coord_flip(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + coord_flip()
        assert p.coord_system is not None
        assert hasattr(p.coord_system, '_apply')

    def test_coord_fixed_renders(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().coord_fixed()
        result = p._render()
        assert result is not None

    def test_coord_flip_renders(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().coord_flip()
        result = p._render()
        assert result is not None

    def test_chaining_coord_fixed(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().coord_fixed()
        assert p.coord_system is not None
        assert p.coord_system.ratio == 1

    def test_chaining_coord_equal(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().coord_equal()
        assert p.coord_system is not None
        assert p.coord_system.ratio == 1


# ---------------------------------------------------------------------------
# Labs (utility)
# ---------------------------------------------------------------------------

class TestLabs:
    def test_labs_method(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().labs(
            title='Test Plot', x='X Label', y='Y Label'
        )
        result = p._render()
        assert result is not None

    def test_labs_via_plus(self, sample_data):
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + labs(title='Hello')
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Position classes (no infinite recursion)
# ---------------------------------------------------------------------------

class TestPositions:
    def test_position_identity(self):
        p = position_identity()
        assert p is not None

    def test_position_stack(self):
        p = position_stack()
        assert p is not None

    def test_position_dodge(self):
        p = position_dodge()
        assert p is not None

    def test_position_jitter(self):
        p = position_jitter(width=0.1, height=0.1)
        assert p is not None


# ---------------------------------------------------------------------------
# Integration: end-to-end workflows
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_full_scatter_workflow(self, sample_data):
        """Full ggplot2-style scatter plot with labels and theme."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             .geom_point()
             .labs(title='Scatter', x='X', y='Y')
             .theme_minimal())
        result = p._render()
        assert result is not None

    def test_bar_with_fill(self, categorical_data):
        """Bar chart with fill aesthetic for grouped bars."""
        p = (ggplot(categorical_data, aes(x='category', fill='group'))
             .geom_bar())
        result = p._render()
        assert result is not None

    def test_density_grouped(self, categorical_data):
        """Multiple density curves by group."""
        p = (ggplot(categorical_data, aes(x='value', color='category'))
             .geom_density())
        result = p._render()
        assert result is not None

    def test_faceted_scatter(self, categorical_data):
        """Faceted scatter plot."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('~group'))
        result = p._render()
        assert result is not None

    def test_point_smooth_combo(self, sample_data):
        """Points + smooth line overlaid."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             .geom_point()
             .geom_smooth(method='lm'))
        result = p._render()
        assert result is not None

    def test_plus_operator_multi(self, sample_data):
        """Chaining multiple components via + operator."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + geom_smooth(method='lm')
             + theme_minimal()
             + coord_fixed()
             + labs(title='Combined'))
        result = p._render()
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
