# ggviews Troubleshooting Guide

## Common Issues and Solutions

### 1. Import Errors

**Error:** `ImportError: No module named 'ggviews'`

**Solution:**
```bash
# Make sure you're in the /app directory
cd /app
pip install -e .
```

**Error:** `ImportError: cannot import name 'scale_colour_viridis_d' from 'ggviews.viridis'`

**Solution:** Some imports might not be available in all versions. Try:
```python
# Instead of:
from ggviews.viridis import scale_colour_viridis_d

# Use:
from ggviews import ggplot, aes
plot = ggplot(data).geom_point().scale_colour_viridis_d()
```

### 2. Jupyter Notebook Issues

**Error:** Plots not displaying in Jupyter

**Solution:**
```python
import holoviews as hv
hv.extension('bokeh')  # or 'matplotlib'

# Then create your plot
plot = ggplot(df, aes(x='x', y='y')).geom_point()
plot  # This should display the plot
```

**Error:** `AttributeError: 'ggplot' object has no attribute 'show'`

**Solution:** Remove `.show()` - just use the plot object directly:
```python
# Instead of:
plot.show()

# Use:
plot
```

### 3. Method Chaining Issues

**Error:** `AttributeError: 'ggplot' object has no attribute 'geom_point'`

**Solution:** Make sure you're using the latest version:
```python
# This should work:
plot = (ggplot(df, aes(x='height', y='weight'))
        .geom_point()
        .theme_minimal())

# If not, use + operator:
from ggviews.geoms import geom_point
from ggviews.themes import theme_minimal
plot = ggplot(df, aes(x='height', y='weight')) + geom_point() + theme_minimal()
```

### 4. Data Issues

**Error:** `KeyError: 'column_name'`

**Solution:** Check your column names:
```python
print(df.columns.tolist())  # Check available columns
# Make sure column names match exactly
```

**Error:** `ValueError: x aesthetic is required`

**Solution:** Make sure you specify required aesthetics:
```python
# geom_point requires x and y
ggplot(df, aes(x='height', y='weight')).geom_point()

# geom_histogram requires x
ggplot(df, aes(x='height')).geom_histogram()
```

### 5. Faceting Issues

**Error:** Facets not working or showing empty plots

**Solution:**
```python
# Make sure the faceting variable exists and has multiple values
print(df['species'].value_counts())

# Use proper formula syntax
plot = ggplot(df).geom_point().facet_wrap('~species')  # Correct
plot = ggplot(df).geom_point().facet_wrap('species')   # Also works
```

### 6. Color Scale Issues

**Error:** Colors not appearing or viridis not working

**Solution:**
```python
# Make sure color aesthetic is mapped
ggplot(df, aes(x='x', y='y', color='category')).geom_point()

# For manual colors:
ggplot(df, aes(x='x', y='y', color='category')).geom_point().scale_color_manual(values=['red', 'blue'])
```

## Quick Test

Run this to test if everything is working:

```python
import pandas as pd
import numpy as np
import holoviews as hv
from ggviews import ggplot, aes

hv.extension('bokeh')

# Create test data
df = pd.DataFrame({
    'x': np.random.randn(50),
    'y': np.random.randn(50),
    'category': np.random.choice(['A', 'B'], 50)
})

# Create test plot
plot = (ggplot(df, aes(x='x', y='y', color='category'))
        .geom_point()
        .theme_minimal())

plot  # Should display an interactive plot
```

## Getting Help

If you're still having issues:

1. **Check the examples:** Look in `/app/examples/` for working examples
2. **Test basic functionality:** Run `/app/examples/test_notebook_compatibility.py`
3. **Check your data:** Make sure column names and data types are correct
4. **Try simple plots first:** Start with basic scatter plots before complex visualizations

## Version Information

To check your ggviews version:

```python
import ggviews
print(ggviews.__version__)
```

Current version should be 0.2.0 or higher for full functionality.