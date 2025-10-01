#!/usr/bin/env python3
"""
Test to understand the rendering logic and find the exact issue
"""

import pandas as pd
import numpy as np
from ggviews import ggplot, aes
from ggviews.geoms import geom_point

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 10),
    'weight': np.random.normal(70, 15, 10), 
    'species': ['setosa', 'versicolor', 'virginica'] * 3 + ['setosa']
})

print("Test data:")
print(df)

print("\n" + "="*60)
print("DETAILED RENDERING ANALYSIS")
print("="*60)

# Test 1: Working case - aes(color='species') 
print("\n1. WORKING CASE: aes(color='species')")
try:
    plot1 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(aes(color='species'), size=8, alpha=0.8))
    
    # Get the geom and inspect its behavior
    geom = plot1.layers[0]
    data = plot1.data
    combined_aes = plot1._combine_aesthetics(geom.mapping)
    
    print(f"   Combined aesthetics: {combined_aes.mappings}")
    print(f"   Data columns: {data.columns.tolist()}")
    
    # Check color mapping
    color_map = geom._get_color_mapping(combined_aes, data, plot1)
    print(f"   Color mapping: {color_map}")
    
    # Try to render
    try:
        rendered = geom._render(data, combined_aes, plot1)
        print(f"   Render result type: {type(rendered)}")
        print("   ✅ Rendering successful")
    except Exception as render_error:
        print(f"   ❌ Render failed: {render_error}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ Plot creation failed: {e}")

# Test 2: Broken case - aes(color='Species') with wrong column name
print("\n2. BROKEN CASE: aes(color='Species') - wrong column")
try:
    plot2 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(aes(color='Species'), size=8, alpha=0.8))
    
    geom = plot2.layers[0]
    data = plot2.data
    combined_aes = plot2._combine_aesthetics(geom.mapping)
    
    print(f"   Combined aesthetics: {combined_aes.mappings}")
    print(f"   Looking for 'Species' in columns: {'Species' in data.columns}")
    
    # Check color mapping
    color_map = geom._get_color_mapping(combined_aes, data, plot2)
    print(f"   Color mapping: {color_map}")
    
    # Try to render
    try:
        rendered = geom._render(data, combined_aes, plot2)
        print(f"   Render result type: {type(rendered)}")
        print("   ✅ Rendering successful (but shouldn't be!)")
    except Exception as render_error:
        print(f"   ❌ Render failed: {render_error}")
        
except Exception as e:
    print(f"❌ Plot creation failed: {e}")

# Test 3: Fixed color case
print("\n3. FIXED COLOR CASE: color='red'")
try:
    plot3 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(color='red', size=8, alpha=0.8))
    
    geom = plot3.layers[0]
    data = plot3.data
    combined_aes = plot3._combine_aesthetics(geom.mapping)
    
    print(f"   Combined aesthetics: {combined_aes.mappings}")
    print(f"   Geom params: {geom.params}")
    
    # Check color mapping  
    color_map = geom._get_color_mapping(combined_aes, data, plot3)
    print(f"   Color mapping: {color_map}")
    
    # Try to render
    try:
        rendered = geom._render(data, combined_aes, plot3)
        print(f"   Render result type: {type(rendered)}")
        print("   ✅ Rendering successful")
    except Exception as render_error:
        print(f"   ❌ Render failed: {render_error}")
        
except Exception as e:
    print(f"❌ Plot creation failed: {e}")

# Test 4: The problematic case - color='Species' as fixed value
print("\n4. PROBLEMATIC CASE: color='Species' as fixed value")
try:
    plot4 = (ggplot(df, aes(x='height', y='weight'))
             .geom_point(color='Species', size=8, alpha=0.8))
    
    geom = plot4.layers[0]
    data = plot4.data
    combined_aes = plot4._combine_aesthetics(geom.mapping)
    
    print(f"   Combined aesthetics: {combined_aes.mappings}")
    print(f"   Geom params: {geom.params}")
    print(f"   Should use 'Species' as a fixed color name")
    
    # Check color mapping
    color_map = geom._get_color_mapping(combined_aes, data, plot4)
    print(f"   Color mapping: {color_map}")
    
    # Try to render
    try:
        rendered = geom._render(data, combined_aes, plot4)
        print(f"   Render result type: {type(rendered)}")
        print("   ✅ Rendering successful")
        print("   This should set all points to color='Species' (literal string)")
    except Exception as render_error:
        print(f"   ❌ Render failed: {render_error}")
        
except Exception as e:
    print(f"❌ Plot creation failed: {e}")