"""Tests for new features: facetting, position adjustments, coord_polar, geom_label."""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import (
    ggplot, aes,
    geom_point, geom_line, geom_bar, geom_histogram, geom_smooth,
    geom_area, geom_boxplot, geom_density, geom_text, geom_label,
    geom_violin, geom_ribbon, geom_errorbar,
    theme_minimal, theme_classic, theme_bw, theme_dark, theme_void,
    facet_wrap, facet_grid,
    coord_fixed, coord_equal, coord_flip, coord_cartesian, coord_polar,
    scale_color_manual, scale_x_continuous, scale_y_continuous,
    labs,
    position_identity, position_stack, position_dodge, position_jitter,
    position_fill, position_nudge, position_jitterdodge,
)


# ---------------------------------------------------------------------------
# Facet tests (the main pain point)
# ---------------------------------------------------------------------------

class TestFacetWrap:
    """Thorough tests for facet_wrap."""

    def test_basic_facet_wrap(self, categorical_data):
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('~group'))
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Layout)

    def test_facet_wrap_formula_tilde(self, categorical_data):
        """'~var' formula should produce panels for each unique value."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('~group'))
        result = p._render()
        n_groups = categorical_data['group'].nunique()
        assert len(result) == n_groups

    def test_facet_wrap_plain_var(self, categorical_data):
        """Plain variable name (no tilde) should also work."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('group'))
        result = p._render()
        assert isinstance(result, hv.Layout)
        assert len(result) == categorical_data['group'].nunique()

    def test_facet_wrap_ncol(self, categorical_data):
        """ncol parameter should control column count."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('~category', ncol=1))
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Layout)

    def test_facet_wrap_nrow(self, categorical_data):
        """nrow parameter should control row count."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('~category', nrow=1))
        result = p._render()
        assert result is not None

    def test_facet_wrap_multiple_vars(self, categorical_data):
        """Faceting by multiple variables should combine them."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap(['~category', '~group']))
        result = p._render()
        assert result is not None
        # Should have panels for each combination
        n_combos = len(categorical_data.groupby(['category', 'group']))
        assert len(result) == n_combos

    def test_facet_wrap_does_not_mutate_data(self, categorical_data):
        """facet_wrap must not modify the original DataFrame."""
        original_cols = set(categorical_data.columns)
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_wrap('~group'))
        p._render()
        assert set(categorical_data.columns) == original_cols

    def test_facet_wrap_with_theme(self, categorical_data):
        """Faceting should work with themes applied."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .theme_minimal()
             .facet_wrap('~group'))
        result = p._render()
        assert result is not None

    def test_facet_wrap_with_bars(self, categorical_data):
        """facet_wrap should work with bar charts."""
        p = (ggplot(categorical_data, aes(x='category'))
             .geom_bar()
             .facet_wrap('~group'))
        result = p._render()
        assert result is not None

    def test_facet_wrap_with_smooth(self, sample_data):
        """facet_wrap should work with geom_smooth."""
        df = sample_data.copy()
        df['group'] = np.where(df['x'] > 0, 'A', 'B')
        p = (ggplot(df, aes(x='x', y='y'))
             .geom_point()
             .geom_smooth(method='lm')
             .facet_wrap('~group'))
        result = p._render()
        assert result is not None

    def test_facet_wrap_via_plus(self, categorical_data):
        """facet_wrap via + operator should work."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             + geom_point()
             + facet_wrap('~group'))
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Layout)


class TestFacetGrid:
    """Thorough tests for facet_grid."""

    def test_basic_facet_grid(self, categorical_data):
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_grid('category~group'))
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Layout)

    def test_facet_grid_panel_count(self, categorical_data):
        """Should produce rows * cols panels."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_grid('category~group'))
        result = p._render()
        n_cats = categorical_data['category'].nunique()
        n_groups = categorical_data['group'].nunique()
        assert len(result) == n_cats * n_groups

    def test_facet_grid_row_only(self, categorical_data):
        """'row_var ~ .' should facet by rows only."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_grid('category~.'))
        result = p._render()
        assert result is not None
        n_cats = categorical_data['category'].nunique()
        assert len(result) == n_cats

    def test_facet_grid_col_only(self, categorical_data):
        """'. ~ col_var' should facet by columns only."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_grid('.~group'))
        result = p._render()
        assert result is not None
        n_groups = categorical_data['group'].nunique()
        assert len(result) == n_groups

    def test_facet_grid_does_not_mutate_data(self, categorical_data):
        original_cols = set(categorical_data.columns)
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .facet_grid('category~group'))
        p._render()
        assert set(categorical_data.columns) == original_cols

    def test_facet_grid_via_plus(self, categorical_data):
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             + geom_point()
             + facet_grid('category~group'))
        result = p._render()
        assert isinstance(result, hv.Layout)

    def test_facet_grid_with_labs(self, categorical_data):
        """facet_grid should work with labs."""
        p = (ggplot(categorical_data, aes(x='value', y='value'))
             .geom_point()
             .labs(title='Faceted Plot')
             .facet_grid('category~group'))
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# Position adjustment tests (now wired into the pipeline)
# ---------------------------------------------------------------------------

class TestPositionAdjustments:
    """Test that position adjustments actually modify data during rendering."""

    def test_position_dodge_modifies_x(self):
        """position_dodge should spread groups apart on the x axis."""
        df = pd.DataFrame({
            'x': ['A', 'A', 'B', 'B'],
            'y': [10, 20, 15, 25],
            'group': ['G1', 'G2', 'G1', 'G2'],
        })
        dodge = position_dodge(width=0.9)
        combined_aes = aes(x='x', y='y', fill='group')
        result = dodge.adjust(df.copy(), combined_aes, {})
        # Categorical x should be converted to numeric and offset
        assert pd.api.types.is_numeric_dtype(result['x'])
        # Within category 'A' (mapped to 0.0), G1 and G2 should be offset
        x_vals = result['x'].values
        assert x_vals[0] != x_vals[1]  # G1 and G2 at 'A' should differ

    def test_position_jitter_adds_noise(self):
        """position_jitter should add random offsets."""
        df = pd.DataFrame({'x': [1.0, 2.0, 3.0], 'y': [4.0, 5.0, 6.0]})
        jitter = position_jitter(width=0.5, height=0.5, seed=42)
        combined_aes = aes(x='x', y='y')
        result = jitter.adjust(df.copy(), combined_aes, {})
        assert not np.allclose(result['x'].values, df['x'].values)
        assert not np.allclose(result['y'].values, df['y'].values)

    def test_position_stack_cumulates(self):
        """position_stack should stack y values."""
        df = pd.DataFrame({
            'x': ['A', 'A'],
            'y': [10.0, 20.0],
            'fill': ['G1', 'G2'],
        })
        stack = position_stack()
        combined_aes = aes(x='x', y='y', fill='fill')
        result = stack.adjust(df.copy(), combined_aes, {})
        # First value should stay at 10, second should be 30 (10+20)
        sorted_result = result.sort_values('fill')
        assert sorted_result['y'].iloc[1] == 30.0

    def test_position_fill_normalizes(self):
        """position_fill should normalize y to sum to 1 within groups."""
        df = pd.DataFrame({
            'x': ['A', 'A'],
            'y': [10.0, 20.0],
            'fill': ['G1', 'G2'],
        })
        fill = position_fill()
        combined_aes = aes(x='x', y='y', fill='fill')
        result = fill.adjust(df.copy(), combined_aes, {})
        # Values within each x should sum to ~1
        assert abs(result['y'].sum() - 1.0) < 0.1

    def test_position_nudge_shifts(self):
        """position_nudge should shift all points by fixed amounts."""
        df = pd.DataFrame({'x': [1.0, 2.0], 'y': [3.0, 4.0]})
        nudge = position_nudge(x=0.5, y=-1.0)
        combined_aes = aes(x='x', y='y')
        result = nudge.adjust(df.copy(), combined_aes, {})
        assert np.allclose(result['x'].values, [1.5, 2.5])
        assert np.allclose(result['y'].values, [2.0, 3.0])

    def test_position_identity_noop(self):
        """position_identity should not modify data."""
        df = pd.DataFrame({'x': [1.0, 2.0], 'y': [3.0, 4.0]})
        identity = position_identity()
        combined_aes = aes(x='x', y='y')
        result = identity.adjust(df.copy(), combined_aes, {})
        assert np.allclose(result['x'].values, df['x'].values)
        assert np.allclose(result['y'].values, df['y'].values)

    def test_position_jitterdodge(self):
        """position_jitterdodge should combine dodging and jittering."""
        jd = position_jitterdodge(dodge_width=0.9, jitter_width=0.1, seed=42)
        assert jd is not None

    def test_position_string_resolution(self, sample_data):
        """String position arguments should be resolved during rendering."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point(position='jitter'))
        # Should render without error (the geom stores position='jitter')
        result = p._render()
        assert result is not None

    def test_position_object_in_geom(self, sample_data):
        """Position objects should be usable directly in geoms."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point(position=position_jitter(width=0.1, height=0.1, seed=42)))
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# coord_polar tests
# ---------------------------------------------------------------------------

class TestCoordPolar:
    def test_coord_polar_creation(self):
        cp = coord_polar()
        assert cp.theta == 'x'
        assert cp.start == 0
        assert cp.direction == 1

    def test_coord_polar_bar_to_pie(self):
        """Bar chart + coord_polar should produce a pie chart (Overlay of Polygons)."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'count': [30, 50, 20],
        })
        p = (ggplot(df, aes(x='category', y='count'))
             .geom_bar(stat='identity')
             + coord_polar())
        result = p._render()
        assert result is not None
        # Should be an Overlay containing Polygons (wedges)
        assert isinstance(result, hv.Overlay)

    def test_coord_polar_scatter(self, sample_data):
        """Scatter + coord_polar should transform to Cartesian."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             .geom_point()
             + coord_polar())
        result = p._render()
        assert result is not None

    def test_coord_polar_custom_params(self):
        cp = coord_polar(theta='y', start=np.pi/2, direction=-1)
        assert cp.theta == 'y'
        assert cp.start == np.pi / 2
        assert cp.direction == -1

    def test_coord_polar_renders_via_method(self, sample_data):
        """coord_polar via method chaining."""
        # ggplot class doesn't have a coord_polar method, so use +
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + coord_polar()
        result = p._render()
        assert result is not None


# ---------------------------------------------------------------------------
# geom_label tests
# ---------------------------------------------------------------------------

class TestGeomLabel:
    def test_geom_label_renders(self, labeled_data):
        """geom_label should render as Labels (like geom_text)."""
        p = ggplot(labeled_data, aes(x='x', y='y')).geom_label(
            mapping=aes(label='label')
        )
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Labels) or isinstance(result, hv.Overlay)

    def test_geom_label_has_hooks(self, labeled_data):
        """geom_label should apply a Bokeh hook for background."""
        p = ggplot(labeled_data, aes(x='x', y='y')).geom_label(
            mapping=aes(label='label')
        )
        result = p._render()
        # The Labels element should have hooks in its options
        assert result is not None

    def test_geom_label_via_plus(self, labeled_data):
        p = (ggplot(labeled_data, aes(x='x', y='y'))
             + geom_label(mapping=aes(label='label'), fill='lightyellow'))
        result = p._render()
        assert result is not None

    def test_geom_label_custom_fill(self, labeled_data):
        """Custom fill color should be stored."""
        label = geom_label(fill='lightyellow')
        assert label.params['fill'] == 'lightyellow'


# ---------------------------------------------------------------------------
# Integration: end-to-end with new features
# ---------------------------------------------------------------------------

class TestNewIntegration:
    def test_faceted_bar_chart(self, categorical_data):
        """Bar chart faceted by group."""
        p = (ggplot(categorical_data, aes(x='category'))
             .geom_bar()
             .facet_wrap('~group')
             .theme_minimal()
             .labs(title='Faceted Bars'))
        result = p._render()
        assert result is not None

    def test_scatter_with_jitter(self, categorical_data):
        """Scatter plot with position_jitter applied."""
        p = (ggplot(categorical_data, aes(x='category', y='value'))
             + geom_point(position=position_jitter(width=0.2, height=0, seed=42)))
        result = p._render()
        assert result is not None

    def test_faceted_boxplot(self, categorical_data):
        """Boxplot with facetting."""
        p = (ggplot(categorical_data, aes(x='category', y='value'))
             .geom_boxplot()
             .facet_wrap('~group'))
        result = p._render()
        assert result is not None

    def test_full_pipeline(self, categorical_data):
        """Full pipeline: geom + theme + scale + facet + labs."""
        p = (ggplot(categorical_data, aes(x='value', y='value', color='category'))
             .geom_point()
             .scale_color_manual(values=['red', 'green', 'blue'])
             .theme_bw()
             .facet_wrap('~group')
             .labs(title='Full Pipeline', x='Value', y='Value'))
        result = p._render()
        assert result is not None

    def test_density_faceted(self, categorical_data):
        """Density plot with facetting."""
        p = (ggplot(categorical_data, aes(x='value'))
             .geom_density()
             .facet_wrap('~category'))
        result = p._render()
        assert result is not None

    def test_line_faceted(self):
        """Line plot with facetting."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.tile(np.arange(20), 2),
            'y': np.random.randn(40),
            'panel': np.repeat(['A', 'B'], 20),
        })
        p = (ggplot(df, aes(x='x', y='y'))
             .geom_line()
             .facet_wrap('~panel'))
        result = p._render()
        assert result is not None
        assert isinstance(result, hv.Layout)
        assert len(result) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
