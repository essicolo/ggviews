"""
ggrepel-style label repulsion for ggviews

Provides ``geom_text_repel`` and ``geom_label_repel`` which automatically
position text labels so they do not overlap each other or the data points,
and draw thin segments connecting each label to its data point.

The algorithm is a simplified force-directed layout:

1. Initialise each label at its data point (+ any nudge).
2. Estimate bounding boxes from text length and font size.
3. Iterate (default 100 rounds):
   a. Push overlapping label pairs apart (repulsion).
   b. Push labels away from nearby data points.
   c. Pull labels back toward their data point (spring).
4. Render the final positions as ``hv.Labels`` plus ``hv.Segments``.
"""

import holoviews as hv
import pandas as pd
import numpy as np
from typing import Optional
import warnings

from .geoms import GeomLayer


# ---------------------------------------------------------------------------
# Force-directed repulsion engine
# ---------------------------------------------------------------------------

def _estimate_bbox_size(text: str, font_size_pt: float,
                        x_range: float, y_range: float,
                        plot_width: int = 500, plot_height: int = 400):
    """Estimate label bounding-box in *data* coordinates.

    Uses a rough heuristic: each character ≈ 0.6× font height in width.
    The result is scaled from pixel space into data space so that the
    repulsion forces are in the same units as the data.
    """
    # Approximate pixel size
    char_w_px = font_size_pt * 0.6
    char_h_px = font_size_pt * 1.3
    w_px = len(str(text)) * char_w_px + 6  # small padding
    h_px = char_h_px + 4

    # Convert to data units
    w_data = w_px / plot_width * x_range if x_range > 0 else w_px / plot_width
    h_data = h_px / plot_height * y_range if y_range > 0 else h_px / plot_height
    return w_data, h_data


def _boxes_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    """Check if two axis-aligned bounding boxes overlap."""
    return (abs(ax - bx) < (aw + bw) / 2 and
            abs(ay - by) < (ah + bh) / 2)


def repel_labels(x_orig, y_orig, texts, font_size=12,
                 box_padding=0.25, point_padding=0.01,
                 force=1.0, max_iter=100, seed=42):
    """Compute non-overlapping label positions.

    Parameters
    ----------
    x_orig, y_orig : array-like
        Original data-point positions (1-D, same length).
    texts : array-like of str
        Label strings (used only to estimate widths).
    font_size : float
        Font size in points.
    box_padding : float
        Extra padding around each label box, in fraction of box size.
    point_padding : float
        Minimum distance (data units) between a label centre and *any*
        data point.
    force : float
        Multiplier on the repulsion force (higher = more aggressive).
    max_iter : int
        Number of iterations.
    seed : int or None
        Random seed for tie-breaking jitter.

    Returns
    -------
    x_final, y_final : np.ndarray
        Adjusted label positions.
    """
    rng = np.random.RandomState(seed)
    n = len(x_orig)
    if n == 0:
        return np.array([]), np.array([])

    x_orig = np.asarray(x_orig, dtype=float)
    y_orig = np.asarray(y_orig, dtype=float)
    texts = [str(t) for t in texts]

    # Data ranges for bbox estimation
    x_range = float(x_orig.max() - x_orig.min()) if (x_orig.max() - x_orig.min()) > 0 else 1.0
    y_range = float(y_orig.max() - y_orig.min()) if (y_orig.max() - y_orig.min()) > 0 else 1.0

    # Estimate bounding boxes
    widths = np.empty(n)
    heights = np.empty(n)
    for i in range(n):
        w, h = _estimate_bbox_size(texts[i], font_size, x_range, y_range)
        widths[i] = w * (1 + box_padding)
        heights[i] = h * (1 + box_padding)

    # Initialise label positions slightly offset from data points
    x_lab = x_orig.copy() + rng.uniform(-x_range * 0.005, x_range * 0.005, n)
    y_lab = y_orig.copy() + rng.uniform(y_range * 0.01, y_range * 0.03, n)

    step = force * 0.02  # base step size

    for iteration in range(max_iter):
        fx = np.zeros(n)
        fy = np.zeros(n)

        # --- label-label repulsion ---
        for i in range(n):
            for j in range(i + 1, n):
                if _boxes_overlap(x_lab[i], y_lab[i], widths[i], heights[i],
                                  x_lab[j], y_lab[j], widths[j], heights[j]):
                    dx = x_lab[i] - x_lab[j]
                    dy = y_lab[i] - y_lab[j]
                    dist = max(np.sqrt(dx * dx + dy * dy), 1e-6)
                    # Push proportional to overlap
                    push = step * x_range / dist
                    fx[i] += dx / dist * push
                    fy[i] += dy / dist * push
                    fx[j] -= dx / dist * push
                    fy[j] -= dy / dist * push

        # --- label-point repulsion ---
        for i in range(n):
            for j in range(n):
                dx = x_lab[i] - x_orig[j]
                dy = y_lab[i] - y_orig[j]
                dist = np.sqrt(dx * dx + dy * dy)
                if dist < max(widths[i], heights[i]) * 0.8 and dist > 1e-6:
                    push = step * x_range * 0.5 / dist
                    fx[i] += dx / dist * push
                    fy[i] += dy / dist * push

        # --- spring toward original position ---
        spring = 0.02 * force
        fx -= spring * (x_lab - x_orig)
        fy -= spring * (y_lab - y_orig)

        # Apply forces with decay
        decay = 1.0 - iteration / max_iter
        x_lab += fx * decay
        y_lab += fy * decay

    return x_lab, y_lab


# ---------------------------------------------------------------------------
# geom_text_repel
# ---------------------------------------------------------------------------

class geom_text_repel(GeomLayer):
    """Text labels with automatic repulsion to avoid overlaps.

    Equivalent to ``ggrepel::geom_text_repel`` in R.  Labels are pushed
    away from each other and from data points, and thin segments connect
    each label to its data point.

    Parameters
    ----------
    mapping : aes
        Must include ``x``, ``y``, ``label``.
    nudge_x, nudge_y : float
        Fixed offset applied before repulsion.
    size : float
        Font size in points.
    color : str
        Text colour.
    segment_color : str
        Colour of the connecting segment.
    segment_alpha : float
        Transparency of the connecting segment.
    box_padding : float
        Extra padding around label bounding boxes.
    point_padding : float
        Minimum distance from label to any data point.
    force : float
        Strength of the repulsion (default 1).
    max_iter : int
        Iterations for the layout algorithm.
    max_overlaps : int
        If there are more labels than this, skip repulsion and fall back
        to plain labels (performance guard).
    seed : int or None
        Random seed for reproducibility.

    Examples
    --------
    >>> geom_text_repel(aes(x='x', y='y', label='name'))
    >>> geom_text_repel(aes(label='city'), size=10, color='navy')
    """

    def __init__(self, mapping=None, data=None,
                 nudge_x=0, nudge_y=0,
                 size=10, color='black', alpha=1,
                 segment_color='gray', segment_alpha=0.5,
                 segment_size=0.5,
                 box_padding=0.25, point_padding=0.01,
                 force=1.0, max_iter=100, max_overlaps=50,
                 seed=42, **kwargs):
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'nudge_x': nudge_x,
            'nudge_y': nudge_y,
            'size': size,
            'color': color,
            'alpha': alpha,
            'segment_color': segment_color,
            'segment_alpha': segment_alpha,
            'segment_size': segment_size,
            'box_padding': box_padding,
            'point_padding': point_padding,
            'force': force,
            'max_iter': max_iter,
            'max_overlaps': max_overlaps,
            'seed': seed,
        })

    def _render(self, data, combined_aes, ggplot_obj):
        required = ['x', 'y', 'label']
        for a in required:
            if a not in combined_aes.mappings:
                raise ValueError(f"geom_text_repel requires '{a}' aesthetic")

        x_col = combined_aes.mappings['x']
        y_col = combined_aes.mappings['y']
        label_col = combined_aes.mappings['label']

        missing = [c for c in [x_col, y_col, label_col] if c not in data.columns]
        if missing:
            warnings.warn(f"Columns not found: {missing}")
            return None

        df = data[[x_col, y_col, label_col]].dropna().copy()
        if df.empty:
            return None

        x_orig = df[x_col].values.astype(float) + self.params['nudge_x']
        y_orig = df[y_col].values.astype(float) + self.params['nudge_y']
        texts = df[label_col].astype(str).values

        # Run repulsion
        if len(texts) <= self.params['max_overlaps']:
            x_lab, y_lab = repel_labels(
                x_orig, y_orig, texts,
                font_size=self.params['size'],
                box_padding=self.params['box_padding'],
                point_padding=self.params['point_padding'],
                force=self.params['force'],
                max_iter=self.params['max_iter'],
                seed=self.params['seed'],
            )
        else:
            x_lab, y_lab = x_orig.copy(), y_orig.copy()

        # Build segments (data-point → label)
        seg_df = pd.DataFrame({
            'x0': x_orig, 'y0': y_orig,
            'x1': x_lab, 'y1': y_lab,
        })
        # Only draw segments when label actually moved
        moved = np.sqrt((x_lab - x_orig) ** 2 + (y_lab - y_orig) ** 2)
        x_range = float(x_orig.max() - x_orig.min()) if (x_orig.max() - x_orig.min()) > 0 else 1.0
        threshold = x_range * 0.01
        seg_df = seg_df[moved > threshold]

        segments = hv.Segments(seg_df, kdims=['x0', 'y0', 'x1', 'y1']).opts(
            color=self.params['segment_color'],
            alpha=self.params['segment_alpha'],
            line_width=self.params['segment_size'],
        )

        # Build labels
        label_df = pd.DataFrame({'x': x_lab, 'y': y_lab, 'text': texts})
        labels = hv.Labels(label_df, kdims=['x', 'y'], vdims=['text']).opts(
            text_color=self.params['color'],
            text_font_size=f"{self.params['size']}pt",
            text_alpha=self.params['alpha'],
        )

        return segments * labels


# ---------------------------------------------------------------------------
# geom_label_repel
# ---------------------------------------------------------------------------

class geom_label_repel(geom_text_repel):
    """Labels with background boxes and automatic repulsion.

    Like ``geom_text_repel`` but each label gets a background rectangle
    (via a Bokeh hook), similar to ``ggrepel::geom_label_repel``.

    Additional Parameters
    ---------------------
    fill : str
        Background fill colour (default ``'white'``).
    label_padding : float
        Padding inside the background box.
    """

    def __init__(self, mapping=None, data=None,
                 fill='white', label_padding=0.25, **kwargs):
        kwargs.setdefault('color', 'black')
        super().__init__(mapping, data, **kwargs)
        self.params.update({
            'fill': fill,
            'label_padding': label_padding,
        })

    def _render(self, data, combined_aes, ggplot_obj):
        result = super()._render(data, combined_aes, ggplot_obj)
        if result is None:
            return None

        bg_fill = self.params.get('fill', 'white')
        bg_alpha = 0.85

        def _add_background(plot, element):
            for renderer in plot.state.renderers:
                glyph = getattr(renderer, 'glyph', None)
                if glyph is None:
                    continue
                if hasattr(glyph, 'background_fill_color'):
                    glyph.background_fill_color = bg_fill
                    glyph.background_fill_alpha = bg_alpha
                    if hasattr(glyph, 'border_line_color'):
                        glyph.border_line_color = 'gray'
                        glyph.border_line_alpha = 0.5

        return result.opts(hooks=[_add_background])


# ---------------------------------------------------------------------------
__all__ = [
    'geom_text_repel',
    'geom_label_repel',
    'repel_labels',
]
