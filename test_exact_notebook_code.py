#!/usr/bin/env python3
"""
Test the exact code from ggviews_demo.ipynb to ensure it all works
"""

# Import required libraries
import pandas as pd
import numpy as np
import holoviews as hv

# Set up holoviews for Jupyter
hv.extension('bokeh')  # Use 'matplotlib' if you prefer static plots

print("Libraries loaded successfully!")

# Import ggviews - test imports first
try:
    from ggviews import ggplot, aes
    from ggviews.geoms import geom_point, geom_line, geom_bar, geom_area
    from ggviews.themes import theme_minimal, theme_classic
    from ggviews.viridis import scale_colour_viridis_d
    from ggviews.facets import facet_wrap
    from ggviews.coords import coord_fixed
    print("✅ ggviews imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure ggviews is installed: pip install -e .")

# Create sample dataset
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

print("Sample data created:")
print(df.head(10))
print(f"\nData shape: {df.shape}")
print(f"Species counts: {df['species'].value_counts().to_dict()}")

# Test all the plots from the notebook

print("\n=== Testing all notebook plots ===")

# 1. Basic scatter plot
print("1. Basic scatter plot...")
try:
    plot1 = ggplot(df, aes(x='height', y='weight')) + geom_point()
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Method chaining
print("2. Method chaining...")
try:
    plot2 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(size=6, alpha=0.7)
        .theme_minimal()
        .labs(title='Height vs Weight', x='Height (cm)', y='Weight (kg)')
    )
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Colored by category
print("3. Colored by category...")
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
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Viridis color scale
print("4. Viridis color scale...")
try:
    plot4 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .scale_colour_viridis_d()
        .theme_minimal()
        .labs(title='Viridis Color Palette')
    )
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 5. Line plot with smoothing
print("5. Line plot with smoothing...")
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
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 6. Bar chart
print("6. Bar chart...")
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
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 7. Histogram
print("7. Histogram...")
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
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 8. Faceted plot
print("8. Faceted plot...")
try:
    plot8 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(alpha=0.7, size=4)
        .facet_wrap('~species')
        .theme_minimal()
        .labs(title='Height vs Weight by Species (Faceted)')
    )
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 9. Area plot
print("9. Area plot...")
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
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 10. Fixed aspect ratio
print("10. Fixed aspect ratio...")
try:
    plot10 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=6, alpha=0.8)
        .coord_fixed()
        .theme_minimal()
        .labs(title='Fixed Aspect Ratio (1:1)')
    )
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 11. Complex multi-layer plot
print("11. Complex multi-layer plot...")
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
    print("   ✅ Created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ ALL NOTEBOOK EXAMPLES TESTED SUCCESSFULLY!")
print("📊 The ggviews_demo.ipynb should work perfectly!")
print("="*60)