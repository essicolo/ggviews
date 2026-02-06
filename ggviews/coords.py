"""
Coordinate systems for ggviews

This module implements coordinate system transformations that control
how data is mapped to the plot area, including aspect ratios and transformations.
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List, Tuple
import warnings


class CoordSystem:
    """Base coordinate system class"""
    
    def __init__(self, **kwargs):
        self.params = kwargs
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this coordinate system to a ggplot object"""
        new_plot = ggplot_obj._copy()
        new_plot.coord_system = self
        return new_plot
    
    def _apply(self, plot, ggplot_obj):
        """Apply coordinate transformation - to be implemented by subclasses"""
        return plot


class coord_cartesian(CoordSystem):
    """Cartesian coordinate system (default)
    
    The standard coordinate system where x and y map directly to horizontal
    and vertical positions.
    
    Args:
        xlim: X-axis limits (min, max)
        ylim: Y-axis limits (min, max)
        expand: Whether to expand limits slightly beyond data range
        **kwargs: Additional parameters
    """
    
    def __init__(self, xlim=None, ylim=None, expand=True, **kwargs):
        super().__init__(**kwargs)
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
    
    def _apply(self, plot, ggplot_obj):
        """Apply cartesian coordinate system"""
        opts = {}
        
        if self.xlim is not None:
            opts['xlim'] = self.xlim
        if self.ylim is not None:
            opts['ylim'] = self.ylim
            
        if opts:
            return plot.opts(**opts)
        return plot


class coord_fixed(CoordSystem):
    """Fixed aspect ratio coordinate system
    
    Forces a fixed ratio between the physical representation of data units
    on the axes. This is useful for ensuring that one unit on the x-axis
    is the same length as one unit on the y-axis.
    
    Args:
        ratio: Aspect ratio (y/x). If 1, one unit on x-axis = one unit on y-axis
        xlim: X-axis limits (min, max) 
        ylim: Y-axis limits (min, max)
        expand: Whether to expand limits slightly beyond data range
        **kwargs: Additional parameters
        
    Examples:
        coord_fixed()  # ratio = 1 (equal scaling)
        coord_fixed(ratio=2)  # y-axis units are twice as long as x-axis units
    """
    
    def __init__(self, ratio=1, xlim=None, ylim=None, expand=True, **kwargs):
        super().__init__(**kwargs)
        self.ratio = ratio
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
    
    def _apply(self, plot, ggplot_obj):
        """Apply fixed aspect ratio coordinate system"""
        opts = {}
        
        # Set axis limits if provided
        if self.xlim is not None:
            opts['xlim'] = self.xlim
        if self.ylim is not None:
            opts['ylim'] = self.ylim
        
        # Apply aspect ratio
        # In holoviews, we can control aspect ratio through plot dimensions
        if hasattr(plot, 'opts'):
            # Calculate appropriate dimensions based on aspect ratio
            base_width = 500
            base_height = int(base_width * self.ratio)
            
            opts.update({
                'width': base_width,
                'height': base_height,
                'aspect': self.ratio,
                'data_aspect': self.ratio  # This forces equal scaling of data units
            })
        
        if opts:
            return plot.opts(**opts)
        return plot


class coord_equal(coord_fixed):
    """Equal aspect ratio coordinate system
    
    Convenience function for coord_fixed(ratio=1). Forces equal scaling
    so that one unit on the x-axis is the same length as one unit on the y-axis.
    This is particularly useful for maps, scatter plots where distances matter,
    or any plot where the relationship between x and y units is meaningful.
    
    Args:
        xlim: X-axis limits (min, max)
        ylim: Y-axis limits (min, max)
        expand: Whether to expand limits slightly beyond data range
        **kwargs: Additional parameters
        
    Example:
        coord_equal()  # Same as coord_fixed(ratio=1)
    """
    
    def __init__(self, xlim=None, ylim=None, expand=True, **kwargs):
        super().__init__(ratio=1, xlim=xlim, ylim=ylim, expand=expand, **kwargs)


# coord_flip is defined in coord_flip.py to avoid duplication


class coord_trans(CoordSystem):
    """Transformed coordinate system
    
    Applies transformations to the coordinate system, such as log scales.
    
    Args:
        x: Transformation for x-axis ('identity', 'log', 'log10', 'sqrt', etc.)
        y: Transformation for y-axis ('identity', 'log', 'log10', 'sqrt', etc.)
        xlim: X-axis limits (in transformed space)
        ylim: Y-axis limits (in transformed space)
        **kwargs: Additional parameters
    """
    
    def __init__(self, x='identity', y='identity', xlim=None, ylim=None, **kwargs):
        super().__init__(**kwargs)
        self.x_trans = x
        self.y_trans = y
        self.xlim = xlim
        self.ylim = ylim
    
    def _apply(self, plot, ggplot_obj):
        """Apply coordinate transformations"""
        opts = {}
        
        # Apply transformations
        if self.x_trans == 'log' or self.x_trans == 'log10':
            opts['logx'] = True
        if self.y_trans == 'log' or self.y_trans == 'log10':
            opts['logy'] = True
            
        # Set limits
        if self.xlim is not None:
            opts['xlim'] = self.xlim
        if self.ylim is not None:
            opts['ylim'] = self.ylim
            
        if opts:
            return plot.opts(**opts)
        return plot


class coord_polar(CoordSystem):
    """Polar coordinate system

    Maps data to polar coordinates. When applied to bar charts, this produces
    pie/donut charts. For scatter and line data, it transforms (theta, r) pairs
    into Cartesian coordinates for display.

    Args:
        theta: Which aesthetic to map to angle ('x' or 'y')
        start: Starting angle (in radians, 0 = 12 o'clock)
        direction: Direction of angles (1 for clockwise, -1 for counter-clockwise)
        **kwargs: Additional parameters

    Examples:
        coord_polar()                    # theta='x', default
        coord_polar(theta='y')           # y maps to angle
        coord_polar(start=np.pi/2)       # start at 3 o'clock
    """

    def __init__(self, theta='x', start=0, direction=1, **kwargs):
        super().__init__(**kwargs)
        self.theta = theta
        self.start = start
        self.direction = direction

    def _apply(self, plot, ggplot_obj):
        """Apply polar coordinate transformation.

        For Bars elements this creates a pie chart using Path/Polygons.
        For Scatter/Curve this converts (angle, radius) -> (x, y).
        """
        if plot is None:
            return plot

        # Try to detect the element type inside overlays
        elements = self._collect_elements(plot)
        if not elements:
            return plot

        # Check if we have Bars -> pie chart
        has_bars = any(isinstance(el, hv.Bars) for el in elements)

        if has_bars:
            return self._bars_to_pie(elements, ggplot_obj)

        # For other element types, apply angular transformation
        return self._transform_polar(elements, ggplot_obj)

    # ------------------------------------------------------------------
    def _collect_elements(self, plot):
        """Recursively collect leaf HoloViews elements from a plot."""
        elements = []
        if isinstance(plot, hv.Overlay):
            for item in plot:
                elements.extend(self._collect_elements(item))
        elif isinstance(plot, hv.Element):
            elements.append(plot)
        return elements

    # ------------------------------------------------------------------
    def _bars_to_pie(self, elements, ggplot_obj):
        """Convert bar data into a pie/donut chart rendered as filled wedges."""
        # Gather all bar data
        labels = []
        values = []
        colors = []

        for el in elements:
            if isinstance(el, hv.Bars):
                df = el.dframe()
                if df.empty:
                    continue
                xcol = df.columns[0]
                ycol = df.columns[1] if len(df.columns) > 1 else None
                if ycol is None:
                    continue
                for _, row in df.iterrows():
                    labels.append(str(row[xcol]))
                    values.append(float(row[ycol]))
                    # Try to pick up the bar color
                    try:
                        colors.append(el.opts.get('plot').kwargs.get('color', None))
                    except Exception:
                        colors.append(None)

        if not values or sum(values) == 0:
            warnings.warn("coord_polar: no positive bar values to create pie chart")
            return hv.Overlay([])

        total = sum(values)
        fractions = [v / total for v in values]

        # Build wedge polygons
        n_points = 60  # points per wedge arc
        wedges = []
        current_angle = self.start

        default_colors = ggplot_obj.default_colors
        for i, (label, frac) in enumerate(zip(labels, fractions)):
            sweep = 2 * np.pi * frac * self.direction
            angles = np.linspace(current_angle, current_angle + sweep, n_points)
            # Wedge: centre -> arc -> centre
            xs = np.concatenate([[0], np.cos(angles), [0]])
            ys = np.concatenate([[0], np.sin(angles), [0]])

            color = colors[i] if colors[i] else default_colors[i % len(default_colors)]
            wedge = hv.Polygons([{'x': xs, 'y': ys}]).opts(
                color=color,
                line_color='white',
                line_width=1,
            )
            wedges.append(wedge)

            # Label at midpoint of arc
            mid_angle = current_angle + sweep / 2
            lx = 0.6 * np.cos(mid_angle)
            ly = 0.6 * np.sin(mid_angle)
            lbl = hv.Labels(
                pd.DataFrame({'x': [lx], 'y': [ly], 'text': [label]}),
                kdims=['x', 'y'], vdims=['text'],
            ).opts(text_font_size='9pt', text_color='white')
            wedges.append(lbl)

            current_angle += sweep

        pie = hv.Overlay(wedges).opts(
            width=450, height=450,
            xaxis=None, yaxis=None,
            show_frame=False,
        )
        return pie

    # ------------------------------------------------------------------
    def _transform_polar(self, elements, ggplot_obj):
        """Transform scatter/curve data from (theta, r) to Cartesian."""
        transformed = []
        for el in elements:
            df = el.dframe()
            if df.empty:
                transformed.append(el)
                continue
            cols = list(df.columns)
            if len(cols) < 2:
                transformed.append(el)
                continue

            if self.theta == 'x':
                theta_col, r_col = cols[0], cols[1]
            else:
                theta_col, r_col = cols[1], cols[0]

            theta_vals = df[theta_col].astype(float)
            r_vals = df[r_col].astype(float)

            # Normalise theta to [0, 2*pi]
            t_min, t_max = theta_vals.min(), theta_vals.max()
            if t_max > t_min:
                angles = self.start + self.direction * 2 * np.pi * (theta_vals - t_min) / (t_max - t_min)
            else:
                angles = np.full_like(theta_vals, self.start)

            cart_x = r_vals * np.cos(angles)
            cart_y = r_vals * np.sin(angles)
            cart_df = pd.DataFrame({'x': cart_x, 'y': cart_y})

            if isinstance(el, hv.Scatter):
                transformed.append(hv.Scatter(cart_df).opts(tools=['hover']))
            elif isinstance(el, (hv.Curve, hv.Area)):
                transformed.append(hv.Curve(cart_df))
            else:
                transformed.append(el)

        result = hv.Overlay(transformed) if len(transformed) > 1 else transformed[0]
        return result.opts(
            xaxis=None, yaxis=None, show_frame=False,
            width=450, height=450,
        )


# Convenience functions that mirror ggplot2 API
def coord_quickmap():
    """Quick map projection (approximates coord_map for small areas)
    
    Provides a quick approximation of a map projection that works well
    for small areas where the earth's curvature is not a major factor.
    
    Returns:
        coord_fixed: Fixed coordinate system with appropriate aspect ratio
    """
    return coord_fixed(ratio=1)


# Export all coordinate system classes
__all__ = [
    'CoordSystem',
    'coord_cartesian',
    'coord_fixed', 
    'coord_equal',
    'coord_trans',
    'coord_polar',
    'coord_quickmap',
]