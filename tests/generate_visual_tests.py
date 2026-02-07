"""
Visual comparison test: Generate focused ggviews PNGs for structural review.

Each test case produces a PNG image that can be visually compared against
what ggplot2 would produce for the equivalent R code.  The R code is stored
alongside the PNG for reference.

Focus areas (NOT color): canvas/margins, axis labels/ticks, text positions,
legend placement, facet layout, panel spacing, title alignment.
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd

# Use matplotlib backend for static PNG export
import holoviews as hv
hv.extension('matplotlib')

# ── output directory ──────────────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(__file__), '..', 'visual_tests')
os.makedirs(OUT, exist_ok=True)


def save(plot, name, r_code=""):
    """Save a HoloViews plot as PNG and write companion R code."""
    png_path = os.path.join(OUT, f'{name}.png')
    r_path   = os.path.join(OUT, f'{name}.R')
    try:
        hv.save(plot, png_path, fmt='png')
        print(f"  [OK] {name}.png")
    except Exception as e:
        print(f"  [FAIL] {name}.png — {e}")
    if r_code:
        with open(r_path, 'w') as f:
            f.write(r_code.strip() + '\n')


# ── data ──────────────────────────────────────────────────────────────────────
np.random.seed(42)

iris = pd.DataFrame({
    'sepal_length': np.concatenate([
        np.random.normal(5.0, 0.35, 50),
        np.random.normal(5.9, 0.52, 50),
        np.random.normal(6.6, 0.64, 50),
    ]),
    'sepal_width': np.concatenate([
        np.random.normal(3.4, 0.38, 50),
        np.random.normal(2.8, 0.31, 50),
        np.random.normal(3.0, 0.32, 50),
    ]),
    'species': ['setosa'] * 50 + ['versicolor'] * 50 + ['virginica'] * 50,
})

tips = pd.DataFrame({
    'total_bill': np.random.uniform(10, 50, 80),
    'tip': np.random.uniform(1, 10, 80),
    'day': np.random.choice(['Thu', 'Fri', 'Sat', 'Sun'], 80),
    'sex': np.random.choice(['Male', 'Female'], 80),
    'smoker': np.random.choice(['Yes', 'No'], 80),
})

economics = pd.DataFrame({
    'date': pd.date_range('2000-01-01', periods=60, freq='MS'),
    'unemploy': np.cumsum(np.random.normal(0, 500, 60)) + 8000,
    'pop': np.linspace(280e6, 310e6, 60),
})


# ══════════════════════════════════════════════════════════════════════════════
# TEST CASES
# ══════════════════════════════════════════════════════════════════════════════

# Switch back to bokeh for building plots, then export via matplotlib
hv.extension('bokeh')
from ggviews import (
    ggplot, aes,
    geom_point, geom_line, geom_bar, geom_histogram, geom_smooth,
    geom_boxplot, geom_density, geom_text, geom_label,
    geom_text_repel, geom_label_repel,
    facet_wrap, facet_grid,
    labs, theme_minimal, theme_classic, theme_bw,
    coord_flip, gghighlight,
)

def render(p):
    """Get the HoloViews object from a ggplot."""
    return p._render()

print("Generating visual test images...\n")

# ── 1. Basic scatter ─────────────────────────────────────────────────────────
print("[1] Basic scatter")
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + labs(title='Sepal Length vs Width', x='Sepal Length (cm)', y='Sepal Width (cm)'))
hv.extension('matplotlib')
save(render(p), '01_scatter_basic', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  labs(title='Sepal Length vs Width', x='Sepal Length (cm)', y='Sepal Width (cm)')
ggsave('01_scatter_basic.png', width=5, height=4)
""")

# ── 2. Scatter with group color ──────────────────────────────────────────────
print("[2] Scatter with color grouping")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species'))
     + geom_point()
     + labs(title='Iris by Species'))
hv.extension('matplotlib')
save(render(p), '02_scatter_color', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width, color=Species)) +
  geom_point() +
  labs(title='Iris by Species')
ggsave('02_scatter_color.png', width=6, height=4)
""")

# ── 3. Bar chart (count) ─────────────────────────────────────────────────────
print("[3] Bar chart (count)")
hv.extension('bokeh')
p = (ggplot(tips, aes(x='day'))
     + geom_bar()
     + labs(title='Tips by Day', x='Day of Week', y='Count'))
hv.extension('matplotlib')
save(render(p), '03_bar_count', r_code="""
library(ggplot2)
ggplot(tips, aes(x=day)) +
  geom_bar() +
  labs(title='Tips by Day', x='Day of Week', y='Count')
ggsave('03_bar_count.png', width=5, height=4)
""")

# ── 4. Histogram ─────────────────────────────────────────────────────────────
print("[4] Histogram")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length'))
     + geom_histogram(bins=15)
     + labs(title='Distribution of Sepal Length', x='Sepal Length', y='Count'))
hv.extension('matplotlib')
save(render(p), '04_histogram', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length)) +
  geom_histogram(bins=15) +
  labs(title='Distribution of Sepal Length', x='Sepal Length', y='Count')
ggsave('04_histogram.png', width=5, height=4)
""")

# ── 5. Line plot ─────────────────────────────────────────────────────────────
print("[5] Line plot")
hv.extension('bokeh')
line_df = pd.DataFrame({'x': range(20), 'y': np.cumsum(np.random.normal(0, 1, 20))})
p = (ggplot(line_df, aes(x='x', y='y'))
     + geom_line()
     + labs(title='Random Walk', x='Step', y='Value'))
hv.extension('matplotlib')
save(render(p), '05_line', r_code="""
library(ggplot2)
df <- data.frame(x=0:19, y=cumsum(rnorm(20)))
ggplot(df, aes(x=x, y=y)) +
  geom_line() +
  labs(title='Random Walk', x='Step', y='Value')
ggsave('05_line.png', width=5, height=4)
""")

# ── 6. Scatter + smooth ─────────────────────────────────────────────────────
print("[6] Scatter + smooth (lm)")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + geom_smooth(method='lm')
     + labs(title='Sepal Dimensions with Linear Fit'))
hv.extension('matplotlib')
save(render(p), '06_scatter_smooth', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  geom_smooth(method='lm') +
  labs(title='Sepal Dimensions with Linear Fit')
ggsave('06_scatter_smooth.png', width=5, height=4)
""")

# ── 7. Boxplot ───────────────────────────────────────────────────────────────
print("[7] Boxplot")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='species', y='sepal_length'))
     + geom_boxplot()
     + labs(title='Sepal Length by Species', x='Species', y='Sepal Length'))
hv.extension('matplotlib')
save(render(p), '07_boxplot', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Species, y=Sepal.Length)) +
  geom_boxplot() +
  labs(title='Sepal Length by Species', x='Species', y='Sepal Length')
ggsave('07_boxplot.png', width=5, height=4)
""")

# ── 8. Density plot ──────────────────────────────────────────────────────────
print("[8] Density plot")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length'))
     + geom_density()
     + labs(title='Sepal Length Density', x='Sepal Length', y='Density'))
hv.extension('matplotlib')
save(render(p), '08_density', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length)) +
  geom_density() +
  labs(title='Sepal Length Density', x='Sepal Length', y='Density')
ggsave('08_density.png', width=5, height=4)
""")

# ── 9. Text labels ──────────────────────────────────────────────────────────
print("[9] Text labels")
hv.extension('bokeh')
label_df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 1],
    'name': ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'],
})
p = (ggplot(label_df, aes(x='x', y='y', label='name'))
     + geom_point()
     + geom_text()
     + labs(title='Points with Labels'))
hv.extension('matplotlib')
save(render(p), '09_text_labels', r_code="""
library(ggplot2)
df <- data.frame(x=c(1,2,3,4,5), y=c(2,4,3,5,1),
                 name=c('Alpha','Beta','Gamma','Delta','Epsilon'))
ggplot(df, aes(x=x, y=y, label=name)) +
  geom_point() +
  geom_text() +
  labs(title='Points with Labels')
ggsave('09_text_labels.png', width=5, height=4)
""")

# ── 10. Facet wrap ───────────────────────────────────────────────────────────
print("[10] Facet wrap (3 panels)")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + facet_wrap('species')
     + labs(title='Faceted by Species'))
hv.extension('matplotlib')
save(render(p), '10_facet_wrap', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  facet_wrap(~Species) +
  labs(title='Faceted by Species')
ggsave('10_facet_wrap.png', width=9, height=4)
""")

# ── 11. Facet wrap ncol=2 ───────────────────────────────────────────────────
print("[11] Facet wrap ncol=2 (4 panels)")
hv.extension('bokeh')
p = (ggplot(tips, aes(x='total_bill', y='tip'))
     + geom_point()
     + facet_wrap('day', ncol=2)
     + labs(title='Tips by Day (2 columns)'))
hv.extension('matplotlib')
save(render(p), '11_facet_wrap_ncol2', r_code="""
library(ggplot2)
ggplot(tips, aes(x=total_bill, y=tip)) +
  geom_point() +
  facet_wrap(~day, ncol=2) +
  labs(title='Tips by Day (2 columns)')
ggsave('11_facet_wrap_ncol2.png', width=8, height=6)
""")

# ── 12. Facet grid ──────────────────────────────────────────────────────────
print("[12] Facet grid (sex ~ smoker)")
hv.extension('bokeh')
p = (ggplot(tips, aes(x='total_bill', y='tip'))
     + geom_point()
     + facet_grid('sex ~ smoker')
     + labs(title='Tips: Sex vs Smoker Grid'))
hv.extension('matplotlib')
save(render(p), '12_facet_grid', r_code="""
library(ggplot2)
ggplot(tips, aes(x=total_bill, y=tip)) +
  geom_point() +
  facet_grid(sex ~ smoker) +
  labs(title='Tips: Sex vs Smoker Grid')
ggsave('12_facet_grid.png', width=7, height=5)
""")

# ── 13. Facet wrap with bars ─────────────────────────────────────────────────
print("[13] Facet wrap with bar chart")
hv.extension('bokeh')
p = (ggplot(tips, aes(x='day'))
     + geom_bar()
     + facet_wrap('sex')
     + labs(title='Day counts by Sex'))
hv.extension('matplotlib')
save(render(p), '13_facet_bars', r_code="""
library(ggplot2)
ggplot(tips, aes(x=day)) +
  geom_bar() +
  facet_wrap(~sex) +
  labs(title='Day counts by Sex')
ggsave('13_facet_bars.png', width=8, height=4)
""")

# ── 14. Coord flip ──────────────────────────────────────────────────────────
print("[14] Coord flip")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='species', y='sepal_length'))
     + geom_boxplot()
     + coord_flip()
     + labs(title='Horizontal Boxplot'))
hv.extension('matplotlib')
save(render(p), '14_coord_flip', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Species, y=Sepal.Length)) +
  geom_boxplot() +
  coord_flip() +
  labs(title='Horizontal Boxplot')
ggsave('14_coord_flip.png', width=5, height=4)
""")

# ── 15. Theme minimal ───────────────────────────────────────────────────────
print("[15] Theme minimal")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + theme_minimal()
     + labs(title='Minimal Theme'))
hv.extension('matplotlib')
save(render(p), '15_theme_minimal', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  theme_minimal() +
  labs(title='Minimal Theme')
ggsave('15_theme_minimal.png', width=5, height=4)
""")

# ── 16. Theme classic ───────────────────────────────────────────────────────
print("[16] Theme classic")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + theme_classic()
     + labs(title='Classic Theme'))
hv.extension('matplotlib')
save(render(p), '16_theme_classic', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  theme_classic() +
  labs(title='Classic Theme')
ggsave('16_theme_classic.png', width=5, height=4)
""")

# ── 17. Repel labels ────────────────────────────────────────────────────────
print("[17] Repel labels")
hv.extension('bokeh')
p = (ggplot(label_df, aes(x='x', y='y', label='name'))
     + geom_point()
     + geom_text_repel()
     + labs(title='Repelled Labels'))
hv.extension('matplotlib')
save(render(p), '17_repel_labels', r_code="""
library(ggplot2)
library(ggrepel)
df <- data.frame(x=c(1,2,3,4,5), y=c(2,4,3,5,1),
                 name=c('Alpha','Beta','Gamma','Delta','Epsilon'))
ggplot(df, aes(x=x, y=y, label=name)) +
  geom_point() +
  geom_text_repel() +
  labs(title='Repelled Labels')
ggsave('17_repel_labels.png', width=5, height=4)
""")

# ── 18. Highlight ────────────────────────────────────────────────────────────
print("[18] Highlight")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + gghighlight("species == 'setosa'")
     + labs(title='Highlighted: setosa'))
hv.extension('matplotlib')
save(render(p), '18_highlight', r_code="""
library(ggplot2)
library(gghighlight)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  gghighlight(Species == 'setosa') +
  labs(title='Highlighted: setosa')
ggsave('18_highlight.png', width=5, height=4)
""")

# ── 19. Multi-layer: points + smooth + facets ────────────────────────────────
print("[19] Multi-layer: points + smooth + facets")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + geom_smooth(method='lm')
     + facet_wrap('species')
     + labs(title='Linear Fits by Species'))
hv.extension('matplotlib')
save(render(p), '19_multi_layer_facets', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  geom_smooth(method='lm') +
  facet_wrap(~Species) +
  labs(title='Linear Fits by Species')
ggsave('19_multi_layer_facets.png', width=9, height=4)
""")

# ── 20. Axis labels + title positioning ──────────────────────────────────────
print("[20] Axis labels + title")
hv.extension('bokeh')
p = (ggplot(iris, aes(x='sepal_length', y='sepal_width'))
     + geom_point()
     + labs(title='Main Title Here',
            x='X Axis Label (units)',
            y='Y Axis Label (units)'))
hv.extension('matplotlib')
save(render(p), '20_labels_title', r_code="""
library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  labs(title='Main Title Here',
       x='X Axis Label (units)',
       y='Y Axis Label (units)')
ggsave('20_labels_title.png', width=5, height=4)
""")


print(f"\nDone! {len(os.listdir(OUT))} files in {os.path.abspath(OUT)}")
