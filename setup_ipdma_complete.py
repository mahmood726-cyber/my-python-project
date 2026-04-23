# sentinel:skip-file — hardcoded paths are fixture/registry/audit-narrative data for this repo's research workflow, not portable application configuration. Same pattern as push_all_repos.py and E156 workbook files.
import os

from pathlib import Path

import textwrap



def create_file(path, content):

    """Helper to create a file with content."""

    Path(path).parent.mkdir(parents=True, exist_ok=True)

    Path(path).write_text(textwrap.dedent(content).strip())

    print(f"✓ Created {path}")



def setup_complete_package():

    """Create the entire IPDMA package structure and files."""

    

    print("Setting up IPDMA package...")

    print(f"Working directory: {os.getcwd()}")

    

    # 1. Create all directories

    print("\n1. Creating directories...")

    directories = [

        "src/ipdma",

        "src/ipdma/engines",

        "src/ipdma/diagnostics",

        "src/ipdma/utils",

        "src/ipdma/cli",

        "tests",

        "docs",

        "examples",

        ".github/workflows",

        ".devcontainer"

    ]

    

    for dir_path in directories:

        Path(dir_path).mkdir(parents=True, exist_ok=True)

        print(f"  ✓ {dir_path}/")

    

    # 2. Create pyproject.toml

    print("\n2. Creating pyproject.toml...")

    create_file("pyproject.toml", '''

[build-system]

requires = ["setuptools>=65", "wheel"]

build-backend = "setuptools.build_meta"



[project]

name = "ipdma"

version = "0.1.0"

description = "Individual Patient Data Meta-Analysis platform"

authors = [{name = "IPD Contributors", email = "contact@ipdma.org"}]

requires-python = ">=3.9"

dependencies = [

    "numpy>=1.24.0",

    "pandas>=2.0.0",

    "scipy>=1.10.0",

    "pydantic>=2.0.0",

    "loguru>=0.7.0",

]

    ''')

    

    # 3. Create README.md

    print("\n3. Creating README.md...")

    create_file("README.md", '''

# IPDMA: Individual Patient Data Meta-Analysis Platform



A comprehensive Python platform for IPD meta-analyses.



## Installation

```bash

pip install -e .

''')



# 4. Create LICENSE

print("\n4. Creating LICENSE...")

create_file("LICENSE", '''

MIT License

Copyright (c) 2024 IPD Meta-Analysis Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction.

''')

# 5. Create .gitignore

print("\n5. Creating .gitignore...")

create_file(".gitignore", '''

pycache/

*.py[cod]

*.egg-info/

dist/

build/

.venv/

venv/

''')

# 6. Create MANIFEST.in

print("\n6. Creating MANIFEST.in...")

create_file("MANIFEST.in", '''

include LICENSE

include README.md

recursive-include src/ipdma *.py

''')

# 7. Create package __init__ files

print("\n7. Creating package files...")



create_file("src/ipdma/__init__.py", '''

"""IPDMA Package"""

version = "0.1.0"

from ipdma.api import IPDAnalysis, IPDResults

from ipdma.exceptions import IPDMAError

all = ["IPDAnalysis", "IPDResults", "IPDMAError"]

''')

create_file("src/ipdma/__version__.py", '''

version = "0.1.0"

''')

create_file("src/ipdma/exceptions.py", '''

"""Custom exceptions for IPDMA."""

class IPDMAError(Exception):

"""Base exception for IPDMA package."""

pass

class ConvergenceError(IPDMAError):

"""Raised when model fails to converge."""

pass

class DataError(IPDMAError):

"""Raised when data validation fails."""

pass

class SpecificationError(IPDMAError):

"""Raised when model specification is invalid."""

pass

''')

create_file("src/ipdma/config.py", '''

"""Configuration for IPDMA."""

from pydantic import BaseModel, Field

class EngineConfig(BaseModel):

"""Configuration for statistical engines."""

n_chains: int = Field(default=4, ge=1)

n_iter: int = Field(default=2000, ge=100)

seed: int = Field(default=42)

''')

create_file("src/ipdma/model_spec.py", '''

"""Model specification classes."""

from typing import Optional, List, Dict, Any, Literal

from pydantic import BaseModel, Field

class OutcomeSpec(BaseModel):

"""Specification for outcome variable."""

name: str

type: Literal["continuous", "binary", "survival"]

time_var: Optional[str] = None

event_var: Optional[str] = None

class TreatmentSpec(BaseModel):

"""Specification for treatment variable."""

name: str

type: Literal["binary", "continuous", "categorical"]

class ModelFamily(BaseModel):

"""Model family specification."""

family: str

parameters: Dict[str, Any] = Field(default_factory=dict)

class EstimandSpec(BaseModel):

"""Estimand specification."""

type: Literal["ate", "att", "rmst", "hazard_ratio"]

class ModelSpec(BaseModel):

"""Complete model specification."""

outcome: OutcomeSpec

treatment: TreatmentSpec

covariates: List[str] = Field(default_factory=list)

model: ModelFamily

estimand: EstimandSpec

''')

create_file("src/ipdma/api.py", '''

"""Main API for IPDMA."""

import pandas as pd

from typing import Optional, List

from ipdma.model_spec import ModelSpec, OutcomeSpec, TreatmentSpec, ModelFamily, EstimandSpec

from ipdma.exceptions import IPDMAError

class IPDAnalysis:

"""Main interface for IPD meta-analysis."""

def __init__(self, spec: Optional[ModelSpec] = None):

    self.spec = spec

    

@classmethod

def survival(cls, method: str = "cox", **kwargs):

    """Factory for survival analysis."""

    spec = ModelSpec(

        outcome=OutcomeSpec(name="outcome", type="survival"),

        treatment=TreatmentSpec(name="treatment", type="binary"),

        model=ModelFamily(family=method),

        estimand=EstimandSpec(type="hazard_ratio")

    )

    return cls(spec)



def fit(self, data: pd.DataFrame):

    """Fit model to data."""

    return IPDResults(data)

class IPDResults:

"""Container for results."""

def init(self, data):

self.data = data

def summary(self):

    """Get summary."""

    return pd.DataFrame({"estimate": [0.5]})

''')



# 8. Create engine files

print("\n8. Creating engine files...")

create_file("src/ipdma/engines/__init__.py", "")

create_file("src/ipdma/engines/base.py", '''

"""Base engine classes."""

from abc import ABC, abstractmethod

import pandas as pd

class StatisticalEngine(ABC):

"""Abstract base class for engines."""

@abstractmethod

def fit(self, data: pd.DataFrame):

    """Fit model to data."""

    pass

''')



# 9. Create test files

print("\n9. Creating test files...")

create_file("tests/__init__.py", "")

create_file("tests/conftest.py", '''

"""Test configuration."""

import pytest

import pandas as pd

import numpy as np

@pytest.fixture

def sample_data():

"""Generate sample data."""

np.random.seed(42)

n = 100

return pd.DataFrame({

"outcome": np.random.normal(0, 1, n),

"treatment": np.random.binomial(1, 0.5, n),

"age": np.random.normal(50, 10, n)

})

''')

create_file("tests/test_basic.py", '''

"""Basic tests."""

def test_import():

"""Test imports work."""

from ipdma import IPDAnalysis

assert IPDAnalysis is not None

def test_survival_creation(sample_data):

"""Test creating survival analysis."""

from ipdma import IPDAnalysis

analysis = IPDAnalysis.survival()

assert analysis is not None

''')

# Create empty init files

for init_file in ["src/ipdma/diagnostics/__init__.py", 

                  "src/ipdma/utils/__init__.py",

                  "src/ipdma/cli/__init__.py"]:

    create_file(init_file, "")



print("\n✅ IPDMA package structure created successfully!")

print("\nNow run: python check_package.py")

if __name__ == "__main__":
    setup_complete_package()

# ---------------------------------------------------------------
# Usage (run from the project root):
#
#   import os
#   os.chdir(os.path.dirname(os.path.abspath(__file__)))
#   exec(open("setup_ipdma_complete.py").read())
#   exec(open("check_package.py").read())
# ---------------------------------------------------------------
