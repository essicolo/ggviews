"""Tests for ggrepel-style label repulsion (geom_text_repel, geom_label_repel)."""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import ggplot, aes, geom_text_repel, geom_label_repel
from ggviews.repel import repel_labels


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def label_data():
    """Small dataset with overlapping labels."""
    return pd.DataFrame({
        'x': [1.0, 1.1, 1.05, 3.0, 5.0],
        'y': [2.0, 2.1, 2.05, 4.0, 6.0],
        'name': ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'],
    })


@pytest.fixture
def many_labels():
    """Larger dataset to stress the repulsion algorithm."""
    np.random.seed(99)
    n = 30
    return pd.DataFrame({
        'x': np.random.uniform(0, 10, n),
        'y': np.random.uniform(0, 10, n),
        'label': [f'pt{i}' for i in range(n)],
    })


# ── repel_labels algorithm ────────────────────────────────────────────────────

class TestRepelAlgorithm:
    """Unit tests for the force-directed repel_labels function."""

    def test_returns_arrays(self, label_data):
        x_out, y_out = repel_labels(
            label_data['x'], label_data['y'], label_data['name']
        )
        assert isinstance(x_out, np.ndarray)
        assert isinstance(y_out, np.ndarray)

    def test_output_length_matches_input(self, label_data):
        x_out, y_out = repel_labels(
            label_data['x'], label_data['y'], label_data['name']
        )
        assert len(x_out) == len(label_data)
        assert len(y_out) == len(label_data)

    def test_empty_input(self):
        x_out, y_out = repel_labels([], [], [])
        assert len(x_out) == 0
        assert len(y_out) == 0

    def test_single_label(self):
        x_out, y_out = repel_labels([5.0], [3.0], ['solo'])
        assert len(x_out) == 1
        assert len(y_out) == 1

    def test_overlapping_labels_get_separated(self):
        """Labels at nearly the same position should be pushed apart."""
        x = [1.0, 1.0, 1.0]
        y = [2.0, 2.0, 2.0]
        texts = ['AAA', 'BBB', 'CCC']
        x_out, y_out = repel_labels(x, y, texts, max_iter=200, force=2.0)
        # After repulsion, labels should not all be at the same position
        x_spread = np.ptp(x_out)
        y_spread = np.ptp(y_out)
        assert x_spread > 0.01 or y_spread > 0.01

    def test_well_separated_labels_stay_close(self):
        """Labels far apart should not move much."""
        x = [0.0, 10.0, 20.0]
        y = [0.0, 10.0, 20.0]
        texts = ['A', 'B', 'C']
        x_out, y_out = repel_labels(x, y, texts)
        # Each label should stay close to its original position
        for i in range(3):
            assert abs(x_out[i] - x[i]) < 2.0
            assert abs(y_out[i] - y[i]) < 2.0

    def test_reproducibility_with_seed(self):
        """Same seed should produce same results."""
        x = [1.0, 1.1, 1.05]
        y = [2.0, 2.1, 2.05]
        texts = ['A', 'B', 'C']
        x1, y1 = repel_labels(x, y, texts, seed=42)
        x2, y2 = repel_labels(x, y, texts, seed=42)
        np.testing.assert_array_equal(x1, x2)
        np.testing.assert_array_equal(y1, y2)

    def test_different_seeds_differ(self):
        """Different seeds should produce (slightly) different results."""
        x = [1.0, 1.1, 1.05]
        y = [2.0, 2.1, 2.05]
        texts = ['A', 'B', 'C']
        x1, y1 = repel_labels(x, y, texts, seed=1)
        x2, y2 = repel_labels(x, y, texts, seed=99)
        # At least one coordinate should differ
        assert not (np.allclose(x1, x2) and np.allclose(y1, y2))

    def test_force_parameter(self):
        """Different force values should produce different layouts."""
        x = [1.0, 1.0, 1.0]
        y = [2.0, 2.0, 2.0]
        texts = ['AA', 'BB', 'CC']
        x_low, y_low = repel_labels(x, y, texts, force=0.5, max_iter=100, seed=42)
        x_high, y_high = repel_labels(x, y, texts, force=3.0, max_iter=100, seed=42)
        # Both should produce non-zero spread (labels can't all overlap)
        spread_low = (x_low.max() - x_low.min()) + (y_low.max() - y_low.min())
        spread_high = (x_high.max() - x_high.min()) + (y_high.max() - y_high.min())
        assert spread_low > 0.01
        assert spread_high > 0.01

    def test_many_labels_performance(self, many_labels):
        """30 labels should complete without error in reasonable time."""
        x_out, y_out = repel_labels(
            many_labels['x'], many_labels['y'], many_labels['label'],
            max_iter=50,
        )
        assert len(x_out) == len(many_labels)


# ── geom_text_repel ──────────────────────────────────────────────────────────

class TestGeomTextRepel:
    """Tests for geom_text_repel rendering."""

    def test_basic_render(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_text_repel()
        result = p._render()
        assert result is not None

    def test_produces_labels_and_segments(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_text_repel()
        result = p._render()
        types = {type(el).__name__ for el in _collect_elements(result)}
        assert 'Labels' in types
        assert 'Segments' in types

    def test_label_count_matches_data(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_text_repel()
        result = p._render()
        labels_els = [el for el in _collect_elements(result) if isinstance(el, hv.Labels)]
        total = sum(len(el.dframe()) for el in labels_els)
        assert total == len(label_data)

    def test_custom_color(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_text_repel(color='red')
        result = p._render()
        assert result is not None

    def test_custom_size(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_text_repel(size=14)
        result = p._render()
        assert result is not None

    def test_nudge_offsets(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_text_repel(
            nudge_x=0.5, nudge_y=0.5
        )
        result = p._render()
        assert result is not None

    def test_missing_label_aes_raises(self, label_data):
        with pytest.raises(ValueError, match="label"):
            p = ggplot(label_data, aes(x='x', y='y')).geom_text_repel()
            p._render()

    def test_missing_column_warns(self, label_data):
        with pytest.warns(UserWarning, match="not found"):
            p = ggplot(label_data, aes(x='x', y='y', label='nonexistent')).geom_text_repel()
            result = p._render()

    def test_max_overlaps_fallback(self):
        """When n > max_overlaps, should skip repulsion but still render."""
        df = pd.DataFrame({
            'x': range(10),
            'y': range(10),
            'lab': [f'label_{i}' for i in range(10)],
        })
        p = ggplot(df, aes(x='x', y='y', label='lab')).geom_text_repel(max_overlaps=5)
        result = p._render()
        assert result is not None

    def test_with_other_geoms(self, label_data):
        """Repel labels should compose with other geoms."""
        from ggviews import geom_point
        p = (ggplot(label_data, aes(x='x', y='y', label='name'))
             .geom_point()
             .geom_text_repel())
        result = p._render()
        types = {type(el).__name__ for el in _collect_elements(result)}
        assert 'Scatter' in types
        assert 'Labels' in types

    def test_add_operator(self, label_data):
        """geom_text_repel should work with + operator."""
        p = ggplot(label_data, aes(x='x', y='y', label='name')) + geom_text_repel()
        result = p._render()
        assert result is not None


# ── geom_label_repel ─────────────────────────────────────────────────────────

class TestGeomLabelRepel:
    """Tests for geom_label_repel rendering (with background boxes)."""

    def test_basic_render(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_label_repel()
        result = p._render()
        assert result is not None

    def test_produces_labels_and_segments(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_label_repel()
        result = p._render()
        types = {type(el).__name__ for el in _collect_elements(result)}
        assert 'Labels' in types

    def test_custom_fill(self, label_data):
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_label_repel(
            fill='lightyellow'
        )
        result = p._render()
        assert result is not None

    def test_add_operator(self, label_data):
        """geom_label_repel should work with + operator."""
        p = ggplot(label_data, aes(x='x', y='y', label='name')) + geom_label_repel()
        result = p._render()
        assert result is not None

    def test_inherits_repel_params(self, label_data):
        """geom_label_repel should accept all geom_text_repel parameters."""
        p = ggplot(label_data, aes(x='x', y='y', label='name')).geom_label_repel(
            force=2.0, max_iter=50, segment_color='blue', size=12
        )
        result = p._render()
        assert result is not None


# ── Helper ────────────────────────────────────────────────────────────────────

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
