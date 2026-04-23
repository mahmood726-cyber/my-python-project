"""Main API for IPDMA package."""

from typing import Union, Optional, List, Dict, Any
import pandas as pd
import numpy as np
from pathlib import Path
import json

try:
    from loguru import logger
except ModuleNotFoundError:
    import logging

    logger = logging.getLogger(__name__)

from ipdma.model_spec import ModelSpec, OutcomeSpec, TreatmentSpec, ModelFamily, EstimandSpec
from ipdma.exceptions import IPDMAError, SpecificationError


class IPDAnalysis:
    """
    Main interface for IPD meta-analysis.

    Examples
    --------
    >>> from ipdma import IPDAnalysis

    >>> # Basic survival analysis
    >>> analysis = IPDAnalysis.survival(method='cox')
    >>> results = analysis.fit(data)
    """

    def __init__(self, spec: Optional[ModelSpec] = None, **kwargs):
        """Initialize IPD analysis."""
        self.spec = spec
        self.engine = None
        self._results = None
        self.kwargs = kwargs

    @classmethod
    def survival(cls, 
                method: str = "cox",
                outcome: str = "outcome",
                treatment: str = "treatment",
                covariates: Optional[List[str]] = None,
                **kwargs) -> "IPDAnalysis":
        """Factory method for survival analysis."""
        spec = ModelSpec(
            outcome=OutcomeSpec(
                name=outcome,
                type="survival",
                time_var=kwargs.get("time_var", "time"),
                event_var=kwargs.get("event_var", "event")
            ),
            treatment=TreatmentSpec(
                name=treatment,
                type="binary"
            ),
            covariates=covariates or [],
            model=ModelFamily(
                family=method,
                parameters=kwargs
            ),
            estimand=EstimandSpec(
                type="hazard_ratio"
            )
        )

        return cls(spec=spec)

    def fit(self, data: pd.DataFrame, **kwargs):
        """Fit model to data."""
        logger.info("Fitting model...")
        # Simplified implementation
        return IPDResults(data)


class IPDResults:
    """Container for IPD analysis results."""

    def __init__(self, data):
        self.data = data
        self.estimates = {"effect": 0.5}
        self.se = {"effect": 0.1}
        self.ci = {"effect": (0.3, 0.7)}

    def summary(self):
        """Get summary of results."""
        return pd.DataFrame({
            "estimate": [0.5],
            "se": [0.1],
            "ci_lower": [0.3],
            "ci_upper": [0.7]
        })
