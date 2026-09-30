from __future__ import annotations

import math
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FlowerSample(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sepal_length: Annotated[float, Field(..., gt=0, le=20)]
    sepal_width: Annotated[float, Field(..., gt=0, le=20)]
    petal_length: Annotated[float, Field(..., gt=0, le=20)]
    petal_width: Annotated[float, Field(..., gt=0, le=20)]

    @field_validator("sepal_length", "sepal_width", "petal_length", "petal_width")
    @classmethod
    def validate_measurement(cls, value: float) -> float:
        numeric_value = float(value)
        if not math.isfinite(numeric_value):
            raise ValueError("Measurement must be a finite number.")
        return numeric_value


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float


class ModelInfoResponse(BaseModel):
    model: str
    dataset: str
    features: int
    classes: int
    feature_names: list[str]
    class_names: list[str]
