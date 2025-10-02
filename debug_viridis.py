#!/usr/bin/env python3
"""
Debug why viridis colors are not working
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes

hv.extension('bokeh')

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 20),
    'weight': np.random.normal(70, 15, 20),
    'species': np.random.choice(['setosa', 'versicolor', 'virginica'], 20),
})

print("DEBUGGING VIRIDIS COLORS")
print("="*50)

# Test the problematic viridis case
print("Testing viridis color scale:")
try:
    plot = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .scale_colour_viridis_d()
        .theme_minimal()
        .labs(title='Viridis Color Palette')
    )
    
    print("✅ Plot created")
    print(f"Plot scales: {plot.scales}")
    print(f"Number of layers: {len(plot.layers)}")
    print(f"Plot theme: {plot.theme}")
    
    # Check if viridis scale is stored
    if 'color' in plot.scales:
        viridis_scale = plot.scales['color']
        print(f"Viridis scale found: {type(viridis_scale)}")
        print(f"Scale colors: {viridis_scale.colors}")
    else:
        print("❌ No viridis scale found in plot.scales")
    
    # Check the geom layer
    geom = plot.layers[0]
    print(f"Geom type: {type(geom)}")
    
    # Test color mapping
    combined_aes = plot._combine_aesthetics(geom.mapping)
    print(f"Combined aesthetics: {combined_aes.mappings}")
    
    color_map = geom._get_color_mapping(combined_aes, df, plot)
    print(f"Default color mapping: {color_map}")
    
    # Test scale application
    if 'color' in plot.scales:
        scale = plot.scales['color']
        print(f"\nTesting scale application...")
        
        # Try to apply the scale
        modified_plot = scale._apply(plot._render(), plot, df)
        print(f"Scale applied successfully: {type(modified_plot)}")
        
        # Check if the scale has created any mappings
        if hasattr(plot, 'viridis_discrete_map'):
            print(f"Viridis discrete map: {plot.viridis_discrete_map}")
        else:
            print("❌ No viridis_discrete_map created")
    
    rendered = plot._render()
    print(f"Final rendered plot: {type(rendered)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Compare with working default colors
print("\n" + "="*50)
print("Comparing with default colors (no viridis):")
try:
    plot_default = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .theme_minimal()
    )
    
    geom_default = plot_default.layers[0]
    combined_aes_default = plot_default._combine_aesthetics(geom_default.mapping)
    color_map_default = geom_default._get_color_mapping(combined_aes_default, df, plot_default)
    print(f"Default color mapping: {color_map_default}")
    
except Exception as e:
    print(f"❌ Error: {e}")