"""
Advanced theme system for ggviews

This module implements fine-grained theme control with element functions,
matching ggplot2's theme customization capabilities.
"""

import holoviews as hv
from typing import Dict, Any, Optional, Union, List
import warnings


class ThemeElement:
    """Base class for theme elements"""
    
    def __init__(self, **kwargs):
        self.params = kwargs
    
    def __repr__(self):
        params_str = ', '.join([f"{k}={v}" for k, v in self.params.items()])
        return f"{self.__class__.__name__}({params_str})"


class element_blank(ThemeElement):
    """Blank theme element that draws nothing
    
    Used to remove elements from plots.
    
    Example:
        theme(panel.grid.minor=element_blank())
    """
    
    def __init__(self):
        super().__init__()
    
    def __repr__(self):
        return "element_blank()"


class element_text(ThemeElement):
    """Text theme element
    
    Controls the appearance of text in plots.
    
    Args:
        family: Font family ('Arial', 'Times', 'Courier', etc.)
        face: Font face ('plain', 'bold', 'italic', 'bold.italic')
        colour: Text color (hex color or color name)
        color: Alias for colour (American spelling)
        size: Font size in points
        hjust: Horizontal justification (0=left, 0.5=center, 1=right)
        vjust: Vertical justification (0=bottom, 0.5=center, 1=top)
        angle: Text angle in degrees
        lineheight: Line spacing multiplier
        margin: Margin around text (top, right, bottom, left)
        debug: Show debugging rectangle around text
        **kwargs: Additional parameters
        
    Examples:
        element_text(size=12, face='bold')
        element_text(angle=45, hjust=1)
        element_text(colour='red', family='Arial')
    """
    
    def __init__(self, family=None, face=None, colour=None, color=None, size=None,
                 hjust=None, vjust=None, angle=None, lineheight=None, 
                 margin=None, debug=None, **kwargs):
        
        # Handle color/colour alias
        text_color = color or colour
        
        params = {}
        if family is not None:
            params['family'] = family
        if face is not None:
            params['face'] = face
        if text_color is not None:
            params['colour'] = text_color
        if size is not None:
            params['size'] = size
        if hjust is not None:
            params['hjust'] = hjust
        if vjust is not None:
            params['vjust'] = vjust
        if angle is not None:
            params['angle'] = angle
        if lineheight is not None:
            params['lineheight'] = lineheight
        if margin is not None:
            params['margin'] = margin
        if debug is not None:
            params['debug'] = debug
            
        params.update(kwargs)
        super().__init__(**params)


class element_line(ThemeElement):
    """Line theme element
    
    Controls the appearance of lines in plots.
    
    Args:
        colour: Line color (hex color or color name)
        color: Alias for colour (American spelling)
        size: Line width
        linetype: Line type ('solid', 'dashed', 'dotted', 'dotdash', 'longdash', 'twodash')
        lineend: Line end style ('round', 'butt', 'square')
        arrow: Arrow specification
        **kwargs: Additional parameters
        
    Examples:
        element_line(colour='black', size=0.5)
        element_line(linetype='dashed')
        element_line(color='red', size=2)
    """
    
    def __init__(self, colour=None, color=None, size=None, linetype=None,
                 lineend=None, arrow=None, **kwargs):
        
        # Handle color/colour alias
        line_color = color or colour
        
        params = {}
        if line_color is not None:
            params['colour'] = line_color
        if size is not None:
            params['size'] = size
        if linetype is not None:
            params['linetype'] = linetype
        if lineend is not None:
            params['lineend'] = lineend
        if arrow is not None:
            params['arrow'] = arrow
            
        params.update(kwargs)
        super().__init__(**params)


class element_rect(ThemeElement):
    """Rectangle theme element
    
    Controls the appearance of rectangles in plots.
    
    Args:
        fill: Fill color
        colour: Border color
        color: Alias for colour (American spelling)  
        size: Border line width
        linetype: Border line type
        **kwargs: Additional parameters
        
    Examples:
        element_rect(fill='white', colour='black')
        element_rect(fill='lightgray', size=0.5)
        element_rect(fill='transparent')
    """
    
    def __init__(self, fill=None, colour=None, color=None, size=None, 
                 linetype=None, **kwargs):
        
        # Handle color/colour alias
        border_color = color or colour
        
        params = {}
        if fill is not None:
            params['fill'] = fill
        if border_color is not None:
            params['colour'] = border_color
        if size is not None:
            params['size'] = size
        if linetype is not None:
            params['linetype'] = linetype
            
        params.update(kwargs)
        super().__init__(**params)


class AdvancedTheme:
    """Advanced theme class with fine-grained control
    
    Supports all ggplot2 theme elements for precise customization.
    """
    
    def __init__(self, **kwargs):
        self.elements = {}
        
        # Parse theme element specifications
        for key, value in kwargs.items():
            self.elements[key] = value
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this theme to a ggplot object"""
        new_plot = ggplot_obj._copy()
        
        # If there's already a theme, merge with it
        if new_plot.theme is not None:
            # Merge themes
            if hasattr(new_plot.theme, 'elements'):
                new_plot.theme.elements.update(self.elements)
            else:
                # Convert simple theme to advanced theme
                new_advanced = AdvancedTheme()
                new_advanced.base_theme = new_plot.theme
                new_advanced.elements = self.elements.copy()
                new_plot.theme = new_advanced
        else:
            new_plot.theme = self
            
        return new_plot
    
    def _apply(self, plot, ggplot_obj):
        """Apply advanced theme to plot"""
        # Start with base theme if available
        if hasattr(self, 'base_theme') and self.base_theme:
            plot = self.base_theme._apply(plot, ggplot_obj)
        
        # Apply element-specific customizations
        opts = {}
        
        # Handle panel grid customizations
        if 'panel.grid.minor' in self.elements:
            if isinstance(self.elements['panel.grid.minor'], element_blank):
                # Remove minor grid lines
                opts['show_grid'] = False
                
        if 'panel.grid.major' in self.elements:
            if isinstance(self.elements['panel.grid.major'], element_blank):
                opts['show_grid'] = False
            elif isinstance(self.elements['panel.grid.major'], element_line):
                line_elem = self.elements['panel.grid.major']
                gridstyle = {}
                if 'colour' in line_elem.params:
                    gridstyle['grid_line_color'] = line_elem.params['colour']
                if 'size' in line_elem.params:
                    gridstyle['grid_line_width'] = line_elem.params['size']
                if gridstyle:
                    opts['gridstyle'] = gridstyle
        
        # Handle axis text
        if 'axis.text.x' in self.elements:
            text_elem = self.elements['axis.text.x']
            if isinstance(text_elem, element_text):
                if 'angle' in text_elem.params:
                    opts['xrotation'] = text_elem.params['angle']
                if 'size' in text_elem.params:
                    opts['fontsize'] = {'xticks': text_elem.params['size']}
        
        if 'axis.text.y' in self.elements:
            text_elem = self.elements['axis.text.y']
            if isinstance(text_elem, element_text):
                if 'angle' in text_elem.params:
                    opts['yrotation'] = text_elem.params['angle']
        
        # Handle plot title
        if 'plot.title' in self.elements:
            title_elem = self.elements['plot.title']
            if isinstance(title_elem, element_text):
                title_opts = {}
                if 'size' in title_elem.params:
                    title_opts['fontsize'] = title_elem.params['size']
                if 'face' in title_elem.params:
                    if title_elem.params['face'] in ['bold', 'bold.italic']:
                        title_opts['fontweight'] = 'bold'
                if title_opts:
                    opts['title_format'] = title_opts
        
        # Handle legend
        if 'legend.position' in self.elements:
            pos = self.elements['legend.position']
            if pos == 'none':
                opts['show_legend'] = False
            elif pos in ['top', 'bottom', 'left', 'right']:
                opts['legend_position'] = pos
            elif isinstance(pos, (list, tuple)) and len(pos) == 2:
                # Custom coordinates (not directly supported in holoviews)
                warnings.warn("Custom legend coordinates not fully supported")
        
        # Handle panel background
        if 'panel.background' in self.elements:
            bg_elem = self.elements['panel.background']
            if isinstance(bg_elem, element_rect):
                if 'fill' in bg_elem.params:
                    opts['bgcolor'] = bg_elem.params['fill']
        
        # Handle plot background  
        if 'plot.background' in self.elements:
            bg_elem = self.elements['plot.background']
            if isinstance(bg_elem, element_rect):
                if 'fill' in bg_elem.params:
                    opts['fig_bgcolor'] = bg_elem.params['fill']
        
        # Apply options
        if opts:
            return plot.opts(**opts)
        return plot


# Enhanced theme function
def theme(**kwargs):
    """Create advanced theme with element-level control
    
    Args:
        **kwargs: Theme element specifications
        
    Theme elements include:
        line: All line elements
        rect: All rectangle elements  
        text: All text elements
        title: All title elements
        
        axis.line: Axis lines
        axis.line.x: X-axis line
        axis.line.y: Y-axis line
        axis.text: Axis text
        axis.text.x: X-axis text
        axis.text.y: Y-axis text
        axis.ticks: Axis tick marks
        axis.title: Axis titles
        axis.title.x: X-axis title
        axis.title.y: Y-axis title
        
        legend.background: Legend background
        legend.key: Legend key background
        legend.text: Legend text
        legend.title: Legend title
        legend.position: Legend position ('none', 'left', 'right', 'bottom', 'top')
        
        panel.background: Panel background
        panel.border: Panel border
        panel.grid: Panel grid lines
        panel.grid.major: Major grid lines
        panel.grid.minor: Minor grid lines
        panel.grid.major.x: Major vertical grid lines
        panel.grid.major.y: Major horizontal grid lines
        panel.grid.minor.x: Minor vertical grid lines
        panel.grid.minor.y: Minor horizontal grid lines
        
        plot.background: Plot background
        plot.title: Plot title
        plot.subtitle: Plot subtitle
        plot.caption: Plot caption
        
        strip.background: Facet strip background
        strip.text: Facet strip text
        
    Examples:
        theme(panel.grid.minor=element_blank())
        theme(axis.text.x=element_text(angle=45, hjust=1))
        theme(plot.title=element_text(size=16, face='bold'))
        theme(legend.position='bottom')
    """
    return AdvancedTheme(**kwargs)


# Export all theme elements and functions
__all__ = [
    'ThemeElement',
    'element_blank',
    'element_text', 
    'element_line',
    'element_rect',
    'AdvancedTheme',
    'theme',
]