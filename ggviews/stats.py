"""
Enhanced statistical transformations for ggviews

This module implements advanced statistical layers including confidence intervals,
enhanced smoothing methods, and statistical summaries.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Union, List, Tuple
import warnings
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from .geoms import GeomLayer
import holoviews as hv


class stat_smooth(GeomLayer):
    """Enhanced statistical smoothing with confidence intervals
    
    Provides advanced smoothing methods including linear regression,
    polynomial fitting, and loess-style local regression with 
    confidence intervals.
    
    Args:
        mapping: Aesthetic mappings
        data: Data for this layer
        method: Smoothing method ('lm', 'loess', 'gam', 'poly')
        formula: Formula specification (e.g., 'y ~ x', 'y ~ poly(x, 2)')
        se: Show confidence interval band
        level: Confidence level (default 0.95)
        span: Span for loess smoothing (0-1)
        degree: Polynomial degree for poly method
        n: Number of points to evaluate smooth at
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, method='auto', formula=None,
                 se=True, level=0.95, span=0.75, degree=1, n=80, 
                 color=None, fill=None, alpha=0.4, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.method = method
        self.formula = formula
        self.se = se
        self.level = level
        self.span = span
        self.degree = degree
        self.n = n
        self.params.update({
            'color': color,
            'fill': fill,
            'alpha': alpha
        })
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render enhanced statistical smooth"""
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("stat_smooth requires both x and y aesthetics")
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        if x_col not in data.columns or y_col not in data.columns:
            warnings.warn(f"Required columns not found: {x_col}, {y_col}")
            return None
        
        # Clean data
        clean_data = data[[x_col, y_col]].dropna()
        if len(clean_data) < 3:
            warnings.warn("Not enough data points for smoothing")
            return None
            
        x_data = clean_data[x_col].values
        y_data = clean_data[y_col].values
        
        # Sort by x
        sort_idx = np.argsort(x_data)
        x_data = x_data[sort_idx]
        y_data = y_data[sort_idx]
        
        # Generate smooth curve
        x_smooth = np.linspace(x_data.min(), x_data.max(), self.n)
        
        color = self.params.get('color', 'blue')
        fill_color = self.params.get('fill', color)
        
        try:
            if self.method == 'lm' or (self.method == 'auto' and len(clean_data) < 1000):
                # Linear regression
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
                y_smooth = slope * x_smooth + intercept
                
                if self.se:
                    # Calculate confidence interval
                    x_mean = np.mean(x_data)
                    sxx = np.sum((x_data - x_mean) ** 2)
                    se_y = std_err * np.sqrt(len(x_data)) * np.sqrt(1/len(x_data) + (x_smooth - x_mean)**2 / sxx)
                    
                    # t-distribution critical value
                    t_val = stats.t.ppf((1 + self.level) / 2, len(x_data) - 2)
                    ci_width = t_val * se_y
                    
                    y_upper = y_smooth + ci_width
                    y_lower = y_smooth - ci_width
                    
                    # Create confidence band
                    ci_data = pd.DataFrame({
                        'x': np.concatenate([x_smooth, x_smooth[::-1]]),
                        'y': np.concatenate([y_upper, y_lower[::-1]])
                    })
                    ci_area = hv.Area(ci_data).opts(
                        color=fill_color, alpha=self.params['alpha']
                    )
                    
                    # Create smooth line
                    smooth_data = pd.DataFrame({'x': x_smooth, 'y': y_smooth})
                    smooth_line = hv.Curve(smooth_data).opts(color=color, line_width=2)
                    
                    return ci_area * smooth_line
                else:
                    smooth_data = pd.DataFrame({'x': x_smooth, 'y': y_smooth})
                    return hv.Curve(smooth_data).opts(color=color, line_width=2)
                    
            elif self.method == 'poly':
                # Polynomial regression
                poly_features = PolynomialFeatures(degree=self.degree)
                x_poly = poly_features.fit_transform(x_data.reshape(-1, 1))
                x_smooth_poly = poly_features.transform(x_smooth.reshape(-1, 1))
                
                model = LinearRegression()
                model.fit(x_poly, y_data)
                y_smooth = model.predict(x_smooth_poly)
                
                smooth_data = pd.DataFrame({'x': x_smooth, 'y': y_smooth})
                return hv.Curve(smooth_data).opts(color=color, line_width=2)
                
            else:  # loess or auto with large data
                # Simple local regression approximation
                y_smooth = np.zeros_like(x_smooth)
                window_size = max(int(len(x_data) * self.span), 3)
                
                for i, x_val in enumerate(x_smooth):
                    # Find nearest neighbors
                    distances = np.abs(x_data - x_val)
                    nearest_idx = np.argsort(distances)[:window_size]
                    
                    # Weighted local regression
                    local_x = x_data[nearest_idx]
                    local_y = y_data[nearest_idx]
                    weights = np.exp(-distances[nearest_idx] / (distances[nearest_idx].max() + 1e-10))
                    
                    # Weighted mean
                    y_smooth[i] = np.average(local_y, weights=weights)
                
                smooth_data = pd.DataFrame({'x': x_smooth, 'y': y_smooth})
                return hv.Curve(smooth_data).opts(color=color, line_width=2)
                
        except Exception as e:
            warnings.warn(f"Smoothing failed: {e}")
            # Fallback to simple linear regression
            coeffs = np.polyfit(x_data, y_data, 1)
            y_smooth = np.polyval(coeffs, x_smooth)
            smooth_data = pd.DataFrame({'x': x_smooth, 'y': y_smooth})
            return hv.Curve(smooth_data).opts(color=color, line_width=2)


class stat_summary(GeomLayer):
    """Statistical summaries
    
    Computes and displays statistical summaries of data.
    
    Args:
        mapping: Aesthetic mappings
        data: Data for this layer
        fun: Summary function ('mean', 'median', 'sum', etc.)
        fun_min: Function for lower bound
        fun_max: Function for upper bound
        geom: Geometry to use ('point', 'bar', 'line')
        **kwargs: Additional parameters
    """
    
    def __init__(self, mapping=None, data=None, fun='mean', fun_min=None, fun_max=None,
                 geom='point', **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.fun = fun
        self.fun_min = fun_min
        self.fun_max = fun_max
        self.summary_geom = geom
        
        # Map function names to actual functions
        self.func_map = {
            'mean': np.mean,
            'median': np.median,
            'sum': np.sum,
            'min': np.min,
            'max': np.max,
            'std': np.std,
            'var': np.var,
            'count': len
        }
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render statistical summary"""
        if 'x' not in combined_aes.mappings or 'y' not in combined_aes.mappings:
            raise ValueError("stat_summary requires both x and y aesthetics")
        
        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        
        if x_col not in data.columns or y_col not in data.columns:
            return None
        
        # Group by x and compute summaries
        grouped = data.groupby(x_col)[y_col]
        
        if isinstance(self.fun, str):
            if self.fun in self.func_map:
                summary_func = self.func_map[self.fun]
            else:
                summary_func = np.mean
        else:
            summary_func = self.fun
        
        summaries = grouped.apply(summary_func)
        summary_data = pd.DataFrame({
            'x': summaries.index,
            'y': summaries.values
        })
        
        color = self.params.get('color', 'red')
        
        if self.summary_geom == 'point':
            return hv.Scatter(summary_data).opts(color=color, size=6, alpha=0.8)
        elif self.summary_geom == 'line':
            return hv.Curve(summary_data).opts(color=color, line_width=2)
        else:
            return hv.Bars(summary_data).opts(color=color, alpha=0.7)


# Enhanced geom_smooth that uses stat_smooth
def geom_smooth_enhanced(mapping=None, data=None, method='auto', se=True, 
                        level=0.95, **kwargs):
    """Enhanced geom_smooth with confidence intervals
    
    This replaces the basic geom_smooth with advanced statistical capabilities.
    """
    return stat_smooth(mapping=mapping, data=data, method=method, se=se, 
                      level=level, **kwargs)


# Export statistical functions
__all__ = [
    'stat_smooth',
    'stat_summary', 
    'geom_smooth_enhanced',
]