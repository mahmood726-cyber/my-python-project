"""
IPDMA: Individual Patient Data Meta-Analysis

A specification and analysis scaffold for IPD meta-analyses. Model
specification and configuration are implemented; estimation engines for
survival analysis, network meta-analysis, transportability, and causal
inference are planned.
"""

try:
    from ipdma.__version__ import __version__
except ModuleNotFoundError:
    # setuptools_scm writes this file during build, but local checkouts should
    # remain importable for tests and direct development.
    __version__ = "0+unknown"
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
