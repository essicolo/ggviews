"""
Fine-grained theme elements for ggviews

Implements element functions and advanced theme() control similar to ggplot2.
"""

from .themes import Theme
import holoviews as hv

class ThemeElement:
    """Base class for theme elements"""
    pass

class element_blank(ThemeElement):
    """Remove element entirely
    
    Examples:
        theme(panel_grid_minor=element_blank())
        theme(axis_text_x=element_blank())
    """
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return "element_blank()"

class element_text(ThemeElement):
    """Text elements
    
    Args:
        family: Font family
        face: Font face ('plain', 'bold', 'italic', 'bold.italic')
        colour/color: Text color
        size: Font size in points
        hjust: Horizontal justification (0-1)
        vjust: Vertical justification (0-1)
        angle: Angle of text rotation
        lineheight: Line height multiplier
        margin: Margin around text
        
    Examples:
        element_text(size=12, color='blue')
        element_text(angle=45, hjust=1)
        element_text(face='bold', size=14)
    """
    
    def __init__(self, family=None, face='plain', colour=None, color=None,
                 size=None, hjust=None, vjust=None, angle=0, 
                 lineheight=None, margin=None):
        self.family = family
        self.face = face
        self.colour = colour or color or 'black'
        self.size = size or 11
        self.hjust = hjust or 0.5
        self.vjust = vjust or 0.5
        self.angle = angle
        self.lineheight = lineheight or 1.2
        self.margin = margin
    
    def __repr__(self):
        return f"element_text(size={self.size}, colour='{self.colour}', face='{self.face}')"

class element_line(ThemeElement):
    """Line elements
    
    Args:
        colour/color: Line color
        size: Line width
        linetype: Line type ('solid', 'dashed', 'dotted', etc.)
        lineend: Line end style
        arrow: Arrow specification
        
    Examples:
        element_line(color='gray', size=0.5)
        element_line(linetype='dashed', color='blue')
    """
    
    def __init__(self, colour=None, color=None, size=None, linetype='solid',
                 lineend=None, arrow=None):
        self.colour = colour or color or 'black'
        self.size = size or 0.5
        self.linetype = linetype
        self.lineend = lineend
        self.arrow = arrow
    
    def __repr__(self):
        return f"element_line(colour='{self.colour}', size={self.size}, linetype='{self.linetype}')"

class element_rect(ThemeElement):
    """Rectangle elements
    
    Args:
        fill: Fill color
        colour/color: Border color  
        size: Border width
        linetype: Border line type
        
    Examples:
        element_rect(fill='white', color='black')
        element_rect(fill='lightgray', size=0)
    """
    
    def __init__(self, fill=None, colour=None, color=None, size=None, linetype='solid'):
        self.fill = fill or 'white'
        self.colour = colour or color or 'black'
        self.size = size or 0.5
        self.linetype = linetype
    
    def __repr__(self):
        return f"element_rect(fill='{self.fill}', colour='{self.colour}')"


class AdvancedTheme(Theme):
    """Advanced theme with fine-grained element control
    
    Provides detailed control over plot appearance using theme elements.
    
    Args:
        **elements: Theme elements to customize
        
    Examples:
        theme(
            panel_grid_major=element_line(color='gray', size=0.5),
            panel_grid_minor=element_blank(),
            axis_text_x=element_text(angle=45, hjust=1),
            plot_title=element_text(size=16, face='bold'),
            legend_position='bottom'
        )
    """
    
    def __init__(self, **elements):
        super().__init__()
        self.elements = elements
        
        # Map common theme elements to holoviews options
        self.element_mapping = {
            # Panel elements
            'panel_background': 'bgcolor',
            'panel_border': 'show_frame',
            'panel_grid_major': 'show_grid',
            'panel_grid_minor': 'gridstyle',
            
            # Axis elements  
            'axis_line': 'show_frame',
            'axis_text': 'fontsize',
            'axis_text_x': 'xlabel_opts',
            'axis_text_y': 'ylabel_opts', 
            'axis_title': 'label_opts',
            'axis_title_x': 'xlabel',
            'axis_title_y': 'ylabel',
            'axis_ticks': 'show_ticks',
            
            # Plot elements
            'plot_background': 'bgcolor',
            'plot_title': 'title_opts',
            'plot_subtitle': 'title_opts',
            'plot_caption': 'title_opts',
            
            # Legend elements
            'legend_background': 'legend_opts',
            'legend_box': 'legend_opts',
            'legend_key': 'legend_opts', 
            'legend_text': 'legend_opts',
            'legend_title': 'legend_opts',
            'legend_position': 'legend_position',
            
            # Strip elements (for facets)
            'strip_background': 'bgcolor',
            'strip_text': 'title_opts'
        }
    
    def _apply(self, plot, ggplot_obj):
        """Apply advanced theme elements to the plot"""
        
        # Start with base options
        opts_dict = {
            'width': 500,
            'height': 400,
            'toolbar': 'above'
        }
        
        # Process each theme element
        for element_name, element_value in self.elements.items():
            self._apply_element(element_name, element_value, opts_dict)
        
        # Apply processed options
        try:
            styled_plot = plot.opts(**opts_dict)
            return styled_plot
        except Exception as e:
            # Fallback if some options aren't supported
            basic_opts = {
                'width': opts_dict.get('width', 500),
                'height': opts_dict.get('height', 400),
                'toolbar': opts_dict.get('toolbar', 'above')
            }
            return plot.opts(**basic_opts)
    
    def _apply_element(self, element_name, element_value, opts_dict):
        """Apply a single theme element"""
        
        if isinstance(element_value, element_blank):
            self._apply_blank_element(element_name, opts_dict)
        elif isinstance(element_value, element_text):
            self._apply_text_element(element_name, element_value, opts_dict)
        elif isinstance(element_value, element_line):
            self._apply_line_element(element_name, element_value, opts_dict)
        elif isinstance(element_value, element_rect):
            self._apply_rect_element(element_name, element_value, opts_dict)
        else:
            # Direct value (e.g., legend_position='bottom')
            self._apply_direct_value(element_name, element_value, opts_dict)
    
    def _apply_blank_element(self, element_name, opts_dict):
        """Apply element_blank() - remove elements"""
        
        if element_name == 'panel_grid_major':
            opts_dict['show_grid'] = False
        elif element_name == 'panel_grid_minor':
            opts_dict['gridstyle'] = {}
        elif element_name == 'axis_text_x':
            opts_dict['xaxis'] = None
        elif element_name == 'axis_text_y':
            opts_dict['yaxis'] = None
        elif element_name == 'legend_title':
            # Would need to modify legend title
            pass
        elif element_name == 'panel_border':
            opts_dict['show_frame'] = False
    
    def _apply_text_element(self, element_name, element, opts_dict):
        """Apply element_text() - text styling"""
        
        if element_name == 'plot_title':
            opts_dict['title_format'] = f'<b style="color:{element.colour}; font-size:{element.size}px">{{}}</b>'
        elif element_name == 'axis_title_x':
            opts_dict['xlabel'] = f'<span style="color:{element.colour}; font-size:{element.size}px">{{}}</span>'
        elif element_name == 'axis_title_y':
            opts_dict['ylabel'] = f'<span style="color:{element.colour}; font-size:{element.size}px">{{}}</span>'
        elif element_name == 'axis_text':
            opts_dict['fontsize'] = {'ticks': element.size, 'labels': element.size}
    
    def _apply_line_element(self, element_name, element, opts_dict):
        """Apply element_line() - line styling"""
        
        if element_name == 'panel_grid_major':
            opts_dict['show_grid'] = True
            opts_dict['gridstyle'] = {
                'grid_line_color': element.colour,
                'grid_line_width': element.size
            }
        elif element_name == 'axis_line':
            opts_dict['show_frame'] = True
    
    def _apply_rect_element(self, element_name, element, opts_dict):
        """Apply element_rect() - rectangle styling"""
        
        if element_name == 'panel_background':
            opts_dict['bgcolor'] = element.fill
        elif element_name == 'plot_background':
            opts_dict['bgcolor'] = element.fill
    
    def _apply_direct_value(self, element_name, value, opts_dict):
        """Apply direct values (strings, numbers, etc.)"""
        
        if element_name == 'legend_position':
            if value == 'none':
                opts_dict['show_legend'] = False
            elif value in ['top', 'bottom', 'left', 'right']:
                opts_dict['legend_position'] = value
        elif element_name == 'panel_background':
            opts_dict['bgcolor'] = value
        elif element_name == 'plot_background':
            opts_dict['bgcolor'] = value


def theme(**kwargs):
    """Create a theme with custom elements
    
    Args:
        **kwargs: Theme elements and their specifications
        
    Examples:
        theme(
            panel_grid_minor=element_blank(),
            axis_text_x=element_text(angle=45),
            plot_title=element_text(size=16, face='bold'),
            legend_position='bottom'
        )
    """
    return AdvancedTheme(**kwargs)


# Export
__all__ = ['theme', 'element_blank', 'element_text', 'element_line', 'element_rect']