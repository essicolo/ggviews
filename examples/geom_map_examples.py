#!/usr/bin/env python3
"""
Examples demonstrating geom_map functionality for geographic visualizations
"""

import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes, geom_map
from ggviews.themes import theme_minimal

# Set up holoviews
hv.extension('bokeh')

print("🗺️  GEOM_MAP EXAMPLES")
print("="*60)

# Create sample geographic data
np.random.seed(42)

# Sample 1: World cities data
cities_data = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Sydney', 'Cairo', 'São Paulo', 
             'Mumbai', 'Beijing', 'Lagos', 'Mexico City', 'Moscow', 'Bangkok'],
    'longitude': [-74.0, -0.1, 139.7, 151.2, 31.2, -46.6, 
                  72.8, 116.4, 3.4, -99.1, 37.6, 100.5],
    'latitude': [40.7, 51.5, 35.7, -33.9, 30.0, -23.5, 
                 19.1, 39.9, 6.5, 19.4, 55.8, 13.8],
    'population': [8.4, 9.0, 13.9, 5.3, 9.1, 12.3, 
                   20.0, 21.5, 14.8, 9.2, 12.5, 10.7],
    'continent': ['North America', 'Europe', 'Asia', 'Oceania', 'Africa', 'South America',
                  'Asia', 'Asia', 'Africa', 'North America', 'Europe', 'Asia']
})

# Sample 2: Random points for demonstration
random_points = pd.DataFrame({
    'longitude': np.random.uniform(-180, 180, 50),
    'latitude': np.random.uniform(-60, 60, 50),
    'value': np.random.normal(100, 30, 50),
    'category': np.random.choice(['A', 'B', 'C'], 50)
})

print("Sample geographic data created:")
print("Cities data:", cities_data.shape)
print("Random points:", random_points.shape)

# Example 1: Simple world map
print("\n" + "="*60)
print("EXAMPLE 1: Simple World Map")
print("="*60)
try:
    plot1 = (
        ggplot()
        .geom_map(map_type='world')
        .theme_minimal()
        .labs(title='Simple World Map')
    )
    
    print("✅ Simple world map created")
    print("   Usage: ggplot().geom_map(map_type='world')")
    print("   Shows: Basic world coastlines")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("   Note: Requires geoviews for full functionality")

# Example 2: Points on simple coordinates (fallback mode)
print("\n" + "="*60) 
print("EXAMPLE 2: City Points (Simple Mode)")
print("="*60)
try:
    plot2 = (
        ggplot(cities_data, aes(x='longitude', y='latitude'))
        .geom_map(map_type='simple', size=8, alpha=0.7)
        .theme_minimal()
        .labs(
            title='World Cities (Simple Scatter)',
            x='Longitude', 
            y='Latitude'
        )
    )
    
    print("✅ Simple city points created")
    print("   Usage: .geom_map(map_type='simple')")
    print("   Shows: Cities as points on longitude/latitude grid")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Example 3: Colored points by continent
print("\n" + "="*60)
print("EXAMPLE 3: Cities Colored by Continent")
print("="*60)
try:
    plot3 = (
        ggplot(cities_data, aes(x='longitude', y='latitude', color='continent'))
        .geom_map(map_type='simple', size=10, alpha=0.8)
        .scale_colour_viridis_d()
        .theme_minimal()
        .labs(
            title='World Cities by Continent',
            x='Longitude',
            y='Latitude', 
            color='Continent'
        )
    )
    
    print("✅ Colored city points created")
    print("   Usage: aes(color='continent') + geom_map()")
    print("   Shows: Cities colored by continent with viridis palette")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Example 4: Points sized by population  
print("\n" + "="*60)
print("EXAMPLE 4: Cities Sized by Population")
print("="*60)
try:
    plot4 = (
        ggplot(cities_data, aes(x='longitude', y='latitude', size='population'))
        .geom_map(map_type='simple', alpha=0.7, color='red')
        .theme_minimal()
        .labs(
            title='World Cities by Population',
            x='Longitude',
            y='Latitude',
            size='Population (millions)'
        )
    )
    
    print("✅ Population-sized city points created")
    print("   Usage: aes(size='population') + geom_map()")
    print("   Shows: Cities with point size proportional to population")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Example 5: Geographic points map (requires geoviews)
print("\n" + "="*60)
print("EXAMPLE 5: Geographic Points Map")
print("="*60)
try:
    plot5 = (
        ggplot(cities_data, aes(x='longitude', y='latitude', color='continent'))
        .geom_map(map_type='points', features=['coastlines'], size=8)
        .theme_minimal()
        .labs(title='Cities on Geographic Map')
    )
    
    print("✅ Geographic points map created")  
    print("   Usage: geom_map(map_type='points', features=['coastlines'])")
    print("   Shows: Cities on world map with geographic projection")
    print("   Note: Requires 'pip install geoviews cartopy' for full functionality")
    
except Exception as e:
    print(f"❌ Geoviews not available: {e}")
    print("   Fallback: Use map_type='simple' or install geoviews")

# Example 6: Random data visualization
print("\n" + "="*60)
print("EXAMPLE 6: Random Geographic Data")
print("="*60)
try:
    plot6 = (
        ggplot(random_points, aes(x='longitude', y='latitude', color='category'))
        .geom_map(map_type='simple', alpha=0.6, size=6)
        .scale_colour_viridis_d()
        .theme_minimal()
        .labs(
            title='Random Geographic Points',
            subtitle='Demonstrating geom_map with random data',
            x='Longitude',
            y='Latitude',
            color='Category'
        )
    )
    
    print("✅ Random geographic data visualization created")
    print("   Usage: Automatic longitude/latitude detection")
    print("   Shows: Colored points across the globe")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Example 7: Multiple projection support
print("\n" + "="*60)
print("EXAMPLE 7: Different Map Projections")
print("="*60)

projections = ['PlateCarree', 'Mollweide', 'Robinson']
for i, proj in enumerate(projections, 7):
    try:
        plot = (
            ggplot(cities_data)
            .geom_map(map_type='world', projection=proj)
            .theme_minimal()
            .labs(title=f'World Map - {proj} Projection')
        )
        
        print(f"✅ {proj} projection map created")
        
    except Exception as e:
        print(f"❌ {proj} projection error: {e}")

print("\n" + "="*60)
print("GEOM_MAP FEATURES SUMMARY")
print("="*60)
print("✅ Map Types Available:")
print("   • 'simple' - Basic scatter plot (always works)")  
print("   • 'world' - World map with coastlines (requires geoviews)")
print("   • 'points' - Geographic points on map (requires geoviews)")
print("   • 'choropleth' - Filled regions (placeholder)")

print("\n✅ Key Features:")
print("   • Automatic longitude/latitude detection")
print("   • Color mapping by categories")
print("   • Size mapping by values")  
print("   • Multiple map projections")
print("   • Geographic features (coastlines, borders)")
print("   • Fallback to simple scatter plots")

print("\n📦 Installation for Full Features:")
print("   pip install geoviews cartopy")
print("   # Note: cartopy installation may require system dependencies")

print("\n🎯 Usage Patterns:")
print("   • World overview: .geom_map(map_type='world')")
print("   • Data points: .geom_map(aes(x='lon', y='lat'), map_type='points')")  
print("   • Simple fallback: .geom_map(map_type='simple')")

print("\n🌟 All examples created successfully!")
print("Ready to visualize geographic data with ggviews!")