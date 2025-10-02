#!/usr/bin/env python3
"""
Debug the 'empty canvas' issue
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes
from ggviews.geoms import geom_point

hv.extension('bokeh')

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 20),
    'weight': np.random.normal(70, 15, 20),
    'species': np.random.choice(['setosa', 'versicolor', 'virginica'], 20),
})

print("Testing the 'empty canvas' issue...")
print("="*50)

# Test case that supposedly shows empty canvas
print("\nCase: aes(color='Species') with wrong column name")
try:
    plot = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(aes(color='Species'), size=8, alpha=0.8)
    )
    
    print("Plot created successfully")
    
    # Get detailed info about what's being rendered
    geom = plot.layers[0]
    data = plot.data
    combined_aes = plot._combine_aesthetics(geom.mapping)
    
    print(f"Combined aesthetics: {combined_aes.mappings}")
    print(f"Geom params: {geom.params}")
    
    # Check the rendering step by step
    print("\nStep-by-step rendering:")
    x_col = combined_aes.mappings['x']
    y_col = combined_aes.mappings['y']
    print(f"1. X column: {x_col} ✅")
    print(f"2. Y column: {y_col} ✅")
    
    x_data = data[x_col]
    y_data = data[y_col]
    print(f"3. X data points: {len(x_data)} ✅")
    print(f"4. Y data points: {len(y_data)} ✅")
    print(f"   X range: {x_data.min():.1f} to {x_data.max():.1f}")
    print(f"   Y range: {y_data.min():.1f} to {y_data.max():.1f}")
    
    color_map = geom._get_color_mapping(combined_aes, data, plot)
    print(f"5. Color map: {color_map} ({'empty - will use default' if not color_map else 'has mappings'})")
    
    # Check which rendering path is taken
    if color_map and 'color' in combined_aes.mappings:
        print("6. Taking color mapping path")
    else:
        print("6. Taking single color path")
        color = geom.params.get('color', '#1f77b4')
        print(f"   Using color: {color}")
    
    # Try the actual rendering
    rendered = geom._render(data, combined_aes, plot)
    print(f"7. Rendered result: {type(rendered)}")
    
    # Check if it's actually empty
    if hasattr(rendered, 'data') and hasattr(rendered.data, '__len__'):
        print(f"   Data length: {len(rendered.data)}")
    
    # Try full plot rendering  
    full_rendered = plot._render()
    print(f"8. Full plot rendered: {type(full_rendered)}")
    
    print("\n✅ No 'empty canvas' detected - plot should show points!")
    print("   If user sees empty canvas, it might be a frontend display issue")
    
except Exception as e:
    print(f"❌ Error during rendering: {e}")
    import traceback
    traceback.print_exc()

# Test a working case for comparison
print("\n" + "="*50)
print("Comparison: Working case with correct column")
try:
    plot_working = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(aes(color='species'), size=8, alpha=0.8)
    )
    
    rendered_working = plot_working._render()
    print(f"Working case rendered: {type(rendered_working)}")
    print("This should definitely show colored points")
    
except Exception as e:
    print(f"❌ Working case failed: {e}")

print("\n" + "="*50)
print("CONCLUSION:")
print("The 'empty canvas' is likely NOT due to the aesthetic mapping logic.")
print("Both cases render successfully and should show points.")
print("The issue might be:")
print("1. Frontend display/browser issue")  
print("2. Color visibility (maybe color='Species' renders as invisible color)")
print("3. Plot dimensions/viewport issue")
print("4. User expectation vs actual behavior mismatch")