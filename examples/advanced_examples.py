"""
Advanced examples for ggviews

This script demonstrates more advanced features including
complex faceting, custom themes, and statistical layers.
"""

import pandas as pd
import numpy as np
from ggviews import ggplot, aes
from ggviews.geoms import (geom_point, geom_line, geom_bar, geom_histogram, 
                          geom_boxplot, geom_smooth, geom_density)
from ggviews.themes import theme_minimal, theme_classic, theme_dark, theme_bw
from ggviews.scales import (scale_color_manual, scale_color_continuous, 
                           scale_x_continuous, scale_y_continuous)
from ggviews.facets import facet_wrap, facet_grid
from ggviews.utils import labs, xlim, ylim, guides

# Create more complex sample data
np.random.seed(123)
n = 200

# Simulate experimental data
experimental_data = pd.DataFrame({
    'treatment': np.tile(['Control', 'Treatment A', 'Treatment B'], n//3 + 1)[:n],
    'dose': np.tile([0.1, 0.5, 1.0, 2.0], n//4 + 1)[:n],
    'response': np.random.normal(0, 1, n),
    'batch': np.random.choice(['Batch1', 'Batch2', 'Batch3'], n),
    'subject_id': range(n),
    'time': np.random.uniform(0, 24, n),
    'biomarker': np.random.lognormal(0, 1, n)
})

# Add some realistic effects
experimental_data['response'] += np.where(
    experimental_data['treatment'] == 'Treatment A', 
    experimental_data['dose'] * 0.5, 0
)
experimental_data['response'] += np.where(
    experimental_data['treatment'] == 'Treatment B', 
    experimental_data['dose'] * 0.8 + np.random.normal(0, 0.2, n), 0
)

print("Advanced experimental data:")
print(experimental_data.head())
print(f"Data shape: {experimental_data.shape}")

# Advanced Example 1: Complex faceted plot with multiple aesthetics
print("\n=== Advanced Example 1: Complex Faceted Analysis ===")
p1 = (ggplot(experimental_data, aes(x='dose', y='response', color='treatment'))
      + geom_point(alpha=0.6, size=3)
      + geom_smooth(method='lm', se=False)
      + facet_grid('batch ~ treatment')
      + theme_bw()
      + scale_color_manual(values=['#1B4F72', '#E74C3C', '#F39C12'])
      + labs(title='Treatment Response by Dose and Batch',
             subtitle='Linear regression lines fitted for each treatment',
             x='Dose (mg)', 
             y='Response Score',
             color='Treatment Group'))
print("Created complex faceted analysis plot")

# Advanced Example 2: Multiple layer plot with different data
print("\n=== Advanced Example 2: Multiple Layers, Different Data ===")
# Summarize data for overlay
summary_data = (experimental_data
                .groupby(['treatment', 'dose'])
                .agg({
                    'response': ['mean', 'std'],
                    'subject_id': 'count'
                })
                .reset_index())
summary_data.columns = ['treatment', 'dose', 'mean_response', 'std_response', 'n']

p2 = (ggplot(experimental_data, aes(x='dose', y='response'))
      + geom_point(aes(color='treatment'), alpha=0.3, size=2)
      + geom_line(data=summary_data, mapping=aes(x='dose', y='mean_response', color='treatment'), 
                  size=3)
      + geom_point(data=summary_data, mapping=aes(x='dose', y='mean_response', color='treatment'), 
                   size=5)
      + theme_minimal()
      + labs(title='Individual Points with Group Means',
             x='Dose (mg)',
             y='Response Score'))
print("Created multi-layer plot with summary overlay")

# Advanced Example 3: Continuous color scale
print("\n=== Advanced Example 3: Continuous Color Scale ===")
p3 = (ggplot(experimental_data, aes(x='time', y='biomarker', color='response'))
      + geom_point(size=4, alpha=0.7)
      + scale_color_continuous(low='blue', high='red', mid='white')
      + theme_dark()
      + labs(title='Biomarker Levels Over Time',
             subtitle='Colored by treatment response',
             x='Time (hours)',
             y='Biomarker Level',
             color='Response'))
print("Created continuous color scale plot")

# Advanced Example 4: Statistical summaries
print("\n=== Advanced Example 4: Box Plots and Violin Plots ===")
p4 = (ggplot(experimental_data, aes(x='treatment', y='response'))
      + geom_boxplot(alpha=0.7, fill='lightblue')
      + geom_point(aes(color='batch'), alpha=0.6, size=2, 
                   position='jitter')  # Note: position jitter not implemented yet
      + theme_classic()
      + labs(title='Treatment Response Distribution',
             x='Treatment Group',
             y='Response Score',
             color='Batch'))
print("Created box plot with overlaid points")

# Advanced Example 5: Density plots
print("\n=== Advanced Example 5: Density Overlays ===")
p5 = (ggplot(experimental_data, aes(x='response', fill='treatment'))
      + geom_density(alpha=0.5)
      + scale_color_manual(values=['#3498DB', '#E74C3C', '#F39C12'])
      + theme_minimal()
      + labs(title='Response Distribution by Treatment',
             x='Response Score',
             y='Density',
             fill='Treatment'))
print("Created density plot with filled areas")

# Advanced Example 6: Custom axis scales
print("\n=== Advanced Example 6: Custom Scales ===")
p6 = (ggplot(experimental_data, aes(x='dose', y='biomarker'))
      + geom_point(aes(color='treatment'), alpha=0.6, size=3)
      + scale_x_continuous(
          name='Dose (mg)',
          breaks=[0.1, 0.5, 1.0, 2.0],
          labels=['Low', 'Medium', 'High', 'Very High']
      )
      + scale_y_continuous(
          name='Biomarker (log scale)',
          trans='log'
      )
      + theme_minimal()
      + labs(title='Dose-Response with Custom Scales'))
print("Created plot with custom axis scales")

# Advanced Example 7: Facet wrap with multiple variables
print("\n=== Advanced Example 7: Multi-variable Faceting ===")
p7 = (ggplot(experimental_data, aes(x='time', y='response'))
      + geom_point(aes(color='dose'), alpha=0.6)
      + geom_smooth(se=False, color='black', linetype='dashed')
      + facet_wrap(['treatment', 'batch'], ncol=3)
      + theme_bw()
      + labs(title='Response Over Time - Multi-factor Faceting',
             x='Time (hours)',
             y='Response Score',
             color='Dose (mg)'))
print("Created multi-variable faceted plot")

# Advanced Example 8: Publication-ready plot
print("\n=== Advanced Example 8: Publication-Ready Plot ===")
publication_data = (experimental_data
                   .groupby(['treatment', 'dose'])
                   .agg({
                       'response': ['mean', 'sem'],  # Note: sem not available, using std
                       'subject_id': 'count'
                   })
                   .reset_index())
publication_data.columns = ['treatment', 'dose', 'mean_response', 'sem_response', 'n']
publication_data['sem_response'] = publication_data['sem_response'] / np.sqrt(publication_data['n'])

p8 = (ggplot(publication_data, aes(x='dose', y='mean_response', color='treatment'))
      + geom_line(size=2)
      + geom_point(size=4)
      # Note: Error bars not implemented yet, would use geom_errorbar
      + scale_color_manual(
          values=['#2C3E50', '#E74C3C', '#F39C12'],
          name='Treatment'
      )
      + scale_x_continuous(
          name='Dose (mg)',
          breaks=[0.1, 0.5, 1.0, 2.0]
      )
      + scale_y_continuous(name='Mean Response ± SEM')
      + theme_classic()
      + labs(
          title='Dose-Response Relationship by Treatment',
          subtitle='Mean ± SEM, n=20-25 per group',
          caption='Statistical analysis: Two-way ANOVA, p<0.05'
      ))
print("Created publication-ready plot")

print("\n=== All Advanced Examples Created Successfully! ===")
print("\nThese examples demonstrate:")
print("- Complex faceting with facet_grid and facet_wrap")
print("- Multiple data layers and aesthetic mappings")
print("- Continuous and discrete color scales")
print("- Statistical summary layers")
print("- Custom axis transformations and labels")
print("- Publication-ready formatting")
print("\nTo display any plot: plot.show() or just plot in Jupyter")