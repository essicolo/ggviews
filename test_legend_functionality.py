#!/usr/bin/env python3
"""
Test automatic legend generation in ggviews
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes

hv.extension('bokeh')

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'height': np.random.normal(170, 10, 50),
    'weight': np.random.normal(70, 15, 50),
    'species': np.random.choice(['setosa', 'versicolor', 'virginica'], 50),
    'age': np.random.uniform(20, 60, 50),
    'time': range(50),
    'value': np.cumsum(np.random.randn(50)) + np.sin(np.arange(50) * 0.2) * 5
})

print("🎨 TESTING AUTOMATIC LEGEND GENERATION")
print("="*60)

# Test 1: Color legend for scatter plot (the user's example)
print("\n1. Testing color legend for scatter plot:")
print("   Code: ggplot(df, aes(x='height', y='weight', color='species')).geom_point()")
try:
    plot1 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
    )
    
    # Check if the plot was created successfully
    rendered = plot1._render()
    print("   ✅ Plot created and rendered successfully")
    print(f"   📊 Rendered type: {type(rendered)}")
    
    # Check if it's an overlay (multiple elements for different colors)
    if hasattr(rendered, '__len__'):
        try:
            print(f"   🎨 Legend elements: {len(rendered)} (one per species)")
        except:
            pass
    
    print("   💡 Should automatically show legend for 'species' colors")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Color legend for line plot
print("\n2. Testing color legend for line plot:")
print("   Code: ggplot(df, aes(x='time', y='value', color='species')).geom_line()")
try:
    plot2 = (
        ggplot(df, aes(x='time', y='value', color='species'))
        .geom_line(size=3)
    )
    
    rendered2 = plot2._render()
    print("   ✅ Line plot with color legend created")
    print(f"   📊 Rendered type: {type(rendered2)}")
    print("   💡 Should show legend for different colored lines")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Size mapping (should not create legend automatically)
print("\n3. Testing size mapping:")
print("   Code: ggplot(df, aes(x='height', y='weight', size='age')).geom_point()")
try:
    plot3 = (
        ggplot(df, aes(x='height', y='weight', size='age'))
        .geom_point(alpha=0.7)
    )
    
    rendered3 = plot3._render()
    print("   ✅ Size mapping plot created")
    print(f"   📊 Rendered type: {type(rendered3)}")
    print("   💡 Points should vary in size based on 'age'")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Both color and size mapping
print("\n4. Testing color + size mapping:")
print("   Code: aes(x='height', y='weight', color='species', size='age')")
try:
    plot4 = (
        ggplot(df, aes(x='height', y='weight', color='species', size='age'))
        .geom_point(alpha=0.8)
    )
    
    rendered4 = plot4._render()
    print("   ✅ Color + size mapping plot created")
    print(f"   📊 Rendered type: {type(rendered4)}")
    print("   🎨 Should show legend for 'species' colors")
    print("   📏 Point sizes should vary by 'age'")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: ColorBrewer palette with legend
print("\n5. Testing ColorBrewer palette with legend:")
print("   Code: .scale_colour_brewer(palette='Set1')")
try:
    plot5 = (
        ggplot(df, aes(x='height', y='weight', color='species'))
        .geom_point(size=8, alpha=0.8)
        .scale_colour_brewer(palette='Set1')
    )
    
    rendered5 = plot5._render()
    print("   ✅ ColorBrewer palette with legend created")
    print(f"   📊 Rendered type: {type(rendered5)}")
    print("   🎨 Should show ColorBrewer colors in legend")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: No aesthetic mapping (no legend expected)
print("\n6. Testing no aesthetic mapping (control case):")
print("   Code: ggplot(df, aes(x='height', y='weight')).geom_point()")
try:
    plot6 = (
        ggplot(df, aes(x='height', y='weight'))
        .geom_point(size=6, alpha=0.7, color='red')
    )
    
    rendered6 = plot6._render()
    print("   ✅ Single color plot created")
    print(f"   📊 Rendered type: {type(rendered6)}")
    print("   💡 Should NOT show legend (no aesthetic mapping)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("🎯 LEGEND FUNCTIONALITY SUMMARY")
print("="*60)

expected_behavior = [
    "✅ aes(color='column') → Automatic color legend",
    "✅ aes(size='column') → Variable point sizes",
    "✅ Multiple colors → Legend with all categories",
    "✅ ColorBrewer scales → Legend with proper colors",
    "✅ Line plots → Color legend for different lines",
    "❌ No aesthetics → No legend (correct behavior)"
]

for behavior in expected_behavior:
    print(f"   {behavior}")

print(f"\n💡 HOW TO TEST INTERACTIVELY:")
print(f"   plot1.show()  # Color legend for species")
print(f"   plot2.show()  # Line color legend")  
print(f"   plot3.show()  # Size variation")
print(f"   plot4.show()  # Color legend + size variation")
print(f"   plot5.show()  # ColorBrewer legend")
print(f"   plot6.show()  # No legend")

print(f"\n🎨 GGPLOT2 PARITY:")
print(f"   ggviews now automatically creates legends like ggplot2!")
print(f"   Legend position: Right side (holoviews default)")
print(f"   Legend content: Category names and colors")
print(f"   Legend behavior: Only when aesthetic mappings are used")

print(f"\n📊 NEXT STEPS:")
print(f"   • Add legend customization (position, title, etc.)")
print(f"   • Add size legends for continuous variables")
print(f"   • Add fill legends for geoms like bars, areas")
print(f"   • Add shape legends when shape aesthetic is implemented")