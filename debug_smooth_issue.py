#!/usr/bin/env python3
"""
Debug geom_smooth placement and variable mapping issues
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes

hv.extension('bokeh')

# Create test data with clear relationship
np.random.seed(42)
n = 50

df = pd.DataFrame({
    'height': np.random.normal(170, 10, n),
    'weight': np.random.normal(70, 15, n),
    'species': np.random.choice(['A', 'B'], n),
    'x': range(n),
    'y': np.cumsum(np.random.randn(n)) + np.arange(n) * 0.1
})

# Add clear correlation
df['weight'] = 50 + 0.5 * df['height'] + np.random.normal(0, 5, n)

print("DEBUGGING GEOM_SMOOTH ISSUES")
print("="*50)

# Test 1: Simple smooth on correlated data
print("\n1. Testing geom_smooth with correlated data:")
print("   Expected: Smooth line following height-weight correlation")

try:
    plot1 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(alpha=0.6)
        .geom_smooth(method='lm', color='red')
    )
    
    rendered1 = plot1._render()
    print("   ✅ SUCCESS: geom_smooth with points created")
    print(f"   📊 Type: {type(rendered1)}")
    
    # Check if this is an overlay with multiple elements
    if hasattr(rendered1, '__len__'):
        print(f"   📝 Elements: {len(rendered1)} (points + smooth line)")
    
    # Test aesthetic combination
    geom_smooth_layer = None
    for layer in plot1.layers:
        if 'smooth' in str(type(layer)).lower():
            geom_smooth_layer = layer
            break
    
    if geom_smooth_layer:
        combined_aes = plot1._combine_aesthetics(geom_smooth_layer.mapping)
        print(f"   🎯 Smooth aesthetics: {combined_aes.mappings}")
        print(f"   Expected: x='height', y='weight'")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Check if smooth is using wrong variables
print("\n2. Testing variable mapping explicitly:")

try:
    # Test data ranges
    print(f"   📊 Height range: {df['height'].min():.1f} - {df['height'].max():.1f}")
    print(f"   📊 Weight range: {df['weight'].min():.1f} - {df['weight'].max():.1f}")
    
    # Test correlation
    correlation = df['height'].corr(df['weight'])
    print(f"   📈 Height-Weight correlation: {correlation:.3f}")
    
    # Create smooth only plot to isolate the issue
    plot2 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_smooth(method='lm', color='blue', alpha=0.8)
    )
    
    rendered2 = plot2._render()
    print(f"   ✅ Smooth-only plot created: {type(rendered2)}")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Different data to see if it's a data issue
print("\n3. Testing with simple linear data:")

try:
    simple_df = pd.DataFrame({
        'x': np.linspace(0, 10, 20),
        'y': np.linspace(0, 10, 20) + np.random.normal(0, 0.5, 20)
    })
    
    plot3 = (
        ggplot(simple_df, aes(x='x', y='y'))
        .geom_point()
        .geom_smooth(method='lm', color='green')
    )
    
    rendered3 = plot3._render()
    print("   ✅ Simple linear data smooth created")
    print(f"   📊 Data correlation: {simple_df['x'].corr(simple_df['y']):.3f}")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 4: Check if the issue is with grouped data
print("\n4. Testing grouped smooth (potential issue source):")

try:
    plot4 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(alpha=0.6)
        .geom_smooth(method='lm', se=False)
    )
    
    rendered4 = plot4._render()
    print("   ✅ Grouped smooth created")
    
    # This might be where the issue occurs - smooth might be grouping incorrectly
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "="*50)
print("DIAGNOSTIC SUMMARY:")
print("="*50)

print("🔍 Potential Issues to Check:")
print("   1. Is geom_smooth using correct x/y mappings?")
print("   2. Is smooth line positioned correctly relative to data points?")
print("   3. Are grouped smooths (by color) working correctly?")
print("   4. Is the smooth line visible and styled properly?")

print("\n💡 To Verify Visually:")
print("   plot1.show()  # Points + smooth line")
print("   plot2.show()  # Smooth line only") 
print("   plot3.show()  # Simple linear data")
print("   plot4.show()  # Grouped smooths")

print("\n🎯 Expected Behavior:")
print("   • Smooth line should follow the trend of the data points")
print("   • Linear method (lm) should show straight line through data")
print("   • Smooth should use same x/y mapping as points")
print("   • Color should be applied correctly")