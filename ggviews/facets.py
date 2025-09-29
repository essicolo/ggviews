"""
Facets for ggviews

This module contains faceting functionality that allows creating
subplots based on categorical variables, similar to ggplot2's facet_wrap and facet_grid.
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List, Tuple
import warnings
import re


class Facet:
    """Base facet class"""
    
    def __init__(self, **kwargs):
        self.params = kwargs
    
    def _add_to_ggplot(self, ggplot_obj):
        """Add this facet to a ggplot object"""
        new_plot = ggplot_obj._copy()
        new_plot.facets = self
        return new_plot
    
    def _parse_formula(self, formula):
        """Parse faceting formula like '~var' or 'row_var ~ col_var'"""
        if isinstance(formula, str):
            # Handle formulas like '~var' or 'row ~ col'
            if '~' in formula:
                parts = [part.strip() for part in formula.split('~')]
                if len(parts) == 2:
                    row_var = parts[0] if parts[0] and parts[0] != '.' else None
                    col_var = parts[1] if parts[1] and parts[1] != '.' else None
                    return row_var, col_var
                else:
                    # Just '~var' format
                    return None, parts[-1].strip()
            else:
                # Just variable name
                return None, formula
        else:
            # Assume it's already a variable name
            return None, formula
    
    def _apply(self, plot, ggplot_obj):
        """Apply faceting - to be implemented by subclasses"""
        return plot


class facet_wrap(Facet):
    """Wrap facets into a rectangular layout
    
    Creates subplots for each level of a categorical variable,
    arranging them in a rectangular grid.
    
    Args:
        facets: Faceting variable(s). Can be:
            - String like '~variable' or 'variable'  
            - List of variable names for multiple faceting variables
        ncol: Number of columns in the layout
        nrow: Number of rows in the layout
        scales: Are scales shared across facets? ('fixed', 'free', 'free_x', 'free_y')
        **kwargs: Additional parameters
        
    Examples:
        facet_wrap('~species')
        facet_wrap('species', ncol=2)
        facet_wrap(['species', 'location'], ncol=3)
    """
    
    def __init__(self, facets, ncol=None, nrow=None, scales='fixed', **kwargs):
        super().__init__(**kwargs)
        self.facets = facets if isinstance(facets, list) else [facets]
        self.ncol = ncol
        self.nrow = nrow
        self.scales = scales  # 'fixed', 'free', 'free_x', 'free_y'
        
        # Parse formula format for each facet variable
        self.facet_vars = []
        for facet in self.facets:
            _, var = self._parse_formula(facet)
            if var:
                self.facet_vars.append(var)
    
    def _apply(self, plot, ggplot_obj):
        """Apply facet_wrap to create subplots"""
        if not self.facet_vars:
            return plot
        
        data = ggplot_obj.data
        if data is None:
            warnings.warn("No data available for faceting")
            return plot
        
        # Check if faceting variables exist
        missing_vars = [var for var in self.facet_vars if var not in data.columns]
        if missing_vars:
            warnings.warn(f"Faceting variables not found in data: {missing_vars}")
            return plot
        
        try:
            # For multiple facet variables, combine them
            if len(self.facet_vars) == 1:
                facet_col = self.facet_vars[0]
                facet_key = facet_col
            else:
                # Combine multiple facet variables
                facet_key = '_'.join(self.facet_vars)
                data[facet_key] = data[self.facet_vars].apply(
                    lambda x: ' | '.join([f"{var}: {val}" for var, val in zip(self.facet_vars, x)]), 
                    axis=1
                )
                facet_col = facet_key
            
            unique_facets = sorted(data[facet_col].unique())
            n_facets = len(unique_facets)
            
            if n_facets == 0:
                return plot
            
            # Calculate layout
            if self.ncol is not None and self.nrow is not None:
                ncol, nrow = self.ncol, self.nrow
            elif self.ncol is not None:
                ncol = self.ncol
                nrow = int(np.ceil(n_facets / ncol))
            elif self.nrow is not None:
                nrow = self.nrow
                ncol = int(np.ceil(n_facets / nrow))
            else:
                # Default: try to make roughly square
                ncol = int(np.ceil(np.sqrt(n_facets)))
                nrow = int(np.ceil(n_facets / ncol))
            
            # Create individual plots for each facet
            facet_plots = {}
            
            for facet_val in unique_facets:
                # Filter data for this facet
                facet_data = data[data[facet_col] == facet_val].copy()
                
                if len(facet_data) == 0:
                    continue
                
                # Create a copy of the ggplot object with filtered data
                facet_ggplot = ggplot_obj._copy()
                facet_ggplot.data = facet_data
                facet_ggplot.facets = None  # Remove faceting to avoid recursion
                
                # Render this facet
                facet_plot = facet_ggplot._render()
                
                if facet_plot is not None:
                    # Add facet title
                    facet_plot = facet_plot.opts(title=str(facet_val))
                    facet_plots[facet_val] = facet_plot
            
            if not facet_plots:
                return plot
            
            # Arrange plots in a grid layout
            plot_grid = []
            facet_list = list(facet_plots.values())
            
            for i in range(0, len(facet_list), ncol):
                row_plots = facet_list[i:i+ncol]
                if len(row_plots) == 1:
                    plot_grid.append(row_plots[0])
                else:
                    # Combine horizontally with +
                    row_plot = row_plots[0]
                    for p in row_plots[1:]:
                        row_plot = row_plot + p
                    plot_grid.append(row_plot)
            
            if len(plot_grid) == 1:
                return plot_grid[0]
            else:
                # Stack vertically
                final_plot = plot_grid[0]
                for p in plot_grid[1:]:
                    final_plot = (final_plot + p).cols(ncol)
                return final_plot
            
        except Exception as e:
            warnings.warn(f"Error in facet_wrap: {e}")
            return plot


class facet_grid(Facet):
    """Grid of facets based on row and column variables
    
    Creates a grid of subplots where rows correspond to one variable
    and columns to another variable.
    
    Args:
        facets: Faceting formula like 'row_var ~ col_var' or '. ~ col_var' or 'row_var ~ .'
        scales: Are scales shared across facets? ('fixed', 'free', 'free_x', 'free_y')
        margins: Show marginal plots
        **kwargs: Additional parameters
        
    Examples:
        facet_grid('species ~ location')
        facet_grid('. ~ species')  # Only columns
        facet_grid('location ~ .')  # Only rows
    """
    
    def __init__(self, facets, scales='fixed', margins=False, **kwargs):
        super().__init__(**kwargs)
        self.facets = facets
        self.scales = scales
        self.margins = margins
        
        # Parse the formula
        self.row_var, self.col_var = self._parse_formula(facets)
    
    def _apply(self, plot, ggplot_obj):
        """Apply facet_grid to create grid of subplots"""
        data = ggplot_obj.data
        if data is None:
            warnings.warn("No data available for faceting")
            return plot
        
        # Check which variables we have
        has_row_var = self.row_var is not None and self.row_var in data.columns
        has_col_var = self.col_var is not None and self.col_var in data.columns
        
        if not has_row_var and not has_col_var:
            warnings.warn("No valid faceting variables found")
            return plot
        
        try:
            # Get unique values for each dimension
            row_vals = sorted(data[self.row_var].unique()) if has_row_var else [None]
            col_vals = sorted(data[self.col_var].unique()) if has_col_var else [None]
            
            # Create grid of plots
            grid_plots = {}
            
            for row_val in row_vals:
                for col_val in col_vals:
                    # Filter data for this cell
                    cell_data = data.copy()
                    
                    if has_row_var and row_val is not None:
                        cell_data = cell_data[cell_data[self.row_var] == row_val]
                    
                    if has_col_var and col_val is not None:
                        cell_data = cell_data[cell_data[self.col_var] == col_val]
                    
                    if len(cell_data) == 0:
                        continue
                    
                    # Create plot for this cell
                    cell_ggplot = ggplot_obj._copy()
                    cell_ggplot.data = cell_data
                    cell_ggplot.facets = None  # Remove faceting to avoid recursion
                    
                    cell_plot = cell_ggplot._render()
                    
                    if cell_plot is not None:
                        # Create title
                        title_parts = []
                        if has_row_var and row_val is not None:
                            title_parts.append(f"{self.row_var}: {row_val}")
                        if has_col_var and col_val is not None:
                            title_parts.append(f"{self.col_var}: {col_val}")
                        
                        title = " | ".join(title_parts) if title_parts else "All"
                        cell_plot = cell_plot.opts(title=title)
                        
                        grid_plots[(row_val, col_val)] = cell_plot
            
            if not grid_plots:
                return plot
            
            # Arrange in grid
            if len(row_vals) == 1 and len(col_vals) == 1:
                # Single plot
                return list(grid_plots.values())[0]
            elif len(row_vals) == 1:
                # Single row, multiple columns
                plots = [grid_plots.get((row_vals[0], col_val)) for col_val in col_vals]
                plots = [p for p in plots if p is not None]
                if plots:
                    final_plot = plots[0]
                    for p in plots[1:]:
                        final_plot = final_plot + p
                    return final_plot
            elif len(col_vals) == 1:
                # Single column, multiple rows
                plots = [grid_plots.get((row_val, col_vals[0])) for row_val in row_vals]
                plots = [p for p in plots if p is not None]
                if plots:
                    final_plot = plots[0]
                    for p in plots[1:]:
                        final_plot = (final_plot + p).cols(1)
                    return final_plot
            else:
                # Full grid
                grid_rows = []
                for row_val in row_vals:
                    row_plots = [grid_plots.get((row_val, col_val)) for col_val in col_vals]
                    row_plots = [p for p in row_plots if p is not None]
                    
                    if row_plots:
                        if len(row_plots) == 1:
                            grid_rows.append(row_plots[0])
                        else:
                            row_plot = row_plots[0]
                            for p in row_plots[1:]:
                                row_plot = row_plot + p
                            grid_rows.append(row_plot)
                
                if grid_rows:
                    if len(grid_rows) == 1:
                        return grid_rows[0]
                    else:
                        final_plot = grid_rows[0]
                        for p in grid_rows[1:]:
                            final_plot = (final_plot + p).cols(len(col_vals))
                        return final_plot
            
            return plot
            
        except Exception as e:
            warnings.warn(f"Error in facet_grid: {e}")
            return plot


# Export all facet classes
__all__ = [
    'Facet',
    'facet_wrap',
    'facet_grid',
]