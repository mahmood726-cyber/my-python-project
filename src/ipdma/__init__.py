"""
IPDMA: Individual Patient Data Meta-Analysis Platform

A comprehensive platform for conducting state-of-the-art IPD meta-analyses
with support for survival analysis, network meta-analysis, transportability,
and causal inference methods.
"""

from ipdma.__version__ import __version__
from ipdma.api import IPDAnalysis, IPDResults
from ipdma.model_spec import ModelSpec
from ipdma.exceptions import (
    IPDMAError,
    ConvergenceError,
    DataError,
    SpecificationError,
)

__all__ = [
    "__version__",
    "IPDAnalysis",
    "IPDResults", 
    "ModelSpec",
    "IPDMAError",
    "ConvergenceError",
    "DataError",
    "SpecificationError",
]

# Package metadata
__author__ = "IPD Meta-Analysis Contributors"
__email__ = "contact@ipdma.org"
__license__ = "MIT"