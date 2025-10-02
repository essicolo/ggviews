"""
Density plot implementation for ggviews
"""

import pandas as pd
import numpy as np
import holoviews as hv
from .geoms import GeomLayer
from scipy import stats
import warnings

class geom_density(GeomLayer):
    """Kernel density estimation plots
    
    Computes and displays kernel density estimates, which are smoothed versions
    of histograms.
    
    Args:
        mapping: Aesthetic mappings (aes object)
        data: Data for this layer
        bw: Bandwidth for kernel density estimation ('scott', 'silverman', or float)
        kernel: Kernel to use ('gaussian', 'tophat', 'epanechnikov', etc.)
        n: Number of points to evaluate density at (default: 512)
        adjust: Adjustment factor for bandwidth (default: 1.0)
        trim: Whether to trim the density curve to data range
        **kwargs: Additional parameters
        
    Examples:
        # Basic density plot
        geom_density(aes(x='value'))
        
        # Multiple densities by group
        geom_density(aes(x='value', fill='group'), alpha=0.5)
        
        # Customized bandwidth
        geom_density(aes(x='value'), bw=0.5, kernel='gaussian')
    """
    
    def __init__(self, mapping=None, data=None, bw='scott', kernel='gaussian',
                 n=512, adjust=1.0, trim=False, **kwargs):
        super().__init__(mapping, data, **kwargs)
        
        self.params.update({
            'bw': bw,
            'kernel': kernel,
            'n': n,
            'adjust': adjust,
            'trim': trim,
            'alpha': kwargs.get('alpha', 0.7),
            'color': kwargs.get('color', None),
            'fill': kwargs.get('fill', None)
        })
    
    def _compute_density(self, values, bw='scott', kernel='gaussian', n=512, adjust=1.0):
        """Compute kernel density estimation"""
        values = np.array(values).flatten()
        values = values[~np.isnan(values)]  # Remove NaN values
        
        if len(values) < 2:
            return np.array([]), np.array([])
        
        # Determine bandwidth
        if isinstance(bw, str):
            if bw == 'scott':
                bandwidth = len(values) ** (-1.0/5.0) * np.std(values)
            elif bw == 'silverman':
                bandwidth = (len(values) * 3.0 / 4.0) ** (-1.0/5.0) * np.std(values)
            else:
                bandwidth = np.std(values) * 0.1  # Default fallback
        else:
            bandwidth = float(bw)
        
        bandwidth *= adjust
        
        # Create evaluation points
        data_min, data_max = values.min(), values.max()
        data_range = data_max - data_min
        margin = data_range * 0.1  # 10% margin on each side
        
        x_eval = np.linspace(data_min - margin, data_max + margin, n)
        
        # Compute density using scipy
        try:
            kde = stats.gaussian_kde(values, bw_method=bandwidth)
            density = kde(x_eval)
        except:
            # Fallback to simple histogram-based density
            hist, bin_edges = np.histogram(values, bins=min(50, len(values)//2), density=True)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            # Interpolate to get more points
            density = np.interp(x_eval, bin_centers, hist)
        
        return x_eval, density
    
    def _render(self, data, combined_aes, ggplot_obj):
        """Render the density plot"""
        
        # Get aesthetic mappings
        x_col = combined_aes.mappings.get('x')
        
        if not x_col:
            raise ValueError("geom_density requires x aesthetic")
        
        if x_col not in data.columns:
            raise ValueError(f"Column '{x_col}' not found in data")
        
        # Check if we need to group by color/fill
        color_col = combined_aes.mappings.get('color') or combined_aes.mappings.get('fill')
        
        elements = []
        color_map = self._get_color_mapping(combined_aes, data, ggplot_obj)
        
        if color_col and color_col in data.columns:
            # Group by color/fill variable
            groups = data.groupby(color_col)
            
            for group_name, group_data in groups:
                x_vals = group_data[x_col].dropna()
                
                if len(x_vals) < 2:
                    continue
                
                x_density, y_density = self._compute_density(
                    x_vals, 
                    bw=self.params['bw'],
                    kernel=self.params['kernel'],
                    n=self.params['n'],
                    adjust=self.params['adjust']
                )
                
                if len(x_density) == 0:
                    continue
                
                # Create density curve
                curve_data = pd.DataFrame({
                    'x': x_density,
                    'y': y_density
                })
                
                # Determine color
                curve_color = color_map.get(group_name, '#1f77b4')
                
                # Create area plot for filled density
                if 'fill' in combined_aes.mappings or self.params.get('fill'):
                    density_area = hv.Area(curve_data).opts(
                        color=curve_color,
                        alpha=self.params['alpha'],
                        line_width=1
                    )
                    elements.append(density_area)
                else:
                    # Line plot for unfilled density
                    density_curve = hv.Curve(curve_data).opts(
                        color=curve_color,
                        alpha=self.params['alpha'],
                        line_width=2
                    )
                    elements.append(density_curve)
        
        else:
            # Single density plot
            x_vals = data[x_col].dropna()
            
            if len(x_vals) < 2:
                warnings.warn("Not enough data points for density estimation")
                return hv.Curve([]).opts(width=500, height=400)
            
            x_density, y_density = self._compute_density(
                x_vals,
                bw=self.params['bw'],
                kernel=self.params['kernel'], 
                n=self.params['n'],
                adjust=self.params['adjust']
            )
            
            curve_data = pd.DataFrame({
                'x': x_density,
                'y': y_density
            })
            
            # Determine color
            curve_color = self.params.get('color') or self.params.get('fill') or '#1f77b4'
            
            # Create area plot for filled density
            if self.params.get('fill') or 'fill' in combined_aes.mappings:
                density_plot = hv.Area(curve_data).opts(
                    color=curve_color,
                    alpha=self.params['alpha'],
                    line_width=1
                )
            else:
                # Line plot for unfilled density
                density_plot = hv.Curve(curve_data).opts(
                    color=curve_color,
                    alpha=self.params['alpha'],
                    line_width=2
                )
            
            elements.append(density_plot)
        
        # Combine all elements
        if elements:
            return hv.Overlay(elements) if len(elements) > 1 else elements[0]
        else:
            return hv.Curve([]).opts(width=500, height=400)


# Export
__all__ = ['geom_density']