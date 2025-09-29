"""
Updated ggplot2 comparison with coord_fixed() implemented
"""

import pandas as pd
import numpy as np
from ggviews import ggplot, aes
from ggviews.geoms import geom_point, geom_smooth
from ggviews.themes import theme_minimal
from ggviews.facets import facet_grid
from ggviews.scales import scale_color_continuous

# Create enhanced mpg-like dataset
np.random.seed(42)
years = [1999, 2008]
drvs = ['4', 'f', 'r']

mpg_data = []
for year in years:
    for drv in drvs:
        n_cars = 18  # More balanced dataset
        
        # More realistic mpg relationships
        if drv == '4':  # 4WD
            base_cty = np.random.normal(16, 3, n_cars)  # Lower efficiency
            displ = np.random.normal(4.0, 1.2, n_cars)  # Larger engines
        elif drv == 'f':  # Front wheel drive
            base_cty = np.random.normal(22, 4, n_cars)  # Higher efficiency
            displ = np.random.normal(2.5, 0.8, n_cars)  # Smaller engines
        else:  # Rear wheel drive
            base_cty = np.random.normal(18, 3, n_cars)  # Medium efficiency
            displ = np.random.normal(3.5, 1.0, n_cars)  # Medium engines
        
        # Highway is typically 1.2-1.4x city mpg
        base_hwy = base_cty * np.random.uniform(1.2, 1.4, n_cars)
        
        # Add some correlation with displacement (negative)
        base_cty -= (displ - 3) * 1.5
        base_hwy -= (displ - 3) * 1.5
        
        # Add year effect (cars got slightly more efficient)
        if year == 2008:
            base_cty += 1
            base_hwy += 1
        
        # Ensure reasonable bounds
        base_cty = np.clip(base_cty, 9, 35)
        base_hwy = np.clip(base_hwy, 12, 45)
        displ = np.clip(displ, 1.0, 7.0)
        
        for i in range(n_cars):
            mpg_data.append({
                'cty': base_cty[i],
                'hwy': base_hwy[i],
                'displ': displ[i],
                'year': year,
                'drv': drv
            })

mpg = pd.DataFrame(mpg_data)

print("Enhanced mpg dataset for ggplot2 comparison:")
print(mpg.head(10))
print(f"Shape: {mpg.shape}")
print("\nSummary by drive type:")
print(mpg.groupby('drv')[['cty', 'hwy', 'displ']].mean().round(2))

print("\n" + "="*80)
print("UPDATED GGPLOT2 vs GGVIEWS COMPARISON")
print("="*80)

print("\nOriginal ggplot2 code:")
original_code = '''
ggplot(mpg, aes(cty, hwy)) +
geom_point(mapping = aes(colour = displ)) +
geom_smooth(formula = y ~ x, method = "lm") +
scale_colour_viridis_c() +
facet_grid(year ~ drv) +
coord_fixed() +                    # ← NOW IMPLEMENTED!
theme_minimal() +
theme(panel.grid.minor = element_blank())
'''
print(original_code)

print("New ggviews equivalent:")
ggviews_code = '''
(ggplot(mpg, aes(x='cty', y='hwy'))
 .geom_point(aes(color='displ'), alpha=0.7, size=4)
 .geom_smooth(method='lm', color='darkblue', alpha=0.6)
 .scale_color_continuous(low='#440154', high='#FDE725')  # Viridis colors
 .facet_grid('year ~ drv')
 .coord_fixed()                    # ← NOW IMPLEMENTED!
 .theme_minimal()
 .labs(title='City vs Highway MPG by Year and Drive Type',
       x='City MPG (miles per gallon)',
       y='Highway MPG (miles per gallon)', 
       color='Engine Displacement (L)'))
'''
print(ggviews_code)

# Create the plot
try:
    plot = (ggplot(mpg, aes(x='cty', y='hwy'))
            .geom_point(aes(color='displ'), alpha=0.7, size=4)
            .geom_smooth(method='lm', color='darkblue', alpha=0.6)
            .scale_color_continuous(low='#440154', high='#FDE725')
            .facet_grid('year ~ drv')
            .coord_fixed()  # This is the key addition!
            .theme_minimal()
            .labs(title='City vs Highway MPG by Year and Drive Type',
                  x='City MPG (miles per gallon)',
                  y='Highway MPG (miles per gallon)', 
                  color='Engine Displacement (L)'))
    
    print("✅ Enhanced ggviews plot created successfully with coord_fixed()!")
    
    # Test the coordinate system
    coord_sys = plot.coord_system
    print(f"✅ Coordinate system: {type(coord_sys).__name__} with ratio={coord_sys.ratio}")
    
except Exception as e:
    print(f"❌ Plot creation failed: {e}")

print("\n" + "="*80)
print("UPDATED FEATURE COMPARISON")
print("="*80)

features = [
    ("ggplot(mpg, aes(cty, hwy))", "ggplot(mpg, aes(x='cty', y='hwy'))", "✅ Exact match"),
    ("geom_point(aes(colour = displ))", "geom_point(aes(color='displ'))", "✅ Exact match"),
    ("geom_smooth(method = 'lm')", "geom_smooth(method='lm')", "✅ Exact match"),
    ("facet_grid(year ~ drv)", "facet_grid('year ~ drv')", "✅ Exact match"),
    ("coord_fixed()", "coord_fixed()", "✅ NOW IMPLEMENTED!"),
    ("theme_minimal()", "theme_minimal()", "✅ Exact match"),
    ("scale_colour_viridis_c()", "scale_color_continuous(viridis)", "⚠️ Basic version"),
    ("theme(panel.grid.minor = ...)", "# Not available", "❌ Missing"),
]

print("Feature-by-feature comparison:")
print("-" * 80)
for i, (ggplot2, ggviews, status) in enumerate(features):
    print(f"{i+1}. ggplot2: {ggplot2}")
    print(f"   ggviews: {ggviews}")
    print(f"   Status:  {status}")
    print()

# Updated compatibility assessment
full_match = len([s for _, _, s in features if s.startswith("✅")])
partial_match = len([s for _, _, s in features if s.startswith("⚠️")])
missing = len([s for _, _, s in features if s.startswith("❌")])

print("UPDATED COMPATIBILITY ASSESSMENT:")
print(f"✅ Fully implemented: {full_match}/8 = {full_match/8:.1%}")
print(f"⚠️ Partially implemented: {partial_match}/8 = {partial_match/8:.1%}")
print(f"❌ Missing: {missing}/8 = {missing/8:.1%}")
print(f"Overall compatibility: {(full_match + partial_match*0.5)/8:.1%}")

print(f"\n🎉 MAJOR IMPROVEMENT: coord_fixed() implementation brings us to {full_match}/8 core features!")

print("\n" + "="*80)
print("VISUAL OUTPUT COMPARISON")
print("="*80)

comparison_text = """
EXPECTED OUTPUT (both ggplot2 and ggviews):

📊 6-Panel Faceted Plot Layout:
   ┌─────────────────────────────────────────┐
   │  Year 1999          Year 2008           │
   ├─────────────┬─────────────┬─────────────┤
   │    4WD      │    FWD      │    RWD      │
   │             │             │             │
   │   • • •     │   • • •     │   • • •     │
   │  • • • •    │  • • • •    │  • • • •    │
   │   • • •     │   • • •     │   • • •     │  
   │    ___      │    ___      │    ___      │
   │   /         │   /         │   /         │
   └─────────────┴─────────────┴─────────────┤

KEY IMPROVEMENTS WITH coord_fixed():
✅ Fixed 1:1 aspect ratio (1 unit city MPG = 1 unit highway MPG)
✅ Preserves meaningful spatial relationships
✅ Makes scatter patterns comparable across facets  
✅ Points colored by engine displacement (purple to yellow gradient)
✅ Linear trend lines show positive correlation
✅ Minimal theme with clean appearance

VISUAL DIFFERENCES vs ggplot2:
- ggplot2: Exact viridis color scale, no minor grid lines
- ggviews: Viridis-like colors, default grid lines
- Both: Same data relationships and statistical patterns
"""

print(comparison_text)