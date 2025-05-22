"""
Examples demonstrating faceting with ggviews.

This example shows how to use facet_grid and facet_wrap for creating multi-panel plots.
"""
import pandas as pd
import numpy as np
import holoviews as hv
hv.extension('bokeh')

# Try to use our package, but if it's not installed, add source directory to path 
try:
    from ggviews import ggplot, aes, load_dataset
    from ggviews import facet_grid, facet_wrap
    from ggviews import theme_minimal
except ImportError:
    # Mock implementation for demonstration purposes
    from pathlib import Path
    import sys
    
    # Add the parent directory to sys.path
    sys.path.append(str(Path(__file__).parent.parent))
    
    # Import from our package
    from src.ggviews import ggplot, aes
    from src.ggviews import facet_grid, facet_wrap
    from src.ggviews import theme_minimal
    from src.ggviews.data_loader import load_dataset


def facet_grid_example():
    """Example using facet_grid to create a multi-panel plot by row and column."""
    # Load the diamonds dataset
    mpg = load_dataset('mpg')
    
    # Create a scatter plot with faceting by transmission and cylinder count
    plot = (ggplot(mpg, aes(x='displ', y='hwy', color='class'))
        .geom_point(size=4, alpha=0.7)
        .facet_grid(row='drv', col='cyl')
        .labs(
            title='Highway MPG vs. Engine Displacement',
            subtitle='Faceted by Drive Type (rows) and Cylinders (columns)',
            x='Engine Displacement (L)',
            y='Highway MPG'
        )
        .theme_minimal()
    )
    
    # Save the plot as HTML
    hv_plot = plot.build()
    hv.save(hv_plot, 'facet_grid_example.html')
    
    print("Plot saved as facet_grid_example.html")
    
    return plot


def facet_wrap_example():
    """Example using facet_wrap to create a wrapped multi-panel plot."""
    # Load the diamonds dataset
    mpg = load_dataset('mpg')
    
    # Create a scatter plot with faceting by manufacturer
    plot = (ggplot(mpg, aes(x='cty', y='hwy', color='drv'))
        .geom_point(size=3, alpha=0.7)
        .facet_wrap('manufacturer', ncol=3)
        .labs(
            title='City vs Highway MPG by Manufacturer',
            x='City MPG',
            y='Highway MPG'
        )
        .theme_minimal()
    )
    
    # Save the plot as HTML
    hv_plot = plot.build()
    hv.save(hv_plot, 'facet_wrap_example.html')
    
    print("Plot saved as facet_wrap_example.html")
    
    return plot


def main():
    """Run all examples."""
    print("Running ggviews faceting examples...")
    
    try:
        facet_grid_example()
    except Exception as e:
        print(f"Error in facet_grid example: {e}")
    
    try:
        facet_wrap_example()
    except Exception as e:
        print(f"Error in facet_wrap example: {e}")
    
    print("All faceting examples completed!")


if __name__ == "__main__":
    main()