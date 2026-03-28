"""Configuration management for IPDMA."""

from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
import os


class EngineConfig(BaseModel):
    """Configuration for statistical engines."""

    n_chains: int = Field(default=4, ge=1, description="Number of MCMC chains")
    n_iter: int = Field(default=2000, ge=100, description="MCMC iterations")
    n_warmup: int = Field(default=1000, ge=100, description="Warmup iterations")
    target_accept: float = Field(default=0.9, ge=0.5, le=0.99)
    max_treedepth: int = Field(default=10, ge=5, le=20)
    seed: Optional[int] = Field(default=None)

    @field_validator("n_warmup")
    def warmup_less_than_iter(cls, v, values):
        if "n_iter" in values.data and v >= values.data["n_iter"]:
            raise ValueError("n_warmup must be less than n_iter")
        return v


class RConfig(BaseModel):
    """R integration configuration."""

    r_home: Optional[str] = Field(default=None)
    lib_paths: list[str] = Field(default_factory=list)
    cran_mirror: str = Field(default="https://cloud.r-project.org/")
    auto_install: bool = Field(default=True)
    timeout: int = Field(default=300)


class IPDMASettings(BaseSettings):
    """Global settings for IPDMA package."""

    # Paths
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".ipdma" / "cache")
    temp_dir: Path = Field(default_factory=lambda: Path.home() / ".ipdma" / "temp")

    # Engine settings
    engine: EngineConfig = Field(default_factory=EngineConfig)

    # R settings
    r_config: RConfig = Field(default_factory=RConfig)

    # Performance
    n_jobs: int = Field(default=-1, description="Number of parallel jobs")
    verbose: int = Field(default=1, ge=0, le=3)

    # Numerical settings
    convergence_tol: float = Field(default=1e-6, gt=0)
    max_iterations: int = Field(default=1000, gt=0)

    class Config:
        env_prefix = "IPDMA_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = IPDMASettings()