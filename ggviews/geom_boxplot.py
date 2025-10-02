"""
Box plot implementation for ggviews
"""

import pandas as pd
import numpy as np
import holoviews as hv
from .geoms import GeomLayer
import warnings

class geom_boxplot(GeomLayer):
    """Box and whisker plots
    
    Creates box-and-whisker plots showing the distribution of a continuous variable,
    optionally grouped by a categorical variable.
    
    Args:
        mapping: Aesthetic mappings (aes object)
        data: Data for this layer
        width: Box width (default: 0.9)
        outlier_alpha: Transparency for outliers (default: 1.0)
        outlier_color: Color for outliers (default: None)
        outlier_size: Size for outliers (default: 1.5)
        coef: Whisker length coefficient (default: 1.5)
        **kwargs: Additional parameters
        
    Examples:
        # Basic boxplot
        geom_boxplot(aes(y='value'))
        
        # Grouped boxplot
        geom_boxplot(aes(x='group', y='value'))
        
        # Customized
        geom_boxplot(aes(x='group', y='value', fill='group'), width=0.5)
    """
    
    def __init__(self, mapping=None, data=None, width=0.9, 
                 outlier_alpha=1.0, outlier_color=None, outlier_size=1.5,
                 coef=1.5, **kwargs):
        super().__init__(mapping, data, **kwargs)
        
        self.params.update({
            'width': width,
            'outlier_alpha': outlier_alpha,
            'outlier_color': outlier_color,
            'outlier_size': outlier_size,
            'coef': coef,
            'alpha': kwargs.get('alpha', 0.7),
            'color': kwargs.get('color', None),
            'fill': kwargs.get('fill', None)
        })
    
    def _calculate_boxplot_stats(self, data, y_col, group_col=None):
        """Calculate boxplot statistics"""
        if group_col and group_col in data.columns:
            groups = data.groupby(group_col)
            results = []
            
            for name, group in groups:
                stats = self._compute_single_boxplot(group[y_col].dropna())
                stats['group'] = name
                results.append(stats)
            
            return pd.DataFrame(results)
        else:
            stats = self._compute_single_boxplot(data[y_col].dropna())
            stats['group'] = 'all'
            return pd.DataFrame([stats])
    
    def _compute_single_boxplot(self, values):
        """Compute boxplot statistics for a single group"""
        values = np.array(values)
        
        q1 = np.percentile(values, 25)
        q2 = np.percentile(values, 50)  # median
        q3 = np.percentile(values, 75)
        
        iqr = q3 - q1
        lower_whisker = q1 - self.params['coef'] * iqr
        upper_whisker = q3 + self.params['coef'] * iqr
        
        # Find actual whisker positions (closest data points within limits)
        lower_whisker = max(lower_whisker, values.min())
        upper_whisker = min(upper_whisker, values.max())
        
        # Find outliers
        outliers = values[(values < lower_whisker) | (values > upper_whisker)]
        
        return {
            'q1': q1,
            'median': q2,
            'q3': q3,
            'lower_whisker': lower_whisker,
            'upper_whisker': upper_whisker,
            'outliers': outliers.tolist(),
            'n': len(values)
        }
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render the boxplot"""
        
        # Get aesthetic mappings
        y_col = combined_aes.mappings.get('y')
        x_col = combined_aes.mappings.get('x')
        
        if not y_col:
            raise ValueError("geom_boxplot requires y aesthetic")
        
        if y_col not in data.columns:
            raise ValueError(f"Column '{y_col}' not found in data")
        
        # Calculate boxplot statistics
        stats_df = self._calculate_boxplot_stats(data, y_col, x_col)
        
        # Create plot elements
        elements = []
        
        # Handle colors
        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        
        for i, row in stats_df.iterrows():
            x_pos = i if not x_col else i  # Position along x-axis
            width = self.params['width']
            
            # Determine colors
            if color_map and x_col and x_col in combined_aes.mappings:
                box_color = color_map.get(row['group'], '#1f77b4')
            else:
                box_color = self.params.get('color') or self.params.get('fill') or '#1f77b4'
            
            # Create box (using Rectangles for better control)
            box_data = pd.DataFrame({
                'x': [x_pos - width/2, x_pos + width/2],
                'y': [row['q1'], row['q3']]
            })
            
            # Box rectangle
            box_rect = hv.Rectangles([(x_pos - width/2, row['q1'], x_pos + width/2, row['q3'])]).opts(
                color=box_color,
                alpha=self.params['alpha'],
                line_color='black',
                line_width=1
            )
            elements.append(box_rect)
            
            # Median line
            median_line = hv.Curve([(x_pos - width/2, row['median']), (x_pos + width/2, row['median'])]).opts(
                color='black',
                line_width=2
            )
            elements.append(median_line)
            
            # Whiskers (vertical lines)
            lower_whisker = hv.Curve([(x_pos, row['q1']), (x_pos, row['lower_whisker'])]).opts(
                color='black',
                line_width=1
            )
            upper_whisker = hv.Curve([(x_pos, row['q3']), (x_pos, row['upper_whisker'])]).opts(
                color='black',
                line_width=1
            )
            elements.extend([lower_whisker, upper_whisker])
            
            # Whisker caps
            cap_width = width * 0.3
            lower_cap = hv.Curve([(x_pos - cap_width/2, row['lower_whisker']), 
                                 (x_pos + cap_width/2, row['lower_whisker'])]).opts(
                color='black',
                line_width=1
            )
            upper_cap = hv.Curve([(x_pos - cap_width/2, row['upper_whisker']), 
                                 (x_pos + cap_width/2, row['upper_whisker'])]).opts(
                color='black',
                line_width=1
            )
            elements.extend([lower_cap, upper_cap])
            
            # Outliers
            if row['outliers']:
                outlier_data = pd.DataFrame({
                    'x': [x_pos] * len(row['outliers']),
                    'y': row['outliers']
                })
                
                outlier_color = self.params.get('outlier_color', 'black')
                outliers = hv.Scatter(outlier_data).opts(
                    color=outlier_color,
                    size=self.params['outlier_size'],
                    alpha=self.params['outlier_alpha']
                )
                elements.append(outliers)
        
        # Combine all elements
        if elements:
            return hv.Overlay(elements)
        else:
            # Fallback empty plot
            return hv.Curve([]).opts(width=500, height=400)


# Export
__all__ = ['geom_boxplot']