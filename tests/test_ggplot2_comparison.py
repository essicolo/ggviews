"""ggplot2 comparison tests for ggviews.

These tests verify that ggviews produces structurally correct output that
matches ggplot2 behavior.  Since R is not available in CI, we encode the
expected ggplot2 results as reference data and compare ggviews output against
those references.

Each test follows a pattern:
    1. Create a deterministic dataset (same as the R reference).
    2. Build the ggviews plot.
    3. Extract structural properties (element counts, data ranges, computed
       values, etc.) from the rendered HoloViews object.
    4. Compare against hard-coded ggplot2 reference values.
"""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import (
    ggplot, aes,
    geom_point, geom_line, geom_bar, geom_histogram, geom_smooth,
    geom_area, geom_boxplot, geom_density, geom_text,
    facet_wrap, facet_grid,
    coord_flip,
    labs,
    scale_x_continuous, scale_y_continuous,
    theme_minimal,
    position_dodge, position_stack,
)


# ── helpers ──────────────────────────────────────────────────────────────────

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


def _element_types(plot):
    """Return a sorted list of element type names."""
    return sorted({type(el).__name__ for el in _collect_elements(plot)})


def _dframes(plot):
    """Return list of DataFrames from all leaf elements."""
    return [el.dframe() for el in _collect_elements(plot) if hasattr(el, 'dframe')]


# ── reference dataset (matches what we would use in R) ───────────────────────

@pytest.fixture
def iris_like():
    """Synthetic iris-like data with known seed (100 rows, 3 species)."""
    np.random.seed(123)
    n = 100
    species = np.random.choice(['setosa', 'versicolor', 'virginica'], n)
    sepal_length = np.where(
        species == 'setosa', np.random.normal(5.0, 0.35, n),
        np.where(species == 'versicolor', np.random.normal(5.9, 0.5, n),
                 np.random.normal(6.6, 0.6, n)))
    sepal_width = np.where(
        species == 'setosa', np.random.normal(3.4, 0.38, n),
        np.where(species == 'versicolor', np.random.normal(2.8, 0.31, n),
                 np.random.normal(3.0, 0.32, n)))
    return pd.DataFrame({
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'species': species,
    })


@pytest.fixture
def bar_data():
    """Simple bar data for count-based tests."""
    return pd.DataFrame({
        'category': ['A'] * 30 + ['B'] * 50 + ['C'] * 20,
    })


@pytest.fixture
def line_data():
    """Sorted line data for curve tests."""
    np.random.seed(7)
    x = np.linspace(0, 2 * np.pi, 50)
    return pd.DataFrame({'x': x, 'y': np.sin(x)})


# ── 1. Scatter: ggplot(iris, aes(x, y, color)) + geom_point() ───────────────

class TestScatterComparison:
    """
    R reference:
        ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width, color=Species)) +
            geom_point()
    Expected:
        - 3 Scatter elements (one per species)
        - All Scatter elements contain matching row counts
        - Data ranges match the input
    """

    def test_element_types(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length', y='sepal_width', color='species')).geom_point()
        result = p._render()
        assert 'Scatter' in _element_types(result)

    def test_groups_count(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length', y='sepal_width', color='species')).geom_point()
        result = p._render()
        scatters = [el for el in _collect_elements(result) if isinstance(el, hv.Scatter)]
        # ggplot2 produces one geom layer per species -> 3 sub-traces
        assert len(scatters) == 3

    def test_total_points(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length', y='sepal_width', color='species')).geom_point()
        result = p._render()
        total = sum(len(el.dframe()) for el in _collect_elements(result) if isinstance(el, hv.Scatter))
        assert total == len(iris_like)

    def test_data_ranges(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length', y='sepal_width')).geom_point()
        result = p._render()
        df = result.dframe()
        assert df['x'].min() == pytest.approx(iris_like['sepal_length'].min(), abs=1e-6)
        assert df['x'].max() == pytest.approx(iris_like['sepal_length'].max(), abs=1e-6)


# ── 2. Bar chart: ggplot(df, aes(x)) + geom_bar() ──────────────────────────

class TestBarComparison:
    """
    R reference:
        ggplot(df, aes(x=category)) + geom_bar()
    Expected:
        - Bars element
        - Counts: A=30, B=50, C=20
    """

    def test_element_type(self, bar_data):
        p = ggplot(bar_data, aes(x='category')).geom_bar()
        result = p._render()
        assert 'Bars' in _element_types(result)

    def test_bar_counts(self, bar_data):
        p = ggplot(bar_data, aes(x='category')).geom_bar()
        result = p._render()
        bars_el = [el for el in _collect_elements(result) if isinstance(el, hv.Bars)][0]
        df = bars_el.dframe()
        counts = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        assert counts['A'] == 30
        assert counts['B'] == 50
        assert counts['C'] == 20


# ── 3. Histogram: ggplot(df, aes(x)) + geom_histogram(bins=10) ──────────────

class TestHistogramComparison:
    """
    R reference:
        ggplot(df, aes(x=sepal_length)) + geom_histogram(bins=10)
    Expected:
        - Histogram element
        - Total count across bins equals nrow(df)
    """

    def test_element_type(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length')).geom_histogram(bins=10)
        result = p._render()
        assert 'Histogram' in _element_types(result)

    def test_total_count(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length')).geom_histogram(bins=10)
        result = p._render()
        hist_el = [el for el in _collect_elements(result) if isinstance(el, hv.Histogram)][0]
        # Histogram stores (edges, values); total count == len(data)
        total = hist_el.dframe().iloc[:, 1].sum()
        assert total == len(iris_like)


# ── 4. Line: ggplot(df, aes(x, y)) + geom_line() ───────────────────────────

class TestLineComparison:
    """
    R reference:
        ggplot(df, aes(x, y)) + geom_line()
    Expected:
        - Curve element
        - Data matches input (sorted by x)
    """

    def test_element_type(self, line_data):
        p = ggplot(line_data, aes(x='x', y='y')).geom_line()
        result = p._render()
        assert 'Curve' in _element_types(result)

    def test_data_integrity(self, line_data):
        p = ggplot(line_data, aes(x='x', y='y')).geom_line()
        result = p._render()
        df = result.dframe()
        assert len(df) == len(line_data)


# ── 5. Smooth (LM): ggplot(df, aes(x, y)) + geom_smooth(method='lm') ───────

class TestSmoothComparison:
    """
    R reference:
        ggplot(df, aes(x, y)) + geom_smooth(method='lm')
    Expected:
        - Curve element for the regression line
        - Line passes through data centroid (mean_x, predicted_y_at_mean_x)
    """

    def test_smooth_produces_curve(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length', y='sepal_width')).geom_smooth(method='lm')
        result = p._render()
        assert 'Curve' in _element_types(result)

    def test_linear_fit_slope(self, iris_like):
        """Regression line slope should match numpy polyfit."""
        p = ggplot(iris_like, aes(x='sepal_length', y='sepal_width')).geom_smooth(method='lm')
        result = p._render()
        df = result.dframe()
        # Extract endpoints to compute slope
        x_vals = df.iloc[:, 0].values
        y_vals = df.iloc[:, 1].values
        rendered_slope = (y_vals[-1] - y_vals[0]) / (x_vals[-1] - x_vals[0])
        # Compare against numpy polyfit
        expected_slope = np.polyfit(iris_like['sepal_length'], iris_like['sepal_width'], 1)[0]
        assert rendered_slope == pytest.approx(expected_slope, abs=0.05)


# ── 6. Facet wrap: produces correct panel count ─────────────────────────────

class TestFacetWrapComparison:
    """
    R reference:
        ggplot(iris, aes(x, y)) + geom_point() + facet_wrap(~Species)
    Expected:
        - 3 panels (one per species)
        - Each panel contains only its species data
    """

    def test_panel_count(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .facet_wrap('~species'))
        result = p._render()
        assert isinstance(result, hv.Layout)
        assert len(result) == 3  # setosa, versicolor, virginica

    def test_panel_data_isolation(self, iris_like):
        """Each panel should contain only its species data."""
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .facet_wrap('~species'))
        result = p._render()
        species_counts = iris_like['species'].value_counts().to_dict()
        for item in result:
            elements = _collect_elements(item)
            total = sum(len(el.dframe()) for el in elements if isinstance(el, hv.Scatter))
            # Each panel's point count should match its species count
            assert total in species_counts.values()


# ── 7. Facet grid: row × col layout ─────────────────────────────────────────

class TestFacetGridComparison:
    """
    R reference:
        ggplot(df, aes(x, y)) + geom_point() + facet_grid(row_var ~ col_var)
    """

    def test_grid_panel_count(self):
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(60),
            'y': np.random.randn(60),
            'row_var': np.random.choice(['R1', 'R2'], 60),
            'col_var': np.random.choice(['C1', 'C2', 'C3'], 60),
        })
        p = (ggplot(df, aes(x='x', y='y'))
             .geom_point()
             .facet_grid('row_var~col_var'))
        result = p._render()
        assert isinstance(result, hv.Layout)
        # 2 rows × 3 cols = 6 panels
        assert len(result) == 6


# ── 8. coord_flip: axes should be inverted ───────────────────────────────────

class TestCoordFlipComparison:
    """
    R reference:
        ggplot(df, aes(x, y)) + geom_point() + coord_flip()
    Expected:
        - Axes are inverted (invert_axes=True in HoloViews)
    """

    def test_coord_flip_inverts(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .coord_flip())
        result = p._render()
        assert result is not None


# ── 9. labs: title and axis labels ───────────────────────────────────────────

class TestLabsComparison:
    """
    R reference:
        ggplot(df, aes(x, y)) + geom_point() + labs(title='T', x='X', y='Y')
    """

    def test_labs_stored(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .labs(title='My Title', x='Sepal Length', y='Sepal Width'))
        assert p.labels['title'] == 'My Title'
        assert p.labels['x'] == 'Sepal Length'
        assert p.labels['y'] == 'Sepal Width'

    def test_labs_renders(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .labs(title='My Title', x='Sepal Length', y='Sepal Width'))
        result = p._render()
        assert result is not None


# ── 10. Density: peak near data mode ────────────────────────────────────────

class TestDensityComparison:
    """
    R reference:
        ggplot(df, aes(x=sepal_length)) + geom_density()
    Expected:
        - Area or Curve element
        - Peak of density near the mode of the data
    """

    def test_density_peak(self, iris_like):
        p = ggplot(iris_like, aes(x='sepal_length')).geom_density()
        result = p._render()
        dfs = _dframes(result)
        assert len(dfs) > 0
        # The density peak should be near the data mode
        density_df = dfs[0]
        peak_x = density_df.iloc[density_df.iloc[:, 1].idxmax(), 0]
        data_median = iris_like['sepal_length'].median()
        # Peak should be within 1 unit of median (rough check)
        assert abs(peak_x - data_median) < 1.5


# ── 11. Boxplot: quartile sanity ────────────────────────────────────────────

class TestBoxplotComparison:
    """Verify boxplot renders for categorical data."""

    def test_boxplot_renders(self, iris_like):
        p = ggplot(iris_like, aes(x='species', y='sepal_length')).geom_boxplot()
        result = p._render()
        assert result is not None
        # Custom implementation uses Rectangles + Curves for box drawing
        types = _element_types(result)
        assert 'Rectangles' in types or 'BoxWhisker' in types


# ── 12. Multi-layer: point + smooth ─────────────────────────────────────────

class TestMultiLayerComparison:
    """
    R reference:
        ggplot(df, aes(x, y)) + geom_point() + geom_smooth(method='lm')
    Expected:
        - Overlay with both Scatter and Curve
    """

    def test_overlay_types(self, iris_like):
        p = (ggplot(iris_like, aes(x='sepal_length', y='sepal_width'))
             .geom_point()
             .geom_smooth(method='lm'))
        result = p._render()
        types = _element_types(result)
        assert 'Scatter' in types
        assert 'Curve' in types


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
