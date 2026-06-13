"""Basic tests for IPDMA package."""

import pytest
from ipdma import IPDAnalysis


def test_import():
    """Test that package can be imported."""
    from ipdma import IPDAnalysis, ModelSpec
    assert IPDAnalysis is not None
    assert ModelSpec is not None


def test_survival_creation(sample_survival_data):
    """Test survival analysis creation."""
    analysis = IPDAnalysis.survival(method="cox")
    assert analysis is not None

    results = analysis.fit(sample_survival_data)
    assert results is not None


def test_cli_entry_point_resolves():
    """The console script declared in pyproject.toml must be importable and run.

    Guards against the ``ipdma.cli.main:cli`` entry point silently referencing a
    missing module (a broken ``pip install``-time console command).
    """
    from ipdma.cli.main import cli

    assert cli([]) == 0
    assert cli(["--help"]) == 0