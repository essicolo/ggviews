"""
ggplot2 Comparison: Recreating the mpg example with ggviews

Original ggplot2 code:
ggplot(mpg, aes(cty, hwy)) +
geom_point(mapping = aes(colour = displ)) +
geom_smooth(formula = y ~ x, method = "lm") +
scale_colour_viridis_c() +
facet_grid(year ~ drv) +
coord_fixed() +
theme_minimal() +
theme(panel.grid.minor = element_blank())
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ggviews import ggplot, aes
from ggviews.geoms import geom_point, geom_smooth
from ggviews.themes import theme_minimal
from ggviews.facets import facet_grid
from ggviews.scales import scale_color_continuous
import warnings
warnings.filterwarnings('ignore')

# Create equivalent of mpg dataset
np.random.seed(42)
n = 234  # Similar size to mpg dataset

# Simulate mpg-like data
years = [1999, 2008]
drvs = ['4', 'f', 'r']  # 4wd, front-wheel, rear-wheel drive

mpg_data = []
for year in years:
    for drv in drvs:
        n_cars = np.random.randint(15, 25)  # Variable number per category
        
        # Simulate realistic relationships
        base_cty = np.random.normal(18, 4, n_cars)
        base_hwy = base_cty * 1.3 + np.random.normal(0, 2, n_cars)  # Highway usually better
        displ = np.random.uniform(1.5, 7.0, n_cars)  # Engine displacement
        
        # Add realistic effects
        if drv == '4':
            base_cty -= 2  # 4WD typically less efficient
            base_hwy -= 2
        elif drv == 'f':
            base_cty += 1  # FWD typically more efficient
            base_hwy += 1
            
        # Displacement effect (bigger engines = worse mpg)
        base_cty -= (displ - 2.5) * 2
        base_hwy -= (displ - 2.5) * 2
        
        # Ensure reasonable bounds
        base_cty = np.clip(base_cty, 8, 35)
        base_hwy = np.clip(base_hwy, 12, 45)
        
        for i in range(n_cars):
            mpg_data.append({
                'cty': base_cty[i],
                'hwy': base_hwy[i], 
                'displ': displ[i],
                'year': year,
                'drv': drv
            })

mpg = pd.DataFrame(mpg_data)

print("Simulated mpg dataset:")
print(mpg.head(10))
print(f"Shape: {mpg.shape}")
print(f"Years: {sorted(mpg['year'].unique())}")
print(f"Drive types: {sorted(mpg['drv'].unique())}")

print("\n" + "="*80)
print("GGVIEWS IMPLEMENTATION")
print("="*80)

# ggviews equivalent 
print("\nggviews code:")
print("""
plot = (ggplot(mpg, aes(x='cty', y='hwy'))
        .geom_point(aes(color='displ'), alpha=0.7, size=4)
        .geom_smooth(method='lm', color='blue', alpha=0.3)
        .scale_color_continuous(low='#440154', high='#FDE725')  # Viridis-like
        .facet_grid('year ~ drv')
        .theme_minimal()
        .labs(
            title='City vs Highway MPG by Year and Drive Type',
            x='City MPG', 
            y='Highway MPG',
            color='Engine Displacement'
        ))
""")

# Create the plot
plot = (ggplot(mpg, aes(x='cty', y='hwy'))
        .geom_point(aes(color='displ'), alpha=0.7, size=4)
        .geom_smooth(method='lm', color='blue', alpha=0.3)
        .scale_color_continuous(low='#440154', high='#FDE725')  # Viridis-like colors
        .facet_grid('year ~ drv')
        .theme_minimal()
        .labs(
            title='City vs Highway MPG by Year and Drive Type',
            x='City MPG', 
            y='Highway MPG',
            color='Engine Displacement'
        ))

print("✅ ggviews plot created successfully!")

# Try to render and save
try:
    rendered_plot = plot._render()
    print("✅ Plot rendered successfully!")
    
    # Note: In Jupyter, you would just display: plot
    print("\nTo display in Jupyter notebook:")
    print("plot  # or plot.show()")
    
except Exception as e:
    print(f"❌ Rendering error: {e}")

print("\n" + "="*80)
print("COMPARISON WITH GGPLOT2")
print("="*80)

comparison = """
SIMILARITIES ✅:
- Same basic structure: data + aesthetics + geoms + scales + themes + facets
- Scatter points colored by continuous variable (displacement)
- Linear smooth line overlay
- Facet grid with year as rows, drive type as columns
- Minimal theme applied
- Similar color mapping (viridis-inspired)

DIFFERENCES / LIMITATIONS ❌:
1. scale_colour_viridis_c() - I implemented basic continuous scale with viridis-like colors
2. coord_fixed() - Not implemented (would need coordinate system extensions)
3. theme(panel.grid.minor = element_blank()) - Fine-grained theme control not implemented
4. formula = y ~ x - My geom_smooth uses simpler method specification
5. Dataset - Using simulated mpg data vs real mpg dataset

VISUAL COMPARISON:
- ggplot2 original: 6 facets (2 years × 3 drive types), fixed aspect ratio
- ggviews version: Same 6 facets, but proportional aspect ratio
- Both show positive correlation between city and highway mpg
- Both use color gradient for engine displacement
- Both have linear trend lines

STRENGTHS OF GGVIEWS:
✅ Successfully reproduces the core visualization concept
✅ Handles complex faceting (year ~ drv)
✅ Method chaining syntax is more Pythonic
✅ Interactive holoviews backend (vs static ggplot2)
✅ Proper error handling and data validation

AREAS FOR IMPROVEMENT:
- More color scale options (viridis, plasma, etc.)
- Coordinate system transformations
- Fine-grained theme customization
- More statistical transformations
- Better aspect ratio control
"""

print(comparison)

print("\n" + "="*80)
print("FEATURE COMPATIBILITY MATRIX")
print("="*80)

features = [
    ("ggplot(data, aes(...))", "✅ Full support"),
    ("geom_point(aes(color=...))", "✅ Full support"),
    ("geom_smooth(method='lm')", "✅ Supported"),
    ("facet_grid(year ~ drv)", "✅ Full support"),
    ("theme_minimal()", "✅ Full support"),
    ("scale_colour_viridis_c()", "⚠️  Basic continuous scale (viridis-like)"),
    ("coord_fixed()", "❌ Not implemented"),
    ("theme(panel.grid.minor = element_blank())", "❌ Fine-grained theme control not available"),
]

print("ggplot2 Feature → ggviews Support:")
for feature, support in features:
    print(f"  {feature:<40} → {support}")

coverage = len([s for _, s in features if s.startswith("✅")]) / len(features)
print(f"\nOverall compatibility: {coverage:.1%}")

print("\n" + "="*80)
print("NEXT STEPS TO MATCH GGPLOT2")
print("="*80)

next_steps = """
To achieve full ggplot2 compatibility, implement:

1. SCALE SYSTEM EXPANSION:
   - scale_colour_viridis_c/d()
   - scale_colour_brewer()
   - scale_colour_manual() enhancements

2. COORDINATE SYSTEMS:
   - coord_fixed() for aspect ratio control
   - coord_flip() for swapped axes
   - coord_polar() for circular plots

3. THEME SYSTEM ENHANCEMENT:
   - element_blank(), element_text(), element_line()
   - Fine-grained control over plot elements
   - Custom theme builder

4. STATISTICAL TRANSFORMATIONS:
   - More smoothing methods (gam, loess)
   - Statistical summaries (stat_summary)
   - Binning and density estimation improvements

5. ANNOTATION SYSTEM:
   - geom_text() and geom_label()
   - annotate() function
   - Better legend control

The core grammar is solid - these would be incremental improvements!
"""

print(next_steps)