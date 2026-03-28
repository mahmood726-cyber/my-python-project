"""Pytest configuration and fixtures."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path


@pytest.fixture
def sample_survival_data():
    """Generate sample survival data."""
    np.random.seed(42)
    n = 200

    # Generate covariates
    age = np.random.normal(50, 10, n)
    sex = np.random.binomial(1, 0.5, n)
    treatment = np.random.binomial(1, 0.5, n)

    # Generate survival times
    time = np.random.exponential(10, n)
    event = np.random.binomial(1, 0.7, n)

    return pd.DataFrame({
        "time": time,
        "event": event,
        "treatment": treatment,
        "age": age,
        "sex": sex,
        "outcome": np.random.normal(0, 1, n)
    })