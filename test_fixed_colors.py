#!/usr/bin/env python3
"""
Test the fix for color=None issue
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
    'species': ['setosa', 'versicolor', 'virginica'] * 3 + ['setosa']
})

print("Testing fixed color handling...")
print("="*50)

# Test the user's problematic case
print("\n1. User's case: aes(color='Species') with wrong column name")
try:
    plot = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(aes(color='Species'), size=8, alpha=0.8)
    )
    
    print("✅ Plot created")
    
    # Test rendering
    rendered = plot._render()
    print(f"✅ Rendered: {type(rendered)}")
    
    print("This should now show points with default blue color")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test proper color mapping
print("\n2. Correct case: aes(color='species')")
try:
    plot2 = (
        ggplot(df, aes(x='height', y='weight'))  
        .geom_point(aes(color='species'), size=8, alpha=0.8)
    )
    
    rendered2 = plot2._render()
    print(f"✅ Rendered: {type(rendered2)}")
    print("This should show points colored by species")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test fixed color parameter
print("\n3. Fixed color: color='red'")
try:
    plot3 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(color='red', size=8, alpha=0.8)
    )
    
    rendered3 = plot3._render()
    print(f"✅ Rendered: {type(rendered3)}")
    print("This should show red points")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*50)
print("CONCLUSION:")  
print("The color=None issue should now be fixed.")
print("All cases should render visible points with appropriate colors.")
print("User should no longer see 'empty canvas'.")