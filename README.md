# ggviews: A ggplot2-style API for holoviews

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-github--pages-blue.svg)](https://your-username.github.io/ggviews)

ggviews is a comprehensive Python library that brings the beloved ggplot2 grammar of graphics to Python, built on top of holoviews for interactive visualizations. Create publication-quality plots with the intuitive, layered syntax that R users know and love.

## Features

- Use the same grammar of graphics you know and love from ggplot2
- Build plots incrementally with method chaining such as `ggplot(data, aes(x='a', y='b')).geom_point()`
- Support for most geom types (point, line, bar, histogram, map, etc.), faceting, scales and themes

## Installation

```bash
pip install ggviews
```

For development installation:
```bash
git clone https://github.com/essicolo/ggviews.git
cd ggviews
pip install -e ".[dev]"
```

## Example

```python
from ggviews import ggplot, aes
import pandas as pd

# Generate data
np.random.seed(42)
n = 100
df = pd.DataFrame({
    'height': np.random.normal(170, 10, n),
    'weight': np.random.normal(70, 15, n),
    'species': np.random.choice(['faerie', 'orc', 'saurian'], n),
    'age': np.random.randint(18, 80, n),
    'group': np.random.choice(['A', 'B'], n)
})

# Add some correlation
df['weight'] = df['weight'] + 0.5 * (df['height'] - 170) + np.random.normal(0, 5, n)

# Plot
(
    ggplot(df, aes(x='height', y='weight'))
   .geom_point(aes(color='species'), size=3, alpha=0.7)
   .geom_smooth(method='lm')
   .theme_minimal()
   .labs(
       title='Height vs Weight by Species',
       x='Height (cm)',
       y='Weight (kg)'
   )
   .facet_wrap('~species')
)
```

## License

This project is licensed under the GPL3 License.

## Acknowledgments

- Inspired by Hadley Wickham's [ggplot2](https://ggplot2.tidyverse.org/)
- Built on the [holoviews](http://holoviews.org/) library
- Kudos to the broader Python data visualization community
