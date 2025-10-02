#!/usr/bin/env python3
"""
Test if viridis colors are now working correctly
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes

hv.extension('bokeh')

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 15),
    'weight': np.random.normal(70, 15, 15),
    'species': ['setosa'] * 5 + ['versicolor'] * 5 + ['virginica'] * 5,
})

print("TESTING VIRIDIS COLOR FIX")
print("="*50)
print(f"Test data:\n{df.groupby('species').size()}\n")

# Test 1: Default colors (should show default ggplot colors)
print("1. DEFAULT COLORS (no viridis):")
try:
    plot_default = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .theme_minimal()
    )
    
    rendered_default = plot_default._render()
    print(f"   ✅ Rendered: {type(rendered_default)}")
    
    # Check what colors were used
    geom = plot_default.layers[0]
    combined_aes = plot_default._combine_aesthetics(geom.mapping)
    color_map = geom._get_color_mapping(combined_aes, df, plot_default)
    print(f"   Colors used: {color_map}")
    print("   Should show: Red, Cyan, Green (default ggplot colors)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Viridis colors (should show viridis palette)
print("\n2. VIRIDIS COLORS:")
try:
    plot_viridis = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .scale_colour_viridis_d()
        .theme_minimal()
    )
    
    rendered_viridis = plot_viridis._render()
    print(f"   ✅ Rendered: {type(rendered_viridis)}")
    
    # Check what colors were used after rendering
    if hasattr(plot_viridis, 'viridis_discrete_map'):
        print(f"   Viridis mapping: {plot_viridis.viridis_discrete_map}")
        print("   Should show: Purple, Teal, Yellow (viridis colors)")
    else:
        print("   ❌ No viridis mapping found!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Different viridis options
print("\n3. DIFFERENT VIRIDIS OPTIONS:")
options = ['plasma', 'inferno', 'magma']
for option in options:
    try:
        plot_option = (
            ggplot(df, aes(x='height', y='weight', color='species'))
            .geom_point(size=8, alpha=0.8)
            .scale_colour_viridis_d(option=option)
            .theme_minimal()
        )
        
        rendered_option = plot_option._render()
        if hasattr(plot_option, 'viridis_discrete_map'):
            colors = list(plot_option.viridis_discrete_map.values())
            print(f"   ✅ {option.capitalize()}: {colors[:2]}... (showing first 2)")
        else:
            print(f"   ❌ {option.capitalize()}: No mapping found")
            
    except Exception as e:
        print(f"   ❌ {option.capitalize()} error: {e}")

print("\n" + "="*50)
print("CONCLUSION:")
if hasattr(plot_viridis, 'viridis_discrete_map'):
    print("✅ Viridis colors should now be working!")
    print("🎨 Users should see proper viridis colors instead of default colors")
else:
    print("❌ Viridis colors still not working - need further investigation")