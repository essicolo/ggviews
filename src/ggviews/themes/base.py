"""
Base theme class for ggviews.

This module defines the base Theme class for all themes.
"""
from typing import Dict, List, Optional, Union, Any, Tuple

import holoviews as hv


class Theme:
    """Base class for all themes.
    
    Parameters
    ----------
    name : str
        Name of the theme.
    opts : dict
        Options to apply for the theme.
    """
    
    def __init__(self, name: str, opts: Dict[str, Any]):
        self.name = name
        self.opts = opts
    
    def apply(self, plot: hv.Element) -> hv.Element:
        """Apply the theme to a plot element, dropping any options unsupported by that element."""
        import re, warnings
        opts = dict(self.opts)
        # Attempt to apply all options, removing any that raise a ValueError
        while opts:
            try:
                return plot.opts(**opts)
            except ValueError as e:
                msg = str(e)
                # Look for unsupported option name
                m = re.search(r"Unexpected option '(.+?)'", msg)
                if m:
                    bad_opt = m.group(1)
                    warnings.warn(f"Theme '{self.name}' option '{bad_opt}' not supported by this element; dropping it.")
                    opts.pop(bad_opt, None)
                    continue
                # If we can't parse the error, re-raise
                raise
        # No options left or none applied
        return plot