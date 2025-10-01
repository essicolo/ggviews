#!/usr/bin/env python3
"""
Test script to actually render ggviews plots and identify any rendering issues
"""

import pandas as pd
import numpy as np
import holoviews as hv
import traceback
import sys

# Set up holoviews
hv.extension('bokeh', 'matplotlib')

print("Testing ggviews plot rendering...\n")

# Import ggviews
try:
    from ggviews import ggplot, aes
    from ggviews.geoms import geom_point, geom_line, geom_bar, geom_area
    from ggviews.themes import theme_minimal, theme_classic
    from ggviews.viridis import scale_colour_viridis_d
    from ggviews.facets import facet_wrap
    from ggviews.coords import coord_fixed
    print("✅ All imports successful!")
except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Create sample data
np.random.seed(42)
n = 100

df = pd.DataFrame({
    'height': np.random.normal(170, 10, n),
    'weight': np.random.normal(70, 15, n),
    'species': np.random.choice(['setosa', 'versicolor', 'virginica'], n),
    'age': np.random.randint(18, 80, n),
    'group': np.random.choice(['A', 'B'], n)
})

# Add some correlation
df['weight'] = df['weight'] + 0.5 * (df['height'] - 170) + np.random.normal(0, 5, n)

print("Sample data created successfully!")

def test_plot_rendering(test_name, plot_func):
    """Helper function to test plot rendering"""
    print(f"\n{'='*50}")
    print(f"Testing: {test_name}")
    print(f"{'='*50}")
    
    try:
        plot = plot_func()
        
        # Try to render the plot
        rendered = plot._render()
        print(f"✅ {test_name} - Plot created and rendered successfully!")
        print(f"   Plot type: {type(plot)}")
        print(f"   Rendered type: {type(rendered)}")
        print(f"   Layers: {len(plot.layers)}")
        
        # Try to get the representation (what Jupyter would show)
        try:
            repr_result = plot._repr_mimebundle_()
            if repr_result:
                print(f"   Jupyter display: ✅ Available")
            else:
                print(f"   Jupyter display: ❓ Empty result")
        except Exception as e:
            print(f"   Jupyter display: ❌ Error - {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ {test_name} - Error: {e}")
        traceback.print_exc()
        return False

# Test 1: Basic scatter plot
test_plot_rendering(
    "Basic scatter plot", 
    lambda: ggplot(df, aes(x='height', y='weight')) + geom_point()
)

# Test 2: Method chaining with labs
test_plot_rendering(
    "Method chaining with labs",
    lambda: (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(size=6, alpha=0.7)
        .theme_minimal()
        .labs(title='Height vs Weight', x='Height (cm)', y='Weight (kg)')
    )
)

# Test 3: Color mapping
test_plot_rendering(
    "Color mapping",
    lambda: (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .theme_classic()
        .labs(title='Height vs Weight by Species')
    )
)

# Test 4: Viridis scale
test_plot_rendering(
    "Viridis color scale",
    lambda: (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .scale_colour_viridis_d()
        .theme_minimal()
    )
)

# Test 5: Line plot with smoothing
time_df = pd.DataFrame({
    'time': range(30),
    'value': np.cumsum(np.random.randn(30)) + np.sin(np.arange(30) * 0.2) * 5,
    'group': np.tile(['A', 'B'], 15)
})

test_plot_rendering(
    "Line plot with smoothing",
    lambda: (
        ggplot(time_df, aes(x='time', y='value', color='group'))
        .geom_line(size=2)
        .geom_smooth(method='lm', se=False)
        .theme_minimal()
    )
)

# Test 6: Bar chart
species_counts = df['species'].value_counts().reset_index()
species_counts.columns = ['species', 'count']

test_plot_rendering(
    "Bar chart",
    lambda: (
        ggplot(species_counts, aes(x='species', y='count'))
        .geom_bar(stat='identity', fill='steelblue', alpha=0.7)
        .theme_minimal()
    )
)

# Test 7: Histogram
test_plot_rendering(
    "Histogram",
    lambda: (
        ggplot(df, aes(x='height'))
        .geom_histogram(bins=15, fill='lightcoral', alpha=0.7)
        .theme_minimal()
    )
)

# Test 8: Faceted plot
test_plot_rendering(
    "Faceted plot",
    lambda: (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(alpha=0.7, size=4)
        .facet_wrap('~species')
        .theme_minimal()
    )
)

# Test 9: Area plot
area_data = pd.DataFrame({
    'year': list(range(2000, 2020)),
    'population': np.random.uniform(1000, 5000, 20) + np.arange(20) * 100,
    'region': ['North'] * 20
})

test_plot_rendering(
    "Area plot",
    lambda: (
        ggplot(area_data, aes(x='year', y='population'))
        .geom_area(alpha=0.7, fill='lightgreen')
        .theme_minimal()
    )
)

# Test 10: Fixed aspect ratio
test_plot_rendering(
    "Fixed aspect ratio",
    lambda: (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=6, alpha=0.8)
        .coord_fixed()
        .theme_minimal()
    )
)

# Test 11: Complex multi-layer plot
test_plot_rendering(
    "Complex multi-layer plot",
    lambda: (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(aes(color='species', size='age'), alpha=0.7)
        .geom_smooth(method='lm', color='black', alpha=0.3)
        .scale_colour_viridis_d()
        .theme_minimal()
        .labs(
            title='Complex Multi-layer Plot',
            subtitle='Points colored by species, sized by age, with trend line',
            x='Height (cm)',
            y='Weight (kg)',
            color='Species',
            size='Age'
        )
    )
)

print("\n" + "=" * 60)
print("All rendering tests completed!")
print("=" * 60)