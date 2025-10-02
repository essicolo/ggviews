"""
ColorBrewer color scales for ggviews

Implements the popular ColorBrewer palettes used in ggplot2.
"""

from .scales import Scale

# ColorBrewer palettes
BREWER_PALETTES = {
    # Sequential (single hue)
    'Blues': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'],
    'Greens': ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c', '#00441b'],
    'Greys': ['#ffffff', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525', '#000000'],
    'Oranges': ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704'],
    'Purples': ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#54278f', '#3f007d'],
    'Reds': ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d'],
    
    # Diverging
    'BrBG': ['#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#f5f5f5', '#c7eae5', '#80cdc1', '#35978f', '#01665e'],
    'PiYG': ['#c51b7d', '#de77ae', '#f1b6da', '#fde0ef', '#f7f7f7', '#e6f5d0', '#b8e186', '#7fbc41', '#4d9221'],
    'PRGn': ['#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#f7f7f7', '#d9f0d3', '#a6dba0', '#5aae61', '#1b7837'],
    'PuOr': ['#b35806', '#e08214', '#fdb863', '#fee0b6', '#f7f7f7', '#d8daeb', '#b2abd2', '#8073ac', '#542788'],
    'RdBu': ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7', '#d1e5f0', '#92c5de', '#4393c3', '#2166ac'],
    'RdGy': ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#ffffff', '#e0e0e0', '#bababa', '#878787', '#4d4d4d'],
    'RdYlBu': ['#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4'],
    'RdYlGn': ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'],
    'Spectral': ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#e6f598', '#abdda4', '#66c2a5', '#3288bd'],
    
    # Qualitative 
    'Set1': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999'],
    'Set2': ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3'],
    'Set3': ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f'],
    'Pastel1': ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec', '#f2f2f2'],
    'Pastel2': ['#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae', '#f1e2cc', '#cccccc'],
    'Dark2': ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666'],
    'Accent': ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666'],
    'Paired': ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']
}


class scale_colour_brewer(Scale):
    """ColorBrewer color scale for discrete data
    
    Args:
        type: Type of palette ('seq', 'div', 'qual')
        palette: Name of ColorBrewer palette
        direction: 1 for normal, -1 for reversed
        **kwargs: Additional scale parameters
        
    Examples:
        scale_colour_brewer(type='qual', palette='Set1')
        scale_colour_brewer(palette='Blues', direction=-1)
    """
    
    def __init__(self, type='seq', palette='Blues', direction=1, **kwargs):
        super().__init__('color', **kwargs)
        self.type = type
        self.palette = palette
        self.direction = direction
        
        # Validate palette
        if palette not in BREWER_PALETTES:
            available = list(BREWER_PALETTES.keys())
            raise ValueError(f"Palette '{palette}' not found. Available: {available}")
        
        self.colors = BREWER_PALETTES[palette]
        if direction == -1:
            self.colors = self.colors[::-1]
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply ColorBrewer colors to the ggplot object"""
        
        # Create color mapping for discrete data
        if hasattr(ggplot_obj, 'mapping') and 'color' in ggplot_obj.mapping.mappings:
            color_col = ggplot_obj.mapping.mappings['color']
            
            if data is not None and color_col in data.columns:
                unique_vals = data[color_col].unique()
                n_colors = len(unique_vals)
                
                # Select appropriate number of colors
                if n_colors <= len(self.colors):
                    selected_colors = self.colors[:n_colors]
                else:
                    # Repeat colors if we need more
                    selected_colors = (self.colors * ((n_colors // len(self.colors)) + 1))[:n_colors]
                
                # Create mapping
                brewer_map = dict(zip(unique_vals, selected_colors))
                ggplot_obj.brewer_discrete_map = brewer_map
        
        return plot


class scale_fill_brewer(Scale):
    """ColorBrewer fill scale for discrete data
    
    Args:
        type: Type of palette ('seq', 'div', 'qual')
        palette: Name of ColorBrewer palette  
        direction: 1 for normal, -1 for reversed
        **kwargs: Additional scale parameters
        
    Examples:
        scale_fill_brewer(type='div', palette='RdBu')
        scale_fill_brewer(palette='Set2', direction=-1)
    """
    
    def __init__(self, type='seq', palette='Blues', direction=1, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.palette = palette
        self.direction = direction
        
        # Validate palette
        if palette not in BREWER_PALETTES:
            available = list(BREWER_PALETTES.keys())
            raise ValueError(f"Palette '{palette}' not found. Available: {available}")
        
        self.colors = BREWER_PALETTES[palette]
        if direction == -1:
            self.colors = self.colors[::-1]
    
    def _apply(self, plot, ggplot_obj, data):
        """Apply ColorBrewer fill colors to the ggplot object"""
        
        # Create color mapping for discrete data
        if hasattr(ggplot_obj, 'mapping') and 'fill' in ggplot_obj.mapping.mappings:
            fill_col = ggplot_obj.mapping.mappings['fill']
            
            if data is not None and fill_col in data.columns:
                unique_vals = data[fill_col].unique()
                n_colors = len(unique_vals)
                
                # Select appropriate number of colors
                if n_colors <= len(self.colors):
                    selected_colors = self.colors[:n_colors]
                else:
                    # Repeat colors if we need more
                    selected_colors = (self.colors * ((n_colors // len(self.colors)) + 1))[:n_colors]
                
                # Create mapping
                brewer_map = dict(zip(unique_vals, selected_colors))
                ggplot_obj.brewer_fill_map = brewer_map
        
        return plot


class scale_color_brewer(scale_colour_brewer):
    """Alias for scale_colour_brewer (American spelling)"""
    pass


# List available palettes by type
def display_brewer_palettes():
    """Display available ColorBrewer palettes organized by type"""
    
    sequential = ['Blues', 'Greens', 'Greys', 'Oranges', 'Purples', 'Reds']
    diverging = ['BrBG', 'PiYG', 'PRGn', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral']
    qualitative = ['Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Dark2', 'Accent', 'Paired']
    
    print("📊 COLORBREWER PALETTES")
    print("="*50)
    print(f"🔵 Sequential ({len(sequential)}): {', '.join(sequential)}")
    print(f"🔄 Diverging ({len(diverging)}): {', '.join(diverging)}")
    print(f"🎨 Qualitative ({len(qualitative)}): {', '.join(qualitative)}")
    print(f"\n📝 Usage: scale_colour_brewer(palette='Set1')")
    print(f"📝 Usage: scale_fill_brewer(type='div', palette='RdBu')")


# Export
__all__ = ['scale_colour_brewer', 'scale_color_brewer', 'scale_fill_brewer', 'display_brewer_palettes', 'BREWER_PALETTES']