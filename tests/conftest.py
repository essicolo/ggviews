"""Shared test fixtures for ggviews tests."""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_data():
    """Basic numeric DataFrame for scatter/line tests."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': np.random.randn(50),
        'y': np.random.randn(50),
    })


@pytest.fixture
def categorical_data():
    """DataFrame with categorical x and numeric y for bar/boxplot tests."""
    np.random.seed(42)
    return pd.DataFrame({
        'category': np.random.choice(['A', 'B', 'C'], 80),
        'value': np.random.randn(80) * 10 + 50,
        'group': np.random.choice(['X', 'Y'], 80),
    })


@pytest.fixture
def timeseries_data():
    """DataFrame for line/area plots with a sorted x axis."""
    np.random.seed(42)
    x = np.linspace(0, 10, 60)
    return pd.DataFrame({
        'x': x,
        'y': np.sin(x) + np.random.randn(60) * 0.3,
        'ymin': np.sin(x) - 0.5,
        'ymax': np.sin(x) + 0.5,
    })


@pytest.fixture
def labeled_data():
    """DataFrame with text labels for geom_text tests."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 15, 25, 30],
        'label': ['alpha', 'beta', 'gamma', 'delta', 'epsilon'],
    })
