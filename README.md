# ipdma

A Python scaffold for specifying Individual Patient Data (IPD) meta-analyses.

This package provides typed model-specification classes (`ModelSpec`,
`OutcomeSpec`, `TreatmentSpec`, `EstimandSpec`), configuration management, and
an `IPDAnalysis` API surface. The statistical engines are early-stage: the
current `IPDAnalysis.fit` returns a placeholder result container, so this is a
specification and packaging layer rather than a validated estimation library.

## Install

```bash
pip install -e .
```

Core runtime dependencies include numpy, scipy, pandas, and pydantic.

## Usage

```python
from ipdma import IPDAnalysis

analysis = IPDAnalysis.survival(method="cox")
results = analysis.fit(data)  # placeholder engine; see status below
print(results.summary())
```

A minimal console command is also installed:

```bash
ipdma --help
```

## Testing

```bash
pip install -e ".[dev]"
pytest -q
```

## Status

Beta scaffold. Model specification and configuration are implemented and
tested; estimation engines (survival, network meta-analysis, transportability,
causal inference) are planned but not yet implemented.

## License

MIT — see [LICENSE](LICENSE).
