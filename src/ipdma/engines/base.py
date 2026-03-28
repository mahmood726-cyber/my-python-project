"""Base classes for statistical engines."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple, Union
import numpy as np
import pandas as pd
from scipy import stats
import warnings
from loguru import logger

from ipdma.exceptions import ConvergenceError, DataError
from ipdma.config import settings


@dataclass
class ModelResults:
    """Container for model results."""

    estimates: Dict[str, float]
    se: Dict[str, float]
    ci: Dict[str, Tuple[float, float]]
    diagnostics: Dict[str, Any]

    # Optional fields
    posterior: Optional[Any] = None
    predictions: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> pd.DataFrame:
        """Create summary DataFrame."""
        rows = []
        for param in self.estimates:
            rows.append({
                "parameter": param,
                "estimate": self.estimates[param],
                "se": self.se.get(param, np.nan),
                "ci_lower": self.ci.get(param, (np.nan, np.nan))[0],
                "ci_upper": self.ci.get(param, (np.nan, np.nan))[1],
            })
        return pd.DataFrame(rows)

    def __str__(self) -> str:
        return self.summary().to_string()


class StatisticalEngine(ABC):
    """Abstract base class for statistical engines."""

    def __init__(self, spec: Optional["ModelSpec"] = None):
        """Initialize engine with optional specification."""
        self.spec = spec
        self.is_fitted = False
        self._results: Optional[ModelResults] = None

    @abstractmethod
    def fit(self, data: pd.DataFrame, **kwargs) -> ModelResults:
        """Fit model to data."""
        pass

    def validate_data(self, data: pd.DataFrame) -> None:
        """Validate input data."""
        if data.empty:
            raise DataError("Input data is empty")

        # Check for required columns
        if self.spec:
            required = [self.spec.outcome.name, self.spec.treatment.name]
            required.extend(self.spec.covariates)

            missing = set(required) - set(data.columns)
            if missing:
                raise DataError(f"Missing required columns: {missing}")

        # Check for all missing columns
        all_missing = data.isna().all()
        if any(all_missing):
            bad_cols = all_missing[all_missing].index.tolist()
            raise DataError(f"Columns with all missing values: {bad_cols}")

    def _compute_ci(self, 
                   estimate: float,
                   se: float,
                   level: float = 0.95) -> Tuple[float, float]:
        """Compute confidence interval."""
        z = stats.norm.ppf((1 + level) / 2)
        margin = z * se
        return (estimate - margin, estimate + margin)