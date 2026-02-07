"""
gghighlight - Highlight subsets of data while graying out the rest.

Implements the core behaviour of R's gghighlight package:
  * Row-level predicates  (string for df.query() or callable)
  * Group-level predicates (when use_group_by=True, predicate is
    evaluated per group and whole groups are kept / discarded)
  * Configurable unhighlighted styling (colour, alpha)
  * Optional direct labels on highlighted groups
"""

import copy
import warnings
import numpy as np
import pandas as pd
import holoviews as hv


class gghighlight:
    """Highlight data that matches a predicate.

    Parameters
    ----------
    predicate : str or callable
        * **str** – passed to ``DataFrame.query()`` (e.g. ``"species == 'setosa'"``).
        * **callable** – receives a DataFrame (or group DataFrame when
          *use_group_by* is True) and must return a boolean Series / scalar.
    use_group_by : bool, default False
        When True the predicate is applied once per group (defined by the
        ``color``/``colour``/``group`` aesthetic) and entire groups are
        kept or discarded.  The callable should return a single bool.
    unhighlighted_colour : str, default '#CCCCCC'
        Colour for the de-emphasised (non-matching) data.
    unhighlighted_alpha : float, default 0.3
        Alpha for the de-emphasised data.
    label_key : str or None
        If given, automatically add ``geom_label_repel`` for highlighted
        data using this column as the label aesthetic.
    n : int or None
        When set together with *use_group_by*, keep only the top *n*
        groups (sorted by the predicate value descending).
    keep_scales : bool, default False
        If True the axes limits are computed from the full data, not just
        the highlighted subset.  (Currently a no-op placeholder.)
    """

    def __init__(self, predicate, *, use_group_by=False,
                 unhighlighted_colour='#CCCCCC', unhighlighted_alpha=0.3,
                 label_key=None, n=None, keep_scales=False):
        self.predicate = predicate
        self.use_group_by = use_group_by
        self.unhighlighted_colour = unhighlighted_colour
        self.unhighlighted_alpha = unhighlighted_alpha
        self.label_key = label_key
        self.n = n
        self.keep_scales = keep_scales

    # ── ggplot integration ────────────────────────────────────────────

    def _add_to_ggplot(self, ggplot_obj):
        new_plot = ggplot_obj._copy()
        new_plot.highlight = self
        return new_plot

    # ── data splitting ────────────────────────────────────────────────

    def _split(self, data, combined_aes):
        """Return (highlight_mask,) a boolean Series aligned to *data*."""
        if self.use_group_by:
            return self._split_grouped(data, combined_aes)
        return self._split_rows(data)

    def _split_rows(self, data):
        """Row-level predicate."""
        if isinstance(self.predicate, str):
            try:
                mask = data.eval(self.predicate)
            except Exception:
                mask = data.query(self.predicate).index
                full_mask = pd.Series(False, index=data.index)
                full_mask.loc[mask] = True
                return full_mask
            if isinstance(mask, pd.Series):
                return mask.astype(bool)
            return pd.Series(mask, index=data.index).astype(bool)
        elif callable(self.predicate):
            result = self.predicate(data)
            if isinstance(result, pd.Series):
                return result.astype(bool)
            return pd.Series(result, index=data.index).astype(bool)
        raise TypeError(f"predicate must be str or callable, got {type(self.predicate)}")

    def _split_grouped(self, data, combined_aes):
        """Group-level predicate."""
        group_col = None
        for key in ('color', 'colour', 'group'):
            if key in combined_aes.mappings:
                group_col = combined_aes.mappings[key]
                break
        if group_col is None or group_col not in data.columns:
            warnings.warn("gghighlight: use_group_by=True but no group/color aesthetic found; "
                          "falling back to row-level predicate.")
            return self._split_rows(data)

        if isinstance(self.predicate, str):
            # Evaluate predicate per group; keep groups where it is True
            keep_groups = set()
            scores = {}
            for name, grp in data.groupby(group_col, sort=False):
                try:
                    val = grp.eval(self.predicate)
                except Exception:
                    val = len(grp.query(self.predicate)) > 0
                if isinstance(val, pd.Series):
                    val = val.all()
                scores[name] = val
                if val:
                    keep_groups.add(name)
        elif callable(self.predicate):
            keep_groups = set()
            scores = {}
            for name, grp in data.groupby(group_col, sort=False):
                val = self.predicate(grp)
                if isinstance(val, (pd.Series, np.ndarray)):
                    val = bool(np.all(val))
                scores[name] = val
                if val:
                    keep_groups.add(name)
        else:
            raise TypeError(f"predicate must be str or callable, got {type(self.predicate)}")

        # Top-N filtering
        if self.n is not None and len(keep_groups) > self.n:
            # Sort by score descending, keep top n
            sorted_groups = sorted(keep_groups,
                                   key=lambda g: (scores.get(g, 0), str(g)),
                                   reverse=True)
            keep_groups = set(sorted_groups[:self.n])

        mask = data[group_col].isin(keep_groups)
        return mask

    # ── rendering helpers ─────────────────────────────────────────────

    def _render_layer_highlighted(self, layer, layer_data, combined_aes, ggplot_obj):
        """Render a single layer split into highlighted / unhighlighted parts."""
        mask = self._split(layer_data, combined_aes)
        highlighted_data = layer_data[mask]
        unhighlighted_data = layer_data[~mask]

        parts = []

        # 1) Unhighlighted (gray, low alpha)
        if len(unhighlighted_data) > 0:
            uh_plot = self._render_unhighlighted(layer, unhighlighted_data,
                                                 combined_aes, ggplot_obj)
            if uh_plot is not None:
                parts.append(uh_plot)

        # 2) Highlighted (full aesthetics)
        if len(highlighted_data) > 0:
            h_plot = layer._render(highlighted_data, combined_aes, ggplot_obj)
            if h_plot is not None:
                parts.append(h_plot)

        # 3) Optional labels
        if self.label_key and len(highlighted_data) > 0:
            lbl = self._render_labels(highlighted_data, combined_aes)
            if lbl is not None:
                parts.append(lbl)

        if not parts:
            return None
        result = parts[0]
        for p in parts[1:]:
            result = result * p
        return result

    def _render_unhighlighted(self, layer, data, combined_aes, ggplot_obj):
        """Render the unhighlighted portion of a layer in gray."""
        # Create a stripped-down copy of aesthetics (remove color/fill grouping)
        stripped_aes = copy.deepcopy(combined_aes)
        for key in ('color', 'colour', 'fill'):
            stripped_aes.mappings.pop(key, None)

        # Create a minimal ggplot proxy that won't apply color mappings
        proxy_gg = ggplot_obj._copy()
        proxy_gg.highlight = None  # prevent recursion

        try:
            uh_plot = layer._render(data, stripped_aes, proxy_gg)
        except Exception:
            return None
        if uh_plot is None:
            return None

        # Apply gray styling
        gray_opts = {
            'color': self.unhighlighted_colour,
            'alpha': self.unhighlighted_alpha,
        }
        try:
            uh_plot = uh_plot.opts(**gray_opts)
        except Exception:
            # Some elements use different opt names
            try:
                uh_plot = uh_plot.opts(
                    fill_color=self.unhighlighted_colour,
                    fill_alpha=self.unhighlighted_alpha,
                    line_color=self.unhighlighted_colour,
                    line_alpha=self.unhighlighted_alpha,
                )
            except Exception:
                pass
        return uh_plot

    def _render_labels(self, data, combined_aes):
        """Auto-label highlighted data using hv.Labels."""
        x_col = combined_aes.mappings.get('x')
        y_col = combined_aes.mappings.get('y')
        if x_col is None or y_col is None or x_col not in data.columns or y_col not in data.columns:
            return None
        if self.label_key not in data.columns:
            warnings.warn(f"gghighlight label_key '{self.label_key}' not in data columns")
            return None
        lbl_df = data[[x_col, y_col, self.label_key]].copy()
        lbl_df.columns = ['x', 'y', 'text']
        return hv.Labels(lbl_df, kdims=['x', 'y'], vdims=['text']).opts(
            text_font_size='9pt', text_color='black'
        )
