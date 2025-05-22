"""
Data loading utilities for ggviews.

This module provides functions for loading sample datasets included with ggviews.
"""
import os
from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional, Union, Any


# Dictionary to cache loaded datasets
_DATASETS = {}


def get_data_path() -> Path:
    """Get the path to the data directory.
    
    Returns
    -------
    Path
        Path to the data directory.
    """
    # Data is in package_root/data
    return Path(__file__).parent.parent.parent / "data"


def load_dataset(name: str) -> pd.DataFrame:
    """Load a dataset by name.
    
    Parameters
    ----------
    name : str
        Name of the dataset to load.
    
    Returns
    -------
    pandas.DataFrame
        The loaded dataset.
    
    Examples
    --------
    >>> from ggviews import load_dataset
    >>> diamonds = load_dataset('diamonds')
    >>> diamonds.head()
       carat      cut color clarity  depth  table  price     x     y     z
    0   0.23    Ideal     E     SI2   61.5   55.0    326  3.95  3.98  2.43
    """
    global _DATASETS
    
    # Return cached version if available
    if name in _DATASETS:
        return _DATASETS[name]
    
    # Find the CSV file
    data_path = get_data_path()
    file_path = data_path / f"{name}.csv"
    
    if not file_path.exists():
        # Check if we need to add .csv extension
        if not name.endswith(".csv"):
            file_path = data_path / f"{name}.csv"
        
        # If still doesn't exist, raise an error with available datasets
        if not file_path.exists():
            available = [p.stem for p in data_path.glob("*.csv")]
            raise ValueError(
                f"Dataset '{name}' not found. Available datasets: {', '.join(available)}"
            )
    
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Cache the dataset
    _DATASETS[name] = data
    
    return data


def list_datasets() -> List[str]:
    """List available datasets.
    
    Returns
    -------
    List[str]
        Names of available datasets.
    
    Examples
    --------
    >>> from ggviews import list_datasets
    >>> list_datasets()
    ['diamonds', 'mtcars', 'mpg', 'economics']
    """
    data_path = get_data_path()
    return [p.stem for p in data_path.glob("*.csv")]
