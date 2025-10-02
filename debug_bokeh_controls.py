#!/usr/bin/env python3
"""
Debug bokeh controls duplication issue
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes

hv.extension('bokeh')

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 10),
    'weight': np.random.normal(70, 15, 10),
    'species': ['setosa'] * 4 + ['versicolor'] * 3 + ['virginica'] * 3,
})

print("DEBUGGING BOKEH CONTROLS")
print("="*50)

# Test case with theme_minimal that shows controls twice
print("1. Testing theme_minimal (reported to show controls twice):")
try:
    plot = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(size=6, alpha=0.7)
        .theme_minimal()
        .labs(title='Height vs Weight', x='Height (cm)', y='Weight (kg)')
    )
    
    print(f"   Plot layers: {len(plot.layers)}")
    print(f"   Plot theme: {type(plot.theme)}")
    
    # Check rendering without calling show
    rendered = plot._render()
    print(f"   Rendered type: {type(rendered)}")
    
    # Check if this is an overlay (which might cause double controls)
    if hasattr(rendered, 'type'):
        print(f"   Holoviews element type: {rendered.type}")
    
    print("   ✅ This should show controls once, at the top")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test case with theme_classic that shows controls once  
print("\n2. Testing theme_classic (reported to show controls once):")
try:
    plot = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .theme_classic()
        .labs(title='Height vs Weight by Species', x='Height (cm)', y='Weight (kg)')
    )
    
    print(f"   Plot layers: {len(plot.layers)}")
    print(f"   Plot theme: {type(plot.theme)}")
    
    rendered = plot._render()
    print(f"   Rendered type: {type(rendered)}")
    
    # This one creates an overlay because of color mapping
    if hasattr(rendered, 'type'):
        print(f"   Holoviews element type: {rendered.type}")
    
    print("   ✅ This should show controls once, at the top")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test the difference between single element vs overlay
print("\n3. Analyzing rendering differences:")

# Single element (no color mapping)
plot_single = (
    ggplot(df, aes(x='height', y='weight'))
    .geom_point(size=6, alpha=0.7)
    .theme_minimal()
)
rendered_single = plot_single._render()

# Overlay element (with color mapping)  
plot_overlay = (
    ggplot(df, aes(x='height', y='weight', color='species'))
    .geom_point(size=8, alpha=0.8)
    .theme_minimal()
)
rendered_overlay = plot_overlay._render()

print(f"   Single element type: {type(rendered_single)}")
print(f"   Overlay element type: {type(rendered_overlay)}")

# Check if overlay contains multiple elements
if hasattr(rendered_overlay, '__len__'):
    try:
        print(f"   Overlay contains {len(rendered_overlay)} elements")
    except:
        pass

print("\n" + "="*50)
print("ANALYSIS:")
print("The issue might be that:")
print("1. Single elements get toolbar options applied once")
print("2. Overlays (multiple colored categories) get toolbar applied to each element")
print("3. This results in multiple toolbars being shown")