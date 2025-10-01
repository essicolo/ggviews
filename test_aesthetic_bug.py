#!/usr/bin/env python3
"""
Test to reproduce and understand the aesthetic mapping bug
"""

import pandas as pd
import numpy as np
from ggviews import ggplot, aes
from ggviews.geoms import geom_point

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 20),
    'weight': np.random.normal(70, 15, 20),
    'species': np.random.choice(['setosa', 'versicolor', 'virginica'], 20),
})

print("Test data columns:", df.columns.tolist())
print("Sample data:")
print(df.head())

print("\n" + "="*60)
print("TESTING AESTHETIC MAPPING ISSUES")
print("="*60)

# Test 1: This works but shouldn't (color='Species' should be a fixed color)
print("\n1. Testing: geom_point(color='Species') - Should set fixed color, not map column")
try:
    plot1 = (ggplot(df, aes(x='height', y='weight', color='species'))
             .geom_point(color='Species', size=8, alpha=0.8))
    print("✅ Plot created (but this behavior is WRONG)")
    print("   This should set all points to a fixed color 'Species', not map to a column")
    
    # Let's examine what the geom actually received
    geom = plot1.layers[0]
    print(f"   Geom params: {geom.params}")
    print(f"   Geom mapping: {geom.mapping}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: This should work but doesn't (proper aesthetic mapping)
print("\n2. Testing: geom_point(aes(color='species')) - Should map to species column")
try:
    plot2 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(aes(color='species'), size=8, alpha=0.8))
    print("✅ Plot created")
    
    # Let's examine what the geom actually received
    geom = plot2.layers[0]
    print(f"   Geom params: {geom.params}")
    print(f"   Geom mapping: {geom.mapping}")
    print(f"   Geom mapping dict: {geom.mapping.mappings if geom.mapping else 'None'}")
    
    # Test rendering
    combined_aes = plot2._combine_aesthetics(geom.mapping)
    print(f"   Combined aesthetics: {combined_aes.mappings}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Let's test what should happen with a fixed color
print("\n3. Testing: geom_point(color='red') - Should set all points to red")
try:
    plot3 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(color='red', size=8, alpha=0.8))
    print("✅ Plot created")
    
    geom = plot3.layers[0]
    print(f"   Geom params: {geom.params}")
    print(f"   Should render all points in red color")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Testing case sensitivity
print("\n4. Testing: aes(color='Species') with wrong case - Should fail gracefully")
try:
    plot4 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(aes(color='Species'), size=8, alpha=0.8))
    print("✅ Plot created (but 'Species' column doesn't exist)")
    
    geom = plot4.layers[0]
    print(f"   Geom mapping: {geom.mapping.mappings if geom.mapping else 'None'}")
    
    # Try to render to see what happens
    try:
        rendered = plot4._render()
        print("   Render successful")
    except Exception as render_error:
        print(f"   Render failed: {render_error}")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("DIAGNOSIS:")
print("="*60)
print("The issue is that the API doesn't properly distinguish between:")
print("1. Fixed aesthetic values (color='red') - should apply to all points") 
print("2. Mapped aesthetic values (aes(color='column')) - should map from data")
print("\nThe current implementation is confusing these two cases!")