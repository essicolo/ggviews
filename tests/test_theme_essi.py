"""Tests for theme_essi and palette_essi."""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import ggplot, aes, geom_point, geom_line, geom_bar, theme_essi, palette_essi
from ggviews.themes import _ESSI_BASE, _hex_to_hsl, _hsl_to_hex


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def iris_like():
    np.random.seed(42)
    species = ['setosa'] * 20 + ['versicolor'] * 20 + ['virginica'] * 20
    return pd.DataFrame({
        'sepal_length': np.random.normal(5.5, 0.5, 60),
        'sepal_width':  np.random.normal(3.0, 0.3, 60),
        'species': species,
    })


@pytest.fixture
def multi_group():
    """12-group dataset to test palette expansion beyond 8."""
    np.random.seed(99)
    groups = [f'G{i}' for i in range(12)]
    dfs = []
    for g in groups:
        dfs.append(pd.DataFrame({
            'x': np.random.uniform(0, 10, 5),
            'y': np.random.uniform(0, 10, 5),
            'group': g,
        }))
    return pd.concat(dfs, ignore_index=True)


# ── palette_essi ──────────────────────────────────────────────────────────────

class TestPaletteEssi:
    def test_returns_list(self):
        assert isinstance(palette_essi(), list)

    def test_default_8_colors(self):
        pal = palette_essi(8)
        assert len(pal) == 8

    def test_base_colors_match_bcgsc(self):
        pal = palette_essi(7)
        assert pal == _ESSI_BASE[:7]

    def test_n_zero(self):
        assert palette_essi(0) == []

    def test_n_one(self):
        assert len(palette_essi(1)) == 1
        assert palette_essi(1)[0] == '#2271B2'

    def test_expand_to_12(self):
        pal = palette_essi(12)
        assert len(pal) == 12
        # First 7 should be the base colors
        assert pal[:7] == _ESSI_BASE[:7]

    def test_expand_to_20(self):
        pal = palette_essi(20)
        assert len(pal) == 20

    def test_all_valid_hex(self):
        for c in palette_essi(15):
            assert c.startswith('#')
            assert len(c) == 7
            # Should be valid hex
            int(c[1:], 16)

    def test_expanded_colors_are_unique(self):
        pal = palette_essi(12)
        # At least 10 of 12 should be distinct (HSL rounding may cause dupes)
        assert len(set(pal)) >= 10

    def test_no_white_or_near_white(self):
        """Expanded colors should not be too light to see on beige background."""
        for c in palette_essi(15):
            _, _, l = _hex_to_hsl(c)
            assert l < 0.90  # not near-white


# ── HSL helpers ───────────────────────────────────────────────────────────────

class TestHSLHelpers:
    def test_roundtrip(self):
        for hex_color in ['#FF0000', '#00FF00', '#0000FF', '#2271B2', '#F748A5']:
            h, s, l = _hex_to_hsl(hex_color)
            result = _hsl_to_hex(h, s, l)
            # Allow ±1 in each channel due to rounding
            for i in range(1, 7, 2):
                orig = int(hex_color[i:i+2], 16)
                got  = int(result[i:i+2], 16)
                assert abs(orig - got) <= 1, f'{hex_color} -> {result}'

    def test_black(self):
        h, s, l = _hex_to_hsl('#000000')
        assert l == 0.0

    def test_white(self):
        h, s, l = _hex_to_hsl('#FFFFFF')
        assert l == 1.0


# ── theme_essi rendering ─────────────────────────────────────────────────────

class TestThemeEssi:
    def test_basic_render(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .theme_essi())
        result = p._render()
        assert result is not None

    def test_with_color_grouping(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width', color='species'))
             .geom_point()
             .theme_essi())
        result = p._render()
        assert result is not None

    def test_palette_applied_to_ggplot(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .theme_essi())
        # After theme_essi, default_colors should be the BCGSC palette
        assert p.default_colors[0] == '#2271B2'

    def test_plus_syntax(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length', y='sepal_width')) + geom_point() + theme_essi()
        result = p._render()
        assert result is not None

    def test_with_bars(self):
        df = pd.DataFrame({
            'cat': ['A', 'B', 'C', 'D'],
            'val': [10, 25, 15, 30],
        })
        p = (ggplot(df, aes(x='cat', y='val'))
             .geom_bar(stat='identity')
             .theme_essi())
        result = p._render()
        assert result is not None

    def test_with_lines(self):
        df = pd.DataFrame({
            'x': range(20),
            'y': np.cumsum(np.random.normal(0, 1, 20)),
        })
        p = (ggplot(df, aes(x='x', y='y'))
             .geom_line()
             .theme_essi())
        result = p._render()
        assert result is not None

    def test_many_groups_renders(self, multi_group):
        """With 12 groups, should render without error."""
        p = (ggplot(multi_group, aes(x='x', y='y', color='group'))
             .geom_point()
             .theme_essi())
        result = p._render()
        assert result is not None

    def test_palette_expandable_via_function(self):
        """palette_essi(n) returns any requested number of colors."""
        assert len(palette_essi(12)) == 12
        assert len(palette_essi(20)) == 20

    def test_with_facets(self, iris_like):
        from ggviews import facet_wrap
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .theme_essi()
             .facet_wrap('species'))
        result = p._render()
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
