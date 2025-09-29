"""
Test suite for ggviews

Run with: python -m pytest tests/
"""

import pytest
import pandas as pd
import numpy as np
import holoviews as hv

# Set up holoviews backend for testing
hv.extension('matplotlib', 'bokeh')

# Import ggviews components
from ggviews import ggplot, aes
from ggviews.geoms import (geom_point, geom_line, geom_bar, geom_histogram, 
                          geom_boxplot, geom_smooth, geom_density)
from ggviews.themes import (theme_minimal, theme_classic, theme_bw, theme_dark, theme_void)
from ggviews.scales import (scale_color_manual, scale_color_discrete, scale_color_continuous,
                           scale_x_continuous, scale_y_continuous)
from ggviews.facets import facet_wrap, facet_grid
from ggviews.coords import coord_fixed, coord_equal, coord_flip
from ggviews.utils import labs, xlim, ylim


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    np.random.seed(42)
    n = 100
    
    df = pd.DataFrame({
        'x': np.random.randn(n),
        'y': 2 * np.random.randn(n) + 1,
        'category': np.random.choice(['A', 'B', 'C'], n),
        'continuous': np.random.uniform(0, 10, n),
        'size_var': np.random.uniform(1, 5, n),
        'group': np.random.choice(['Group1', 'Group2'], n)
    })
    
    # Add some correlation
    df['y'] = df['y'] + 0.3 * df['x'] + np.random.normal(0, 0.5, n)
    
    return df


class TestCore:
    """Test core functionality"""
    
    def test_ggplot_creation(self, sample_data):
        """Test ggplot object creation"""
        p = ggplot(sample_data)
        assert p.data is not None
        assert len(p.layers) == 0
        assert p.theme is None
    
    def test_ggplot_with_aes(self, sample_data):
        """Test ggplot with aesthetic mappings"""
        p = ggplot(sample_data, aes(x='x', y='y'))
        assert p.mapping is not None
        assert 'x' in p.mapping.mappings
        assert 'y' in p.mapping.mappings
    
    def test_aes_creation(self):
        """Test aesthetic mapping creation"""
        a = aes(x='height', y='weight', color='species')
        assert a.mappings['x'] == 'height'
        assert a.mappings['y'] == 'weight'
        assert a.mappings['color'] == 'species'
    
    def test_aes_color_colour_alias(self):
        """Test that color and colour are aliases"""
        a1 = aes(color='species')
        a2 = aes(colour='species')
        assert a1.mappings['color'] == a2.mappings['color']
    
    def test_method_chaining(self, sample_data):
        """Test method chaining functionality"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             .geom_point()
             .theme_minimal()
             .labs(title='Test Plot'))
        
        assert len(p.layers) == 1
        assert p.theme is not None
        assert 'title' in p.labels


class TestGeoms:
    """Test geometric objects"""
    
    def test_geom_point(self, sample_data):
        """Test geom_point"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point()
        assert len(p.layers) == 1
        assert p.layers[0].geom_type == 'point'
        
        # Test rendering doesn't throw errors
        try:
            rendered = p._render()
            assert rendered is not None
        except Exception as e:
            pytest.fail(f"geom_point rendering failed: {e}")
    
    def test_geom_point_with_color(self, sample_data):
        """Test geom_point with color aesthetic"""
        p = ggplot(sample_data, aes(x='x', y='y', color='category')) + geom_point()
        
        try:
            rendered = p._render()
            assert rendered is not None
        except Exception as e:
            pytest.fail(f"geom_point with color failed: {e}")
    
    def test_geom_line(self, sample_data):
        """Test geom_line"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_line()
        assert len(p.layers) == 1
        assert p.layers[0].geom_type == 'line'
    
    def test_geom_bar(self, sample_data):
        """Test geom_bar"""
        p = ggplot(sample_data, aes(x='category')) + geom_bar()
        assert len(p.layers) == 1
        assert p.layers[0].geom_type == 'bar'
        assert p.layers[0].stat == 'count'
    
    def test_geom_histogram(self, sample_data):
        """Test geom_histogram"""
        p = ggplot(sample_data, aes(x='x')) + geom_histogram(bins=20)
        assert len(p.layers) == 1
        assert p.layers[0].geom_type == 'histogram'
    
    def test_geom_boxplot(self, sample_data):
        """Test geom_boxplot"""
        p = ggplot(sample_data, aes(x='category', y='y')) + geom_boxplot()
        assert len(p.layers) == 1
        assert p.layers[0].geom_type == 'boxplot'
    
    def test_geom_smooth(self, sample_data):
        """Test geom_smooth"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_smooth()
        assert len(p.layers) == 1
        assert p.layers[0].geom_type == 'smooth'
    
    def test_multiple_layers(self, sample_data):
        """Test multiple geom layers"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + geom_smooth())
        assert len(p.layers) == 2


class TestThemes:
    """Test themes"""
    
    def test_theme_minimal(self, sample_data):
        """Test theme_minimal"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + theme_minimal()
        assert p.theme is not None
        assert hasattr(p.theme, '_apply')
    
    def test_theme_classic(self, sample_data):
        """Test theme_classic"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + theme_classic()
        assert p.theme is not None
    
    def test_theme_bw(self, sample_data):
        """Test theme_bw"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + theme_bw()
        assert p.theme is not None
    
    def test_theme_dark(self, sample_data):
        """Test theme_dark"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + theme_dark()
        assert p.theme is not None
    
    def test_theme_void(self, sample_data):
        """Test theme_void"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + theme_void()
        assert p.theme is not None


class TestScales:
    """Test scales"""
    
    def test_scale_color_manual(self, sample_data):
        """Test scale_color_manual"""
        colors = ['red', 'blue', 'green']
        p = (ggplot(sample_data, aes(x='x', y='y', color='category'))
             + geom_point()
             + scale_color_manual(values=colors))
        
        assert 'color' in p.scales
        assert p.scales['color'].values == colors
    
    def test_scale_color_discrete(self, sample_data):
        """Test scale_color_discrete"""
        p = (ggplot(sample_data, aes(x='x', y='y', color='category'))
             + geom_point()
             + scale_color_discrete())
        
        assert 'color' in p.scales
    
    def test_scale_color_continuous(self, sample_data):
        """Test scale_color_continuous"""
        p = (ggplot(sample_data, aes(x='x', y='y', color='continuous'))
             + geom_point()
             + scale_color_continuous(low='blue', high='red'))
        
        assert 'color' in p.scales
        assert p.scales['color'].low == 'blue'
        assert p.scales['color'].high == 'red'
    
    def test_scale_x_continuous(self, sample_data):
        """Test scale_x_continuous"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_x_continuous(name='X Variable', limits=[-2, 2]))
        
        assert 'x' in p.scales
        assert p.scales['x'].name == 'X Variable'
        assert p.scales['x'].limits == [-2, 2]
    
    def test_scale_y_continuous(self, sample_data):
        """Test scale_y_continuous"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_y_continuous(name='Y Variable'))
        
        assert 'y' in p.scales
        assert p.scales['y'].name == 'Y Variable'


class TestFacets:
    """Test faceting"""
    
    def test_facet_wrap(self, sample_data):
        """Test facet_wrap"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('~category'))
        
        assert p.facets is not None
        assert 'category' in p.facets.facet_vars
    
    def test_facet_wrap_with_ncol(self, sample_data):
        """Test facet_wrap with ncol parameter"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('~category', ncol=2))
        
        assert p.facets is not None
        assert p.facets.ncol == 2
    
    def test_facet_grid(self, sample_data):
        """Test facet_grid"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_grid('group ~ category'))
        
        assert p.facets is not None
        assert p.facets.row_var == 'group'
        assert p.facets.col_var == 'category'
    
    def test_facet_grid_row_only(self, sample_data):
        """Test facet_grid with row variable only"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_grid('group ~ .'))
        
        assert p.facets is not None
        assert p.facets.row_var == 'group'
        assert p.facets.col_var == '.'
    
    def test_facet_grid_col_only(self, sample_data):
        """Test facet_grid with column variable only"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_grid('. ~ category'))
        
        assert p.facets is not None
        assert p.facets.row_var == '.'
        assert p.facets.col_var == 'category'


class TestUtils:
    """Test utility functions"""
    
    def test_labs(self, sample_data):
        """Test labs function"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + labs(title='Test Title', x='X Label', y='Y Label'))
        
        assert 'title' in p.labels
        assert 'x' in p.labels
        assert 'y' in p.labels
        assert p.labels['title'] == 'Test Title'
    
    def test_xlim(self, sample_data):
        """Test xlim function"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + xlim(-2, 2))
        
        assert 'x' in p.limits
        assert p.limits['x'] == (-2, 2)
    
    def test_ylim(self, sample_data):
        """Test ylim function"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + ylim(-3, 3))
        
        assert 'y' in p.limits
        assert p.limits['y'] == (-3, 3)
    
    def test_xlim_single_arg(self, sample_data):
        """Test xlim with single tuple argument"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + xlim((-2, 2)))
        
        assert 'x' in p.limits
        assert p.limits['x'] == (-2, 2)


class TestMethodChaining:
    """Test method chaining specifically"""
    
    def test_chaining_geom_point(self, sample_data):
        """Test chaining geom_point method"""
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point()
        assert len(p.layers) == 1
        assert p.layers[0].geom_type == 'point'
    
    def test_chaining_themes(self, sample_data):
        """Test chaining theme methods"""
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().theme_minimal()
        assert p.theme is not None
    
    def test_chaining_scales(self, sample_data):
        """Test chaining scale methods"""
        p = (ggplot(sample_data, aes(x='x', y='y', color='category'))
             .geom_point()
             .scale_color_manual(values=['red', 'blue', 'green']))
        
        assert 'color' in p.scales
    
    def test_chaining_facets(self, sample_data):
        """Test chaining facet methods"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             .geom_point()
             .facet_wrap('~category'))
        
        assert p.facets is not None
    
    def test_complex_chaining(self, sample_data):
        """Test complex method chaining"""
        p = (ggplot(sample_data, aes(x='x', y='y', color='category'))
             .geom_point(size=4, alpha=0.7)
             .geom_smooth(method='lm')
             .scale_color_manual(values=['#FF6B6B', '#4ECDC4', '#45B7D1'])
             .theme_minimal()
             .facet_wrap('~group')
             .labs(title='Complex Plot', x='X Variable', y='Y Variable')
             .xlim(-3, 3)
             .ylim(-5, 5))
        
        assert len(p.layers) == 2
        assert p.theme is not None
        assert 'color' in p.scales
        assert p.facets is not None
        assert 'title' in p.labels
        assert 'x' in p.limits
        assert 'y' in p.limits


class TestRendering:
    """Test plot rendering"""
    
    def test_basic_rendering(self, sample_data):
        """Test basic plot rendering"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point()
        
        try:
            rendered = p._render()
            assert rendered is not None
        except Exception as e:
            pytest.fail(f"Basic rendering failed: {e}")
    
    def test_empty_plot_rendering(self, sample_data):
        """Test rendering empty plot"""
        p = ggplot(sample_data, aes(x='x', y='y'))
        
        try:
            rendered = p._render()
            assert rendered is not None
        except Exception as e:
            pytest.fail(f"Empty plot rendering failed: {e}")
    
    def test_show_method(self, sample_data):
        """Test show method"""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point()
        
        try:
            result = p.show()
            assert result is not None
        except Exception as e:
            pytest.fail(f"Show method failed: {e}")


class TestErrorHandling:
    """Test error handling"""
    
    def test_missing_data_columns(self, sample_data):
        """Test handling of missing data columns"""
        # This should not raise an error but might show warnings
        p = ggplot(sample_data, aes(x='nonexistent', y='y')) + geom_point()
        
        try:
            rendered = p._render()
            # Should handle gracefully (might return None or empty plot)
        except Exception as e:
            # Should not raise unhandled exceptions
            pass
    
    def test_invalid_data_type(self):
        """Test handling of invalid data types"""
        with pytest.raises(ValueError):
            ggplot("not_a_dataframe")
    
    def test_geom_without_required_aesthetics(self, sample_data):
        """Test geom without required aesthetics"""
        p = ggplot(sample_data) + geom_point()  # No x, y aesthetics
        
        try:
            rendered = p._render()
            # Should handle gracefully or raise appropriate error
        except ValueError:
            # Expected behavior for missing required aesthetics
            pass
        except Exception as e:
            pytest.fail(f"Unexpected error type: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])