# ggviews: A ggplot2-style API for holoviews

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-github--pages-blue.svg)](https://your-username.github.io/ggviews)

ggviews is a comprehensive Python library that uses the ggplot2 grammar of graphics on top of holoviews for interactive visualizations. It is an option among other packages with similar goals like `plotnine` and `lets-plot`. ggviews was developed mostly with vibe coding to fulfill the need for an interactive ggplot2 interface in Pyodide environments.

## Features

- Use the same grammar of graphics you know and love from ggplot2
- Build plots incrementally with method chaining or the `+` operator
- Support for most geom types (point, line, bar, histogram, boxplot, density, map, etc.), faceting, scales and themes
- Colorblind-safe palette via `theme_essi()` and `palette_essi()`
- Label repulsion with `geom_text_repel()` and `geom_label_repel()`
- Conditional highlighting with `gghighlight()`

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

## Quick start

```python
import ggviews as gv
import pandas as pd
import numpy as np

np.random.seed(42)
n = 100
df = pd.DataFrame({
    'height': np.random.normal(170, 10, n),
    'weight': np.random.normal(70, 15, n),
    'species': np.random.choice(['faerie', 'orc', 'saurian'], n),
})
df['weight'] = df['weight'] + 0.5 * (df['height'] - 170) + np.random.normal(0, 5, n)
```

### Method chaining (fluent style)

```python
(
    gv.ggplot(df, gv.aes(x='height', y='weight', color='species'))
    .geom_point(alpha=0.7)
    .geom_smooth(method='lm')
    .facet_wrap('~species')
    .theme_essi()
    .labs(
        title='Height vs Weight by Species',
        x='Height (cm)',
        y='Weight (kg)',
    )
)
```

### `+` operator (ggplot2 style)

```python
(
    gv.ggplot(df, gv.aes(x='height', y='weight', color='species'))
    + gv.geom_point(alpha=0.7)
    + gv.geom_smooth(method='lm')
    + gv.facet_wrap('~species')
    + gv.theme_essi()
    + gv.labs(
        title='Height vs Weight by Species',
        x='Height (cm)',
        y='Weight (kg)',
    )
)
```

Both styles produce identical results. Method chaining reads like a pipeline; the `+` operator mirrors R's ggplot2 syntax.

## More examples

### Boxplot with coord_flip

```python
(
    gv.ggplot(df, gv.aes(x='species', y='height'))
    .geom_boxplot()
    .coord_flip()
    .theme_minimal()
    .labs(title='Height Distribution', x='Species', y='Height (cm)')
)
```

### Highlight a subset

```python
(
    gv.ggplot(df, gv.aes(x='height', y='weight'))
    .geom_point()
    .gghighlight("species == 'orc'")
    .labs(title='Orcs highlighted')
)
```

### Repelled labels

```python
top5 = df.nlargest(5, 'weight').assign(label=lambda d: d['species'])

(
    gv.ggplot(top5, gv.aes(x='height', y='weight', label='label'))
    .geom_point()
    .geom_text_repel()
    .labs(title='Top 5 by Weight')
)
```

### Facet grid

```python
(
    gv.ggplot(df, gv.aes(x='height', y='weight'))
    .geom_point(alpha=0.5)
    .geom_smooth(method='lm')
    .facet_wrap('~species', ncol=2)
    .theme_classic()
)
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- Inspired by Hadley Wickham's [ggplot2](https://ggplot2.tidyverse.org/)
- Built on the [holoviews](http://holoviews.org/) library
- Colorblind-safe palette by [Martin Krzywinski](http://mkweb.bcgsc.ca/colorblind/)
- Kudos to the broader Python data visualization community
