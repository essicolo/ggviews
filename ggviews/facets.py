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
            if '~' in formula:
                parts = [part.strip() for part in formula.split('~')]
                if len(parts) == 2:
                    row_var = parts[0] if parts[0] and parts[0] != '.' else None
                    col_var = parts[1] if parts[1] and parts[1] != '.' else None
                    return row_var, col_var
                else:
                    return None, parts[-1].strip()
            else:
                return None, formula
        else:
            return None, formula

    @staticmethod
    def _strip_hook(plot, element):
        """Bokeh hook: style the panel title as a ggplot2-style strip label.

        Adds a gray background fill to the title text so it resembles
        the colored strip bars in ggplot2 facets.
        """
        fig = plot.state
        if hasattr(fig, 'title') and fig.title:
            fig.title.background_fill_color = '#E5E5E5'
            fig.title.background_fill_alpha = 1.0
            fig.title.text_font_size = '10pt'
            fig.title.text_font_style = 'normal'  # ggplot2 strips are not bold
            fig.title.align = 'center'
            # Add a little padding via border
            if hasattr(fig.title, 'border_line_color'):
                fig.title.border_line_color = '#CCCCCC'
                fig.title.border_line_alpha = 0.5

    def _render_facet_panel(self, facet_data, ggplot_obj, title):
        """Render a single facet panel with the given subset of data.

        Creates a copy of the ggplot object with filtered data and no faceting
        to avoid recursion, then renders it and applies the facet title
        styled as a ggplot2-style strip label.
        """
        facet_ggplot = ggplot_obj._copy()
        facet_ggplot.data = facet_data
        facet_ggplot.facets = None  # prevent recursion

        panel = facet_ggplot._render()
        if panel is not None:
            # Reduce panel size for multi-panel layouts and add strip hook
            try:
                panel = panel.opts(
                    title=str(title), width=350, height=280,
                    hooks=[self._strip_hook],
                )
            except Exception:
                try:
                    panel = panel.opts(title=str(title), hooks=[self._strip_hook])
                except Exception:
                    panel = panel.opts(title=str(title))
        return panel

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
        self.scales = scales

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
            # Build a facet key column (work on a copy to avoid mutating original)
            work_data = data.copy()

            if len(self.facet_vars) == 1:
                facet_col = self.facet_vars[0]
            else:
                facet_col = '_facet_key'
                work_data[facet_col] = work_data[self.facet_vars].apply(
                    lambda row: ' | '.join(
                        f"{var}: {val}" for var, val in zip(self.facet_vars, row)
                    ),
                    axis=1,
                )

            unique_facets = sorted(work_data[facet_col].unique())
            n_facets = len(unique_facets)

            if n_facets == 0:
                return plot

            # Determine layout dimensions
            if self.ncol is not None and self.nrow is not None:
                ncol = self.ncol
            elif self.ncol is not None:
                ncol = self.ncol
            elif self.nrow is not None:
                ncol = int(np.ceil(n_facets / self.nrow))
            else:
                ncol = int(np.ceil(np.sqrt(n_facets)))

            # Render each panel
            panels = []
            for facet_val in unique_facets:
                facet_data = work_data[work_data[facet_col] == facet_val].copy()
                # Drop the synthetic key column so downstream geoms don't see it
                if facet_col == '_facet_key' and '_facet_key' in facet_data.columns:
                    facet_data = facet_data.drop(columns=['_facet_key'])

                if facet_data.empty:
                    continue

                panel = self._render_facet_panel(facet_data, ggplot_obj, facet_val)
                if panel is not None:
                    panels.append(panel)

            if not panels:
                return plot

            n_panels = len(panels)
            nrow_actual = int(np.ceil(n_panels / ncol))

            # Suppress redundant axis labels (ggplot2 style):
            # - Only leftmost panels keep the y-axis label + ticks
            # - Only bottom-row panels keep the x-axis label + ticks
            for idx, panel in enumerate(panels):
                row_idx = idx // ncol
                col_idx = idx % ncol
                is_left = (col_idx == 0)
                is_bottom = (row_idx == nrow_actual - 1) or (idx + ncol >= n_panels)
                strip_opts = {}
                if not is_left:
                    strip_opts['ylabel'] = ''
                    strip_opts['yaxis'] = 'bare'
                if not is_bottom:
                    strip_opts['xlabel'] = ''
                    strip_opts['xaxis'] = 'bare'
                if strip_opts:
                    try:
                        panels[idx] = panel.opts(**strip_opts)
                    except Exception:
                        pass

            # Build a flat Layout and set the column count once
            layout = hv.Layout(panels).cols(ncol)
            # Suppress HoloViews "A","B","C" subplot labels (not ggplot2 style)
            try:
                layout = layout.opts(sublabel_format='')
            except Exception:
                pass
            return layout

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

        has_row_var = self.row_var is not None and self.row_var in data.columns
        has_col_var = self.col_var is not None and self.col_var in data.columns

        if not has_row_var and not has_col_var:
            warnings.warn("No valid faceting variables found")
            return plot

        try:
            row_vals = sorted(data[self.row_var].unique()) if has_row_var else [None]
            col_vals = sorted(data[self.col_var].unique()) if has_col_var else [None]
            ncol = len(col_vals)

            # Render panels in row-major order so that hv.Layout.cols(ncol)
            # produces the correct visual grid.
            panels = []

            for row_val in row_vals:
                for col_val in col_vals:
                    cell_data = data.copy()

                    if has_row_var and row_val is not None:
                        cell_data = cell_data[cell_data[self.row_var] == row_val]
                    if has_col_var and col_val is not None:
                        cell_data = cell_data[cell_data[self.col_var] == col_val]

                    if cell_data.empty:
                        continue

                    # Build title
                    title_parts = []
                    if has_row_var and row_val is not None:
                        title_parts.append(f"{self.row_var}: {row_val}")
                    if has_col_var and col_val is not None:
                        title_parts.append(f"{self.col_var}: {col_val}")
                    title = " | ".join(title_parts) if title_parts else "All"

                    panel = self._render_facet_panel(cell_data, ggplot_obj, title)
                    if panel is not None:
                        panels.append(panel)

            if not panels:
                return plot

            nrow_actual = len(row_vals)

            # Suppress redundant axis labels (ggplot2 style):
            # - Only leftmost panels keep y-axis label + ticks
            # - Only bottom-row panels keep x-axis label + ticks
            for idx, panel in enumerate(panels):
                row_idx = idx // ncol
                col_idx = idx % ncol
                is_left = (col_idx == 0)
                is_bottom = (row_idx == nrow_actual - 1)
                strip_opts = {}
                if not is_left:
                    strip_opts['ylabel'] = ''
                    strip_opts['yaxis'] = 'bare'
                if not is_bottom:
                    strip_opts['xlabel'] = ''
                    strip_opts['xaxis'] = 'bare'
                if strip_opts:
                    try:
                        panels[idx] = panel.opts(**strip_opts)
                    except Exception:
                        pass

            layout = hv.Layout(panels).cols(ncol)
            # Suppress HoloViews "A","B","C" subplot labels (not ggplot2 style)
            try:
                layout = layout.opts(sublabel_format='')
            except Exception:
                pass
            return layout

        except Exception as e:
            warnings.warn(f"Error in facet_grid: {e}")
            return plot


# Export all facet classes
__all__ = [
    'Facet',
    'facet_wrap',
    'facet_grid',
]
