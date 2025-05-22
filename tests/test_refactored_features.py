"""
Test refactored features of ggviews.

This module tests the refactored features of ggviews to ensure they work correctly.
"""
import pytest
import pandas as pd
import numpy as np
import holoviews as hv

from ggviews import (
    ggplot, 
    aes, 
    load_dataset,
    geom_point,
    geom_line,
    geom_bar,
    geom_histogram,
    geom_boxplot,
    geom_violin,
    geom_density,
    scale_x_log10,
    scale_y_log10,
    scale_color_continuous,
    scale_fill_continuous,
    scale_color_discrete,
    scale_fill_discrete,
    theme_default,
    theme_minimal,
    theme_bw,
    facet_grid,
    facet_wrap,
    coord_flip
)


def test_basic_plot():
    """Test basic plot creation."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25],
        'group': ['A', 'B', 'C', 'D', 'E']
    })
    
    # Create a basic plot
    plot = ggplot(data, aes(x='x', y='y'))
    
    # Check that the plot is a GGPlot object
    assert plot.__class__.__name__ == 'GGPlot'
    
    # Check that the data is stored correctly
    assert plot.data is data
    
    # Check that the aesthetics are stored correctly
    assert plot.mapping['x'] == 'x'
    assert plot.mapping['y'] == 'y'


def test_geom_point():
    """Test point geometry."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25],
        'group': ['A', 'B', 'C', 'D', 'E']
    })
    
    # Create a plot with points
    plot = ggplot(data, aes(x='x', y='y')) + geom_point()
    
    # Check that the plot has a layer
    assert len(plot.layers) == 1
    
    # Check that the layer is a GeomPoint
    assert plot.layers[0].__class__.__name__ == 'GeomPoint'


def test_geom_line():
    """Test line geometry."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25],
        'group': ['A', 'B', 'C', 'D', 'E']
    })
    
    # Create a plot with lines
    plot = ggplot(data, aes(x='x', y='y')) + geom_line()
    
    # Check that the plot has a layer
    assert len(plot.layers) == 1
    
    # Check that the layer is a GeomLine
    assert plot.layers[0].__class__.__name__ == 'GeomLine'


def test_geom_bar():
    """Test bar geometry."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': ['A', 'B', 'C', 'D', 'E'],
        'y': [1, 4, 9, 16, 25]
    })
    
    # Create a plot with bars
    plot = ggplot(data, aes(x='x', y='y')) + geom_bar(stat='identity')
    
    # Check that the plot has a layer
    assert len(plot.layers) == 1
    
    # Check that the layer is a GeomBar
    assert plot.layers[0].__class__.__name__ == 'GeomBar'


def test_geom_histogram():
    """Test histogram geometry."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': np.random.normal(0, 1, 100)
    })
    
    # Create a plot with histogram
    plot = ggplot(data, aes(x='x')) + geom_histogram()
    
    # Check that the plot has a layer
    assert len(plot.layers) == 1
    
    # Check that the layer is a GeomHistogram
    assert plot.layers[0].__class__.__name__ == 'GeomHistogram'


def test_geom_boxplot():
    """Test boxplot geometry."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
        'y': [1, 2, 3, 4, 5, 6, 7, 8, 9]
    })
    
    # Create a plot with boxplot
    plot = ggplot(data, aes(x='x', y='y')) + geom_boxplot()
    
    # Check that the plot has a layer
    assert len(plot.layers) == 1
    
    # Check that the layer is a GeomBoxplot
    assert plot.layers[0].__class__.__name__ == 'GeomBoxplot'


def test_geom_violin():
    """Test violin geometry."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
        'y': [1, 2, 3, 4, 5, 6, 7, 8, 9]
    })
    
    # Create a plot with violin
    plot = ggplot(data, aes(x='x', y='y')) + geom_violin()
    
    # Check that the plot has a layer
    assert len(plot.layers) == 1
    
    # Check that the layer is a GeomViolin
    assert plot.layers[0].__class__.__name__ == 'GeomViolin'


def test_geom_density():
    """Test density geometry."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': np.random.normal(0, 1, 100)
    })
    
    # Create a plot with density
    plot = ggplot(data, aes(x='x')) + geom_density()
    
    # Check that the plot has a layer
    assert len(plot.layers) == 1
    
    # Check that the layer is a GeomDensity
    assert plot.layers[0].__class__.__name__ == 'GeomDensity'


def test_scale_log():
    """Test log scales."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25]
    })
    
    # Create a plot with log scales
    plot = (ggplot(data, aes(x='x', y='y'))
            + geom_point()
            + scale_x_log10()
            + scale_y_log10())
    
    # Check that the plot has scales
    assert len(plot.scales) == 2


def test_scale_color():
    """Test color scales."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25],
        'z': [10, 20, 30, 40, 50],
        'group': ['A', 'B', 'C', 'D', 'E']
    })
    
    # Create a plot with continuous color scale
    plot1 = (ggplot(data, aes(x='x', y='y', color='z'))
             + geom_point()
             + scale_color_continuous())
    
    # Check that the plot has a scale
    assert len(plot1.scales) == 1
    
    # Create a plot with discrete color scale
    plot2 = (ggplot(data, aes(x='x', y='y', color='group'))
             + geom_point()
             + scale_color_discrete())
    
    # Check that the plot has a scale
    assert len(plot2.scales) == 1


def test_scale_fill():
    """Test fill scales."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25],
        'z': [10, 20, 30, 40, 50],
        'group': ['A', 'B', 'C', 'D', 'E']
    })
    
    # Create a plot with continuous fill scale
    plot1 = (ggplot(data, aes(x='x', y='y', fill='z'))
             + geom_point()
             + scale_fill_continuous())
    
    # Check that the plot has a scale
    assert len(plot1.scales) == 1
    
    # Create a plot with discrete fill scale
    plot2 = (ggplot(data, aes(x='x', y='y', fill='group'))
             + geom_point()
             + scale_fill_discrete())
    
    # Check that the plot has a scale
    assert len(plot2.scales) == 1


def test_themes():
    """Test themes."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25]
    })
    
    # Create plots with different themes
    plot1 = (ggplot(data, aes(x='x', y='y'))
             + geom_point()
             + theme_default())
    
    plot2 = (ggplot(data, aes(x='x', y='y'))
             + geom_point()
             + theme_minimal())
    
    plot3 = (ggplot(data, aes(x='x', y='y'))
             + geom_point()
             + theme_bw())
    
    # Check that the plots have themes
    assert plot1.theme_obj is not None
    assert plot2.theme_obj is not None
    assert plot3.theme_obj is not None


def test_facets():
    """Test facets."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 1, 2, 3],
        'y': [1, 4, 9, 2, 5, 10],
        'row': ['A', 'A', 'A', 'B', 'B', 'B'],
        'col': ['X', 'Y', 'Z', 'X', 'Y', 'Z']
    })
    
    # Create a plot with facet grid
    plot1 = (ggplot(data, aes(x='x', y='y'))
             + geom_point()
             + facet_grid(rows='row', cols='col'))
    
    # Check that the plot has a facet
    assert plot1.facet_obj is not None
    
    # Create a plot with facet wrap
    plot2 = (ggplot(data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('row'))
    
    # Check that the plot has a facet
    assert plot2.facet_obj is not None


def test_coord_flip():
    """Test coordinate flip."""
    # Create a simple dataframe
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25]
    })
    
    # Create a plot with flipped coordinates
    plot = (ggplot(data, aes(x='x', y='y'))
            + geom_point()
            + coord_flip())
    
    # Check that the plot has a coordinate system
    assert plot.coord_obj is not None
    assert plot.coord_obj.__class__.__name__ == 'FlippedCoord'