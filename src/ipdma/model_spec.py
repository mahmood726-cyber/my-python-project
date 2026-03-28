"""Model specification classes using Pydantic."""

from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
import json
from pathlib import Path


class OutcomeSpec(BaseModel):
    """Specification for outcome variable."""

    name: str
    type: Literal["continuous", "binary", "count", "survival", "competing_risks"]
    time_var: Optional[str] = None
    event_var: Optional[str] = None
    competing_events: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_survival_fields(self):
        """Ensure survival outcomes have required fields."""
        if self.type in ["survival", "competing_risks"]:
            if not self.time_var or not self.event_var:
                raise ValueError(
                    f"{self.type} outcome requires time_var and event_var"
                )
        return self


class TreatmentSpec(BaseModel):
    """Specification for treatment variable."""

    name: str
    type: Literal["binary", "continuous", "categorical", "network"]
    reference_level: Optional[Union[str, int, float]] = None
    levels: Optional[List[Union[str, int]]] = None

    @model_validator(mode="after")
    def validate_levels(self):
        """Ensure categorical/network treatments have levels defined."""
        if self.type in ["categorical", "network"] and not self.levels:
            raise ValueError(f"{self.type} treatment requires levels")
        return self


class ModelFamily(BaseModel):
    """Model family specification."""

    family: Literal[
        "cox", "royston_parmar", "weibull", "joint",
        "standard_nma", "ml_nmr", "component_nma",
        "grf", "bcf", "tmle"
    ]
    link: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class EstimandSpec(BaseModel):
    """Estimand specification following ICH E9(R1)."""

    type: Literal["ate", "att", "cate", "survivor_average", "rmst", "hazard_ratio"]
    target_population: Literal["trial", "target", "combined"] = "trial"
    time_horizon: Optional[float] = None
    subgroups: Optional[List[str]] = None


class MissingDataSpec(BaseModel):
    """Missing data handling specification."""

    strategy: Literal["complete_case", "mar", "j2r", "cr", "cir", "lmcf", "tipping_point"]
    n_imputations: int = Field(default=20, ge=1)
    sensitivity_delta: Optional[List[float]] = None
    auxiliary_vars: Optional[List[str]] = None


class ModelSpec(BaseModel):
    """Complete model specification."""

    # Basic specifications
    outcome: OutcomeSpec
    treatment: TreatmentSpec
    covariates: List[str] = Field(default_factory=list)
    effect_modifiers: List[str] = Field(default_factory=list)

    # Model specifications
    model: ModelFamily
    estimand: EstimandSpec

    # Data handling
    missing_data: Optional[MissingDataSpec] = None
    clustering: Optional[str] = None
    weights: Optional[str] = None

    # Analysis settings
    confidence_level: float = Field(default=0.95, gt=0, lt=1)
    multiple_testing: Optional[Literal["bonferroni", "holm", "fdr"]] = None

    # Metadata
    protocol_version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = None

    @field_validator("confidence_level")
    def validate_confidence_level(cls, v):
        if not 0 < v < 1:
            raise ValueError("confidence_level must be between 0 and 1")
        return v

    def to_json(self, path: Optional[Path] = None) -> str:
        """Export specification to JSON."""
        json_str = self.model_dump_json(indent=2)
        if path:
            Path(path).write_text(json_str)
        return json_str

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "ModelSpec":
        """Load specification from JSON."""
        data = json.loads(Path(path).read_text())
        return cls(**data)