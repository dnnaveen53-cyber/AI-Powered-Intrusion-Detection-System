from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.config.settings import MODELS_DIR


class IDSInferenceService:
    def __init__(self, model_path: str | Path | None = None) -> None:
        self.model_path = Path(model_path) if model_path is not None else MODELS_DIR / "ids_pipeline.joblib"
        if not self.model_path.exists():
            from src.training.model_trainer import train_model_from_dataset

            train_model_from_dataset()
        self.bundle = joblib.load(self.model_path)
        self.model = self.bundle["model"]
        self.preprocessor = self.bundle["preprocessor"]
        self.selector = self.bundle["selector"]
        self.feature_order = self.bundle["feature_order"]
        self.classes = self.bundle["classes"]

    def predict_record(self, record: dict) -> dict:
        normalized = {}
        for key, value in record.items():
            if isinstance(value, np.generic):
                value = value.item()
            normalized[key] = value

        frame = pd.DataFrame([normalized])
        for column in self.feature_order:
            if column not in frame.columns:
                frame[column] = np.nan
        frame = frame[self.feature_order]

        observed = self.preprocessor.transform(frame)
        selected = self.selector.transform(observed)
        probabilities = self.model.predict_proba(selected)[0]
        predicted_index = int(np.argmax(probabilities))
        label = self.classes[predicted_index]
        confidence = float(probabilities[predicted_index])
        return {
            "prediction": label,
            "confidence": confidence,
            "risk_level": "high" if label != "normal" else "low",
            "class_probabilities": {class_name: float(probabilities[index]) for index, class_name in enumerate(self.classes)},
        }
