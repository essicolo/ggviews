"""Tests for gghighlight - conditional data highlighting."""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import ggplot, aes, gghighlight, geom_point, geom_line, geom_bar


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def iris_like():
    """Iris-like dataset with three species."""
    np.random.seed(42)
    species = ['setosa'] * 20 + ['versicolor'] * 20 + ['virginica'] * 20
    return pd.DataFrame({
        'sepal_length': np.random.normal(5.0, 0.5, 60),
        'sepal_width':  np.random.normal(3.0, 0.4, 60),
        'species': species,
    })


@pytest.fixture
def line_data():
    """Multi-group time-series data."""
    dfs = []
    for grp in ['A', 'B', 'C', 'D']:
        x = np.arange(10)
        slope = {'A': 3, 'B': 1, 'C': 0.5, 'D': -1}[grp]
        y = slope * x + np.random.RandomState(hash(grp) % 2**31).normal(0, 1, 10)
        dfs.append(pd.DataFrame({'x': x, 'y': y, 'group': grp}))
    return pd.concat(dfs, ignore_index=True)


@pytest.fixture
def bar_data():
    return pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'value': [10, 25, 15, 30, 5],
    })


# ── helpers ───────────────────────────────────────────────────────────────────

def _collect_elements(plot):
    """Recursively collect leaf HoloViews elements from any composite."""
    out = []
    if isinstance(plot, (hv.Layout, hv.NdLayout)):
        for item in plot:
            out.extend(_collect_elements(item))
    elif isinstance(plot, hv.Overlay):
        for item in plot:
            out.extend(_collect_elements(item))
    elif isinstance(plot, hv.Element):
        out.append(plot)
    return out


# ── row-level predicate (string) ─────────────────────────────────────────────

class TestRowLevelString:
    def test_renders(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("species == 'setosa'"))
        result = p._render()
        assert result is not None

    def test_produces_overlay(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("species == 'setosa'"))
        result = p._render()
        elements = _collect_elements(result)
        # Should have at least 2 elements: unhighlighted + highlighted
        assert len(elements) >= 2

    def test_highlighted_subset_size(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("species == 'setosa'"))
        result = p._render()
        scatters = [el for el in _collect_elements(result) if isinstance(el, hv.Scatter)]
        # One scatter for highlighted (20 pts), one for unhighlighted (40 pts)
        sizes = sorted([len(s.dframe()) for s in scatters])
        assert sizes == [20, 40]

    def test_numeric_predicate(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("sepal_length > 5.5"))
        result = p._render()
        assert result is not None

    def test_compound_predicate(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("sepal_length > 5 and sepal_width > 3"))
        result = p._render()
        assert result is not None


# ── row-level predicate (callable) ───────────────────────────────────────────

class TestRowLevelCallable:
    def test_lambda_predicate(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight(lambda df: df['species'] == 'virginica'))
        result = p._render()
        elements = _collect_elements(result)
        assert len(elements) >= 2

    def test_callable_numeric(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight(lambda df: df['sepal_length'] > df['sepal_length'].median()))
        result = p._render()
        assert result is not None


# ── group-level predicate ─────────────────────────────────────────────────────

class TestGroupLevel:
    def test_group_by_string(self, line_data):
        p = (ggplot(line_data, aes(x='x', y='y', color='group'))
             .geom_line()
             .gghighlight("y.mean() > 5", use_group_by=True))
        result = p._render()
        assert result is not None

    def test_group_by_callable(self, line_data):
        p = (ggplot(line_data, aes(x='x', y='y', color='group'))
             .geom_line()
             .gghighlight(lambda grp: grp['y'].mean() > 5, use_group_by=True))
        result = p._render()
        assert result is not None

    def test_group_by_fallback_no_group_col(self, iris_like):
        """Without color/group aes, use_group_by should fall back to row-level."""
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
                 .geom_point()
                 .gghighlight("sepal_length > 5", use_group_by=True))
            result = p._render()
        assert result is not None

    def test_top_n_groups(self, line_data):
        """n parameter should limit highlighted groups."""
        p = (ggplot(line_data, aes(x='x', y='y', color='group'))
             .geom_line()
             .gghighlight(lambda grp: True, use_group_by=True, n=2))
        result = p._render()
        assert result is not None


# ── + operator ────────────────────────────────────────────────────────────────

class TestPlusOperator:
    def test_plus_syntax(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             + geom_point()
             + gghighlight("species == 'setosa'"))
        result = p._render()
        assert result is not None

    def test_plus_with_grouped(self, line_data):
        p = (ggplot(line_data, aes(x='x', y='y', color='group'))
             + geom_line()
             + gghighlight(lambda grp: grp['y'].max() > 20, use_group_by=True))
        result = p._render()
        assert result is not None


# ── styling ───────────────────────────────────────────────────────────────────

class TestStyling:
    def test_custom_unhighlighted_colour(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("species == 'setosa'", unhighlighted_colour='lightblue'))
        result = p._render()
        assert result is not None

    def test_custom_unhighlighted_alpha(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("species == 'setosa'", unhighlighted_alpha=0.1))
        result = p._render()
        assert result is not None


# ── label_key ─────────────────────────────────────────────────────────────────

class TestLabelKey:
    def test_label_key_adds_labels(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("species == 'setosa'", label_key='species'))
        result = p._render()
        types = {type(el).__name__ for el in _collect_elements(result)}
        assert 'Labels' in types

    def test_label_key_invalid_column_warns(self, iris_like):
        with pytest.warns(UserWarning, match="not in data"):
            p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
                 .geom_point()
                 .gghighlight("species == 'setosa'", label_key='nonexistent'))
            p._render()


# ── with bars ─────────────────────────────────────────────────────────────────

class TestWithBars:
    def test_bar_highlight(self, bar_data):
        p = (ggplot(bar_data, aes(x='category', y='value'))
             .geom_bar(stat='identity')
             .gghighlight("value > 15"))
        result = p._render()
        assert result is not None

    def test_bar_highlight_callable(self, bar_data):
        p = (ggplot(bar_data, aes(x='category', y='value'))
             .geom_bar(stat='identity')
             .gghighlight(lambda df: df['value'] == df['value'].max()))
        result = p._render()
        assert result is not None


# ── edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_no_matches(self, iris_like):
        """If predicate matches nothing, should still render (all gray)."""
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("sepal_length > 999"))
        result = p._render()
        assert result is not None

    def test_all_match(self, iris_like):
        """If predicate matches everything, no gray layer needed."""
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("sepal_length > 0"))
        result = p._render()
        assert result is not None

    def test_invalid_predicate_type(self, iris_like):
        with pytest.raises(TypeError, match="predicate must be"):
            p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
                 .geom_point()
                 .gghighlight(42))
            p._render()

    def test_multiple_layers(self, iris_like):
        """Highlight should apply to all layers."""
        from ggviews import geom_smooth
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .geom_smooth(method='lm')
             .gghighlight("species == 'setosa'"))
        result = p._render()
        assert result is not None

    def test_with_theme(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("species == 'setosa'")
             .theme_minimal())
        result = p._render()
        assert result is not None

    def test_with_facets(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .gghighlight("sepal_length > 5")
             .facet_wrap('species'))
        result = p._render()
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
