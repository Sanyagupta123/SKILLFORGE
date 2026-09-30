from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np

from app.config import CLASS_NAMES, FEATURE_NAMES, MODEL_PATH
from app.schemas import FlowerSample, ModelInfoResponse, PredictionResponse


class ModelService:
    def __init__(self, model_path: Path | str | None = None):
        self.model_path = Path(model_path) if model_path else MODEL_PATH
        self.model = None
        self.load_model()

    def load_model(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        self.model = joblib.load(self.model_path)

    def _feature_matrix(self, samples: list[FlowerSample]) -> np.ndarray:
        return np.asarray(
            [[float(getattr(sample, name)) for name in FEATURE_NAMES] for sample in samples],
            dtype=float,
        )

    def predict_one(self, sample: FlowerSample) -> PredictionResponse:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        feature_row = np.asarray(
            [[float(getattr(sample, name)) for name in FEATURE_NAMES]],
            dtype=float,
        )
        prediction_index = int(self.model.predict(feature_row)[0])
        probabilities = self.model.predict_proba(feature_row)[0]

        return PredictionResponse(
            prediction=CLASS_NAMES[prediction_index],
            confidence=float(np.max(probabilities)),
        )

    def predict_batch(self, samples: list[FlowerSample]) -> list[PredictionResponse]:
        if not samples:
            raise ValueError("At least one sample is required.")

        feature_matrix = self._feature_matrix(samples)
        predictions = self.model.predict(feature_matrix)
        probabilities = self.model.predict_proba(feature_matrix)

        results: list[PredictionResponse] = []
        for prediction_index, probability_row in zip(predictions, probabilities):
            results.append(
                PredictionResponse(
                    prediction=CLASS_NAMES[int(prediction_index)],
                    confidence=float(np.max(probability_row)),
                )
            )
        return results

    def model_info(self) -> ModelInfoResponse:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        model_name = type(self.model).__name__
        classes = getattr(self.model, "classes_", list(range(len(CLASS_NAMES))))

        return ModelInfoResponse(
            model=model_name,
            dataset="Iris",
            features=int(getattr(self.model, "n_features_in_", len(FEATURE_NAMES))),
            classes=len(classes),
            feature_names=FEATURE_NAMES,
            class_names=CLASS_NAMES,
        )
