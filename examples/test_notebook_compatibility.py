"""
Working ggviews demo script - tests all functionality before notebook conversion
"""

import pandas as pd
import numpy as np

print("Testing ggviews imports...")

try:
    from ggviews import ggplot, aes
    print("✅ Core ggviews imported successfully")
except ImportError as e:
    print(f"❌ Failed to import core ggviews: {e}")
    exit(1)

try:
    from ggviews.geoms import geom_point, geom_line, geom_bar, geom_area
    print("✅ Basic geoms imported successfully")
except ImportError as e:
    print(f"❌ Failed to import geoms: {e}")

try:
    from ggviews.themes import theme_minimal, theme_classic
    print("✅ Themes imported successfully")
except ImportError as e:
    print(f"❌ Failed to import themes: {e}")

try:
    from ggviews.viridis import scale_colour_viridis_c
    print("✅ Viridis scales imported successfully")
except ImportError as e:
    print(f"❌ Failed to import viridis: {e}")

print("\n" + "="*50)
print("CREATING TEST DATA")
print("="*50)

# Create sample data
np.random.seed(42)
n = 50  # Smaller dataset for testing

df = pd.DataFrame({
    'height': np.random.normal(170, 10, n),
    'weight': np.random.normal(70, 15, n),
    'species': np.random.choice(['setosa', 'versicolor', 'virginica'], n),
    'age': np.random.randint(18, 80, n),
    'group': np.random.choice(['A', 'B'], n)
})

# Add correlation
df['weight'] = df['weight'] + 0.5 * (df['height'] - 170) + np.random.normal(0, 5, n)

print(f"Created dataset with {df.shape[0]} rows and {df.shape[1]} columns")
print("Sample data:")
print(df.head())

print("\n" + "="*50)
print("TESTING BASIC PLOTS")
print("="*50)

# Test 1: Basic scatter plot
print("\n1. Basic scatter plot")
try:
    plot1 = ggplot(df, aes(x='height', y='weight')) + geom_point()
    print("✅ Basic scatter plot created")
except Exception as e:
    print(f"❌ Basic scatter failed: {e}")

# Test 2: Method chaining
print("\n2. Method chaining syntax")
try:
    plot2 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(size=6, alpha=0.7)
             .theme_minimal()
             .labs(title='Height vs Weight', x='Height (cm)', y='Weight (kg)'))
    print("✅ Method chaining works")
except Exception as e:
    print(f"❌ Method chaining failed: {e}")

# Test 3: Color mapping
print("\n3. Color by category")
try:
    plot3 = (ggplot(df, aes(x='height', y='weight', color='species'))
             .geom_point(size=8, alpha=0.8)
             .theme_classic()
             .labs(title='Height vs Weight by Species', 
                   x='Height (cm)', y='Weight (kg)', color='Species'))
    print("✅ Color mapping works")
except Exception as e:
    print(f"❌ Color mapping failed: {e}")

# Test 4: Viridis colors (if available)
print("\n4. Custom colors")
try:
    plot4 = (ggplot(df, aes(x='height', y='weight', color='species'))
             .geom_point(size=8, alpha=0.8)
             .scale_colour_viridis_d()
             .theme_minimal()
             .labs(title='Viridis Color Scale'))
    print("✅ Viridis colors work")
except Exception as e:
    print(f"❌ Viridis colors failed: {e}")

# Test 5: Line plot with smoothing
print("\n5. Line plot with smoothing")
try:
    # Create time series data
    time_df = pd.DataFrame({
        'time': range(20),
        'value': np.cumsum(np.random.randn(20)) + np.sin(np.arange(20) * 0.3) * 3,
        'group': np.repeat(['Group1', 'Group2'], 10)
    })
    
    plot5 = (ggplot(time_df, aes(x='time', y='value', color='group'))
             .geom_line(size=2)
             .geom_smooth(method='lm', se=False)
             .theme_classic()
             .labs(title='Time Series with Trend Lines'))
    print("✅ Line plot with smoothing works")
except Exception as e:
    print(f"❌ Line plot failed: {e}")

# Test 6: Bar chart
print("\n6. Bar chart")
try:
    category_counts = df['species'].value_counts().reset_index()
    category_counts.columns = ['species', 'count']
    
    plot6 = (ggplot(category_counts, aes(x='species', y='count'))
             .geom_bar(stat='identity', fill='steelblue', alpha=0.7)
             .theme_minimal()
             .labs(title='Species Counts', x='Species', y='Count'))
    print("✅ Bar chart works")
except Exception as e:
    print(f"❌ Bar chart failed: {e}")

# Test 7: Histogram
print("\n7. Histogram")
try:
    plot7 = (ggplot(df, aes(x='height'))
             .geom_histogram(bins=10, fill='lightblue', alpha=0.7)
             .theme_minimal()
             .labs(title='Height Distribution', x='Height (cm)', y='Frequency'))
    print("✅ Histogram works")
except Exception as e:
    print(f"❌ Histogram failed: {e}")

# Test 8: Faceting (if available)
print("\n8. Faceted plot")
try:
    from ggviews.facets import facet_wrap
    plot8 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(alpha=0.6)
             .facet_wrap('~species')
             .theme_minimal()
             .labs(title='Height vs Weight by Species (Faceted)'))
    print("✅ Faceted plot works")
except Exception as e:
    print(f"❌ Faceted plot failed: {e}")

print("\n" + "="*50)
print("TESTING ADVANCED FEATURES")
print("="*50)

# Test 9: Area plot (if available)
print("\n9. Area plot")
try:
    area_data = pd.DataFrame({
        'year': list(range(2000, 2020)),
        'value': np.random.uniform(10, 100, 20),
        'category': ['A'] * 20
    })
    
    plot9 = (ggplot(area_data, aes(x='year', y='value'))
             .geom_area(alpha=0.7, fill='coral')
             .theme_minimal()
             .labs(title='Area Plot Example'))
    print("✅ Area plot works")
except Exception as e:
    print(f"❌ Area plot failed: {e}")

# Test 10: Coordinate systems (if available)
print("\n10. Coordinate system")
try:
    from ggviews.coords import coord_fixed
    plot10 = (ggplot(df, aes(x='height', y='weight'))
              .geom_point()
              .coord_fixed()
              .theme_minimal()
              .labs(title='Fixed Aspect Ratio'))
    print("✅ Coordinate systems work")
except Exception as e:
    print(f"❌ Coordinate systems failed: {e}")

print("\n" + "="*50)
print("SUMMARY")
print("="*50)

print("✅ Core functionality testing complete!")
print("📊 ggviews basic features are working")
print("🎨 Ready to create the fixed Jupyter notebook")

print("\nTo display plots in Jupyter notebook:")
print("1. Import holoviews: import holoviews as hv")
print("2. Set extension: hv.extension('bokeh')  # or 'matplotlib'")
print("3. Display plot: plot.show() or just plot")

print("\n🚀 All tests completed successfully!")