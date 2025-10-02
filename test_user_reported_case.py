#!/usr/bin/env python3
"""
Test the exact user-reported cases to understand the issue
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes
from ggviews.geoms import geom_point

hv.extension('bokeh')

# Create test data matching what user likely has
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 50),
    'weight': np.random.normal(70, 15, 50),
    'species': np.random.choice(['setosa', 'versicolor', 'virginica'], 50),
})

print("Test data:")
print(df.head())
print(f"Columns: {df.columns.tolist()}")
print(f"Species unique values: {df['species'].unique()}")

print("\n" + "="*60)
print("TESTING USER REPORTED CASES")
print("="*60)

# Case 1: User said this works (but shouldn't according to them)
print("\n1. USER CASE 1: This 'works' but user thinks it shouldn't")
print("   (ggplot(df, aes(x='height', y='weight', color='species'))")
print("   .geom_point(color='Species',size=8, alpha=0.8))")

try:
    plot1 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(color='Species', size=8, alpha=0.8)
    )
    
    print("   ✅ Plot created")
    
    # Analyze what's happening
    geom = plot1.layers[0]
    combined_aes = plot1._combine_aesthetics(geom.mapping)
    print(f"   Plot-level aes: {plot1.mapping.mappings}")
    print(f"   Layer-level aes: {geom.mapping}")
    print(f"   Combined aes: {combined_aes.mappings}")
    print(f"   Geom params: {geom.params}")
    
    # The issue: plot-level has color='species' but geom overrides with color='Species'
    # This should work because geom params override aesthetic mappings
    
    rendered = plot1._render()
    print(f"   Rendered successfully: {type(rendered)}")
    
    # User's concern: They think 'Species' shouldn't be interpreted as a column
    # But it's not - it's being used as a fixed color value, overriding the aes mapping
    print("   ANALYSIS: This IS correct behavior!")
    print("   - Plot-level aes maps color to 'species' column")  
    print("   - Geom-level color='Species' overrides with fixed color")
    print("   - All points should be colored with color 'Species' (literal)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Case 2: User said this returns empty plot
print("\n2. USER CASE 2: This 'returns empty plot canvas'")
print("   (ggplot(df, aes(x='height', y='weight', color='species'))")  
print("   .geom_point(aes(color='Species'),size=8, alpha=0.8))")

try:
    plot2 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(aes(color='Species'), size=8, alpha=0.8)
    )
    
    print("   ✅ Plot created")
    
    # Analyze what's happening
    geom = plot2.layers[0]
    combined_aes = plot2._combine_aesthetics(geom.mapping)
    print(f"   Plot-level aes: {plot2.mapping.mappings}")
    print(f"   Layer-level aes: {geom.mapping.mappings if geom.mapping else None}")
    print(f"   Combined aes: {combined_aes.mappings}")
    
    rendered = plot2._render()
    print(f"   Rendered successfully: {type(rendered)}")
    
    # The issue: Layer-level aes(color='Species') looks for column 'Species'
    # But the column is 'species' (lowercase), so it doesn't find it
    print("   ANALYSIS: This should show a warning!")
    print("   - Layer aes looks for 'Species' column (capital S)")
    print("   - But data only has 'species' column (lowercase s)")
    print("   - Should warn about missing column and fall back")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Case 3: What should work correctly
print("\n3. CORRECT CASE: This should work perfectly")
print("   .geom_point(aes(color='species'), size=8, alpha=0.8))")

try:
    plot3 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(aes(color='species'), size=8, alpha=0.8)
    )
    
    print("   ✅ Plot created")
    rendered = plot3._render()
    print(f"   Rendered successfully: {type(rendered)}")
    print("   This correctly maps to the 'species' column")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("DIAGNOSIS:")
print("="*60)
print("The user's confusion comes from case sensitivity:")
print("- Data has column 'species' (lowercase)")
print("- User used aes(color='Species') (uppercase)")
print("- This silently fails to find the column")
print("- Need better error handling/warnings for missing columns")
print("\nThe API behavior is actually CORRECT, but error handling needs improvement!")