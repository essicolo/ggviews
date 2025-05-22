"""
Basic and advanced examples demonstrating the use of ggviews.

This example shows how to create various types of plots with ggviews.
"""

# %%
from ggviews import ggplot, aes, load_dataset
mtcars = load_dataset('mtcars')
ggplot(mtcars, aes(x='wt', y='mpg')).geom_point(aes(color='cyl'), size=5, alpha=0.7).theme_ggplot2()

# %%
from ggviews import ggplot, aes, load_dataset
mtcars = load_dataset('mtcars')
(
    ggplot(mtcars, aes(x='hp', y='qsec', color='am'))
    .geom_point(size=5, alpha=0.7)
    .scale_x_log10()
    .labs(
        title='Horsepower vs. Quarter Mile Time',
        subtitle='With Transmission Type as Color',
        x='Horsepower (log scale)',
        y='Quarter Mile Time (s)'
    )
    .theme_ggplot2()
)
# %%
from ggviews import ggplot, aes, load_dataset
mtcars = load_dataset('mtcars')
gear_mpg = mtcars.groupby('gear')['mpg'].mean().reset_index()
(
    ggplot(gear_mpg, aes(x='gear', y='mpg'))
    .geom_bar(stat='identity', fill='skyblue', color='black')
    .labs(
        title='Average MPG by Number of Gears',
        x='Number of Gears',
        y='Average Miles per Gallon'
    )
)

# %%
from ggviews import ggplot, aes, load_dataset
diamonds = load_dataset('diamonds')
(
    ggplot(diamonds, aes(x='price'))
    .geom_histogram(bins=50, fill='pink', color='black')
    .labs(
        title='Distribution of Diamond Prices',
        x='Price ($)',
        y='Count'
    )
    .theme_minimal()
)

# %%
import holoviews as hv
diamonds = load_dataset('diamonds')

hv.Scatter(
    diamonds.sample(500),
    kdims=['carat'],
    vdims=['price', 'cut', 'color'],
    label='Diamonds'
).groupby('cut').layout()

# %%
import holoviews as hv
diamonds = load_dataset('diamonds')
hv.Scatter(
    diamonds.sample(500),
    kdims=['carat'],
    vdims=['price', 'cut', 'color'],
    label='Diamonds'
).groupby(['cut', 'color']).layout()

# %%
from ggviews import ggplot, aes, load_dataset
diamonds = load_dataset('diamonds')
(
    ggplot(diamonds.sample(500), aes(x='price', y='carat'))
    .geom_point()
    .facet_wrap('cut')
)

# %%
from ggviews import ggplot, aes, load_dataset
diamonds = load_dataset('diamonds')
(
    ggplot(diamonds.sample(500), aes(x='price'))
    .geom_histogram(bins=50, fill='pink', color='black')
    .facet_wrap('cut', scales='free')
)

# %%
from ggviews import ggplot, aes, load_dataset
diamonds = load_dataset('diamonds')
(
    ggplot(diamonds.sample(500), aes(x='price', y='carat'))
    .geom_point()
    .facet_grid(row='cut', col='color')
)


# %%
import pandas as pd
from ggviews import ggplot, aes, load_dataset
economics = load_dataset('economics')
economics['year'] = pd.to_datetime(economics['date']).dt.year
(
    ggplot(economics, aes(x='year', y='unemploy'))
    .geom_line(color='blue', size=1.5)
    .geom_point(color='red', size=3)
    .labs(
        title='US Unemployment Rate Over Time',
        x='Year',
        y='Unemployment Rate'
    )
    .theme_bw()
)
# %%
