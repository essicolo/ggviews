#!/usr/bin/env python3
"""
Test script to validate ggviews_demo.ipynb functionality
"""

import pandas as pd
import numpy as np
import holoviews as hv
import traceback

# Set up holoviews for Jupyter
hv.extension('bokeh')

print("Testing ggviews_demo.ipynb functionality...\n")

# Test 1: Import ggviews
print("=" * 50)
print("Test 1: Import ggviews")
print("=" * 50)
try:
    from ggviews import ggplot, aes
    from ggviews.geoms import geom_point, geom_line, geom_bar, geom_area
    from ggviews.themes import theme_minimal, theme_classic
    from ggviews.viridis import scale_colour_viridis_d
    from ggviews.facets import facet_wrap
    from ggviews.coords import coord_fixed
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()

# Test 2: Create sample data
print("\n" + "=" * 50)
print("Test 2: Create sample data")
print("=" * 50)
try:
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
    
    print("✅ Sample data created successfully!")
    print(f"   Data shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
except Exception as e:
    print(f"❌ Data creation error: {e}")
    traceback.print_exc()

# Test 3: Basic scatter plot
print("\n" + "=" * 50)
print("Test 3: Basic scatter plot")
print("=" * 50)
try:
    plot1 = ggplot(df, aes(x='height', y='weight')) + geom_point()
    print("✅ Basic scatter plot created successfully!")
    print(f"   Plot type: {type(plot1)}")
except Exception as e:
    print(f"❌ Basic scatter plot error: {e}")
    traceback.print_exc()

# Test 4: Method chaining
print("\n" + "=" * 50)
print("Test 4: Method chaining")
print("=" * 50)
try:
    plot2 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(size=6, alpha=0.7)
        .theme_minimal()
        .labs(title='Height vs Weight', x='Height (cm)', y='Weight (kg)')
    )
    print("✅ Method chaining successful!")
except Exception as e:
    print(f"❌ Method chaining error: {e}")
    traceback.print_exc()

# Test 5: Colored by category
print("\n" + "=" * 50)
print("Test 5: Colored by category")
print("=" * 50)
try:
    plot3 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .theme_classic()
        .labs(
            title='Height vs Weight by Species',
            x='Height (cm)', 
            y='Weight (kg)',
            color='Species'
        )
    )
    print("✅ Colored by category successful!")
except Exception as e:
    print(f"❌ Colored by category error: {e}")
    traceback.print_exc()

# Test 6: Viridis color scale
print("\n" + "=" * 50)
print("Test 6: Viridis color scale")
print("=" * 50)
try:
    plot4 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .scale_colour_viridis_d()
        .theme_minimal()
        .labs(title='Viridis Color Palette')
    )
    print("✅ Viridis color scale successful!")
except Exception as e:
    print(f"❌ Viridis color scale error: {e}")
    traceback.print_exc()

# Test 7: Line plot with smoothing
print("\n" + "=" * 50)
print("Test 7: Line plot with smoothing")
print("=" * 50)
try:
    time_df = pd.DataFrame({
        'time': range(30),
        'value': np.cumsum(np.random.randn(30)) + np.sin(np.arange(30) * 0.2) * 5,
        'group': np.tile(['A', 'B'], 15)
    })
    
    plot5 = (
        ggplot(time_df, aes(x='time', y='value', color='group'))
        .geom_line(size=2)
        .geom_smooth(method='lm', se=False)
        .theme_minimal()
        .labs(title='Time Series with Trend Lines')
    )
    print("✅ Line plot with smoothing successful!")
except Exception as e:
    print(f"❌ Line plot with smoothing error: {e}")
    traceback.print_exc()

# Test 8: Bar charts
print("\n" + "=" * 50)
print("Test 8: Bar charts")
print("=" * 50)
try:
    species_counts = df['species'].value_counts().reset_index()
    species_counts.columns = ['species', 'count']
    
    plot6 = (
        ggplot(species_counts, aes(x='species', y='count'))
        .geom_bar(stat='identity', fill='steelblue', alpha=0.7)
        .theme_minimal()
        .labs(
            title='Species Count',
            x='Species',
            y='Count'
        )
    )
    print("✅ Bar chart successful!")
except Exception as e:
    print(f"❌ Bar chart error: {e}")
    traceback.print_exc()

# Test 9: Histograms
print("\n" + "=" * 50)
print("Test 9: Histograms")
print("=" * 50)
try:
    plot7 = (
        ggplot(df, aes(x='height'))
        .geom_histogram(bins=15, fill='lightcoral', alpha=0.7)
        .theme_minimal()
        .labs(
            title='Distribution of Heights',
            x='Height (cm)',
            y='Count'
        )
    )
    print("✅ Histogram successful!")
except Exception as e:
    print(f"❌ Histogram error: {e}")
    traceback.print_exc()

# Test 10: Faceted plots
print("\n" + "=" * 50)
print("Test 10: Faceted plots")
print("=" * 50)
try:
    plot8 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(alpha=0.7, size=4)
        .facet_wrap('~species')
        .theme_minimal()
        .labs(title='Height vs Weight by Species (Faceted)')
    )
    print("✅ Faceted plot successful!")
except Exception as e:
    print(f"❌ Faceted plot error: {e}")
    traceback.print_exc()

# Test 11: Area plots
print("\n" + "=" * 50)
print("Test 11: Area plots")
print("=" * 50)
try:
    area_data = pd.DataFrame({
        'year': list(range(2000, 2020)),
        'population': np.random.uniform(1000, 5000, 20) + np.arange(20) * 100,
        'region': ['North'] * 20
    })
    
    plot9 = (
        ggplot(area_data, aes(x='year', y='population'))
        .geom_area(alpha=0.7, fill='lightgreen')
        .theme_minimal()
        .labs(
            title='Population Growth Over Time',
            x='Year',
            y='Population'
        )
    )
    print("✅ Area plot successful!")
except Exception as e:
    print(f"❌ Area plot error: {e}")
    traceback.print_exc()

# Test 12: Fixed aspect ratio
print("\n" + "=" * 50)
print("Test 12: Fixed aspect ratio")
print("=" * 50)
try:
    plot10 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=6, alpha=0.8)
        .coord_fixed()
        .theme_minimal()
        .labs(title='Fixed Aspect Ratio (1:1)')
    )
    print("✅ Fixed aspect ratio successful!")
except Exception as e:
    print(f"❌ Fixed aspect ratio error: {e}")
    traceback.print_exc()

# Test 13: Complex multi-layer plot
print("\n" + "=" * 50)
print("Test 13: Complex multi-layer plot")
print("=" * 50)
try:
    plot11 = (
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
    print("✅ Complex multi-layer plot successful!")
except Exception as e:
    print(f"❌ Complex multi-layer plot error: {e}")
    traceback.print_exc()

print("\n" + "=" * 50)
print("Testing Complete!")
print("=" * 50)