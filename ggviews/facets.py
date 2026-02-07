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


# ---------------------------------------------------------------------------
# Cross-backend hook helpers
# ---------------------------------------------------------------------------

def _fix_label_style(plot, element):
    """Hook: set axis labels to non-italic (ggplot2 default) in both backends."""
    # Matplotlib
    ax = getattr(plot, 'handles', {}).get('axis')
    if ax and hasattr(ax, 'transAxes'):
        ax.xaxis.label.set_fontstyle('normal')
        ax.yaxis.label.set_fontstyle('normal')
        for lbl in ax.get_xticklabels() + ax.get_yticklabels():
            lbl.set_fontstyle('normal')
        return
    # Bokeh: labels are normal style by default — nothing to do.


def _make_strip_top(label_text):
    """Return a hook that draws a ggplot2-style column strip at the top."""
    def hook(plot, element):
        # --- Matplotlib ---
        ax = getattr(plot, 'handles', {}).get('axis')
        if ax and hasattr(ax, 'transAxes'):
            import matplotlib.patches as mpatches
            rect = mpatches.FancyBboxPatch(
                (0, 1.0), 1.0, 0.08, transform=ax.transAxes,
                facecolor='#D9D9D9', edgecolor='#D9D9D9',
                clip_on=False, zorder=10, boxstyle='square,pad=0',
            )
            ax.add_patch(rect)
            ax.text(
                0.5, 1.04, str(label_text), transform=ax.transAxes,
                ha='center', va='center', fontsize=9,
                fontweight='normal', fontstyle='normal', zorder=11,
            )
            return
        # --- Bokeh ---
        fig = getattr(plot, 'state', None)
        if fig and hasattr(fig, 'title') and fig.title:
            fig.title.text = str(label_text)
            fig.title.background_fill_color = '#D9D9D9'
            fig.title.background_fill_alpha = 1.0
            fig.title.text_font_size = '10pt'
            fig.title.text_font_style = 'normal'
            fig.title.align = 'center'
    return hook


def _make_strip_right(label_text):
    """Return a hook that draws a ggplot2-style row strip on the right."""
    def hook(plot, element):
        # --- Matplotlib ---
        ax = getattr(plot, 'handles', {}).get('axis')
        if ax and hasattr(ax, 'transAxes'):
            import matplotlib.patches as mpatches
            rect = mpatches.FancyBboxPatch(
                (1.0, 0), 0.08, 1.0, transform=ax.transAxes,
                facecolor='#D9D9D9', edgecolor='#D9D9D9',
                clip_on=False, zorder=10, boxstyle='square,pad=0',
            )
            ax.add_patch(rect)
            ax.text(
                1.04, 0.5, str(label_text), transform=ax.transAxes,
                ha='center', va='center', fontsize=9,
                fontweight='normal', fontstyle='normal', rotation=270,
                zorder=11,
            )
            return
        # --- Bokeh ---  (append row label to existing title)
        fig = getattr(plot, 'state', None)
        if fig and hasattr(fig, 'title'):
            # For Bokeh there's no native right-strip; we could use an
            # annotation, but for now we skip (column strip already shown).
            pass
    return hook


# ---------------------------------------------------------------------------
# Facet base class
# ---------------------------------------------------------------------------

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

    def _render_facet_panel(self, facet_data, ggplot_obj, hooks=None):
        """Render a single facet panel.

        Parameters
        ----------
        facet_data : DataFrame
            Subset of data for this panel.
        ggplot_obj : ggplot
            Parent ggplot object (layers, aes, theme, etc.).
        hooks : list[callable] or None
            Hooks to apply to the rendered panel (strip labels, style fixes).
        """
        facet_ggplot = ggplot_obj._copy()
        facet_ggplot.data = facet_data
        facet_ggplot.facets = None  # prevent recursion
        facet_ggplot._hooks = []   # clear — we merge manually below

        panel = facet_ggplot._render()
        if panel is not None:
            # Merge theme hooks (e.g. essi grid) + facet hooks (strips, italic fix)
            # into one list so a single .opts(hooks=...) call doesn't clobber anything.
            all_hooks = list(getattr(ggplot_obj, '_hooks', [])) + (hooks or [])
            opts_kw = {'title': '', 'hooks': all_hooks}
            try:
                opts_kw['width'] = 350
                opts_kw['height'] = 280
            except Exception:
                pass
            try:
                panel = panel.opts(**opts_kw)
            except Exception:
                try:
                    panel = panel.opts(title='')
                except Exception:
                    pass
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

            # Render each panel with a top strip label
            panels = []
            for facet_val in unique_facets:
                facet_data = work_data[work_data[facet_col] == facet_val].copy()
                # Drop the synthetic key column so downstream geoms don't see it
                if facet_col == '_facet_key' and '_facet_key' in facet_data.columns:
                    facet_data = facet_data.drop(columns=['_facet_key'])

                if facet_data.empty:
                    continue

                hooks = [_fix_label_style, _make_strip_top(facet_val)]
                panel = self._render_facet_panel(facet_data, ggplot_obj, hooks=hooks)
                if panel is not None:
                    panels.append(panel)

            if not panels:
                return plot

            n_panels = len(panels)
            nrow_actual = int(np.ceil(n_panels / ncol))

            # Suppress redundant axis labels (ggplot2 style):
            # Only leftmost panels keep y-axis; only bottom panels keep x-axis.
            for idx, panel in enumerate(panels):
                row_idx = idx // ncol
                col_idx = idx % ncol
                is_left = (col_idx == 0)
                is_bottom = (row_idx == nrow_actual - 1) or (idx + ncol >= n_panels)
                strip_opts = {}
                if not is_left:
                    strip_opts['ylabel'] = ''
                    strip_opts['yaxis'] = None
                if not is_bottom:
                    strip_opts['xlabel'] = ''
                    strip_opts['xaxis'] = None
                if strip_opts:
                    try:
                        panels[idx] = panel.opts(**strip_opts)
                    except Exception:
                        pass

            layout = hv.Layout(panels).cols(ncol)
            try:
                layout = layout.opts(
                    sublabel_format='', hspace=0.1, vspace=0.1,
                )
            except Exception:
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
    and columns to another variable.  Strip labels follow ggplot2
    conventions: column labels at the top of each column, row labels
    on the right of each row.

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
            nrow = len(row_vals)

            # Render panels in row-major order.
            panels = []

            for row_i, row_val in enumerate(row_vals):
                for col_i, col_val in enumerate(col_vals):
                    cell_data = data.copy()

                    if has_row_var and row_val is not None:
                        cell_data = cell_data[cell_data[self.row_var] == row_val]
                    if has_col_var and col_val is not None:
                        cell_data = cell_data[cell_data[self.col_var] == col_val]

                    if cell_data.empty:
                        continue

                    # Build hooks for this cell position
                    hooks = [_fix_label_style]
                    # Column strip at top (first row only)
                    if row_i == 0 and has_col_var and col_val is not None:
                        hooks.append(_make_strip_top(col_val))
                    # Row strip on right (last column only)
                    if col_i == ncol - 1 and has_row_var and row_val is not None:
                        hooks.append(_make_strip_right(row_val))

                    panel = self._render_facet_panel(
                        cell_data, ggplot_obj, hooks=hooks,
                    )
                    if panel is not None:
                        panels.append(panel)

            if not panels:
                return plot

            # Suppress redundant axes
            for idx, panel in enumerate(panels):
                row_idx = idx // ncol
                col_idx = idx % ncol
                is_left = (col_idx == 0)
                is_bottom = (row_idx == nrow - 1)
                strip_opts = {}
                if not is_left:
                    strip_opts['ylabel'] = ''
                    strip_opts['yaxis'] = None
                if not is_bottom:
                    strip_opts['xlabel'] = ''
                    strip_opts['xaxis'] = None
                if strip_opts:
                    try:
                        panels[idx] = panel.opts(**strip_opts)
                    except Exception:
                        pass

            layout = hv.Layout(panels).cols(ncol)
            try:
                layout = layout.opts(
                    sublabel_format='', hspace=0.1, vspace=0.1,
                )
            except Exception:
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
