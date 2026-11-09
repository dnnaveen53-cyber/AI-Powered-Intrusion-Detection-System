from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score

from src.config.settings import ARTIFACTS_DIR, CATEGORY_ORDER, MODELS_DIR
from src.data.dataset_loader import load_nsl_kdd_data
from src.features.feature_selector import IntrusionFeatureSelector
from src.preprocessing.processor import build_preprocessor


class IDSModelTrainer:
    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
        self.train_df = train_df
        self.test_df = test_df

    def _prepare_datasets(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, object, object, list[str]]:
        train_features = self.train_df.drop(columns=["attack_type", "difficulty", "family"])
        train_target = self.train_df["family"]
        test_features = self.test_df.drop(columns=["attack_type", "difficulty", "family"])
        test_target = self.test_df["family"]

        train_features = train_features.copy()
        test_features = test_features.copy()

        for column in train_features.columns:
            if column in {"protocol_type", "service", "flag"}:
                train_features[column] = train_features[column].fillna("missing").astype(str).str.strip().str.lower()
                test_features[column] = test_features[column].fillna("missing").astype(str).str.strip().str.lower()
            else:
                train_features[column] = pd.to_numeric(train_features[column], errors="coerce")
                test_features[column] = pd.to_numeric(test_features[column], errors="coerce")

        preprocessor, _, _ = build_preprocessor(train_features)
        train_matrix = preprocessor.fit_transform(train_features)
        test_matrix = preprocessor.transform(test_features)

        selector = IntrusionFeatureSelector(k=min(40, train_matrix.shape[1]))
        train_matrix = selector.fit_transform(train_matrix, train_target)
        test_matrix = selector.transform(test_matrix)
        return train_matrix, train_target.to_numpy(), test_matrix, test_target.to_numpy(), preprocessor, selector, list(train_features.columns)

    def train(self) -> dict:
        x_train, y_train, x_test, y_test, preprocessor, selector, feature_order = self._prepare_datasets()

        model = RandomForestClassifier(
            n_estimators=250,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced_subsample",
            min_samples_leaf=1,
        )
        model.fit(x_train, y_train)

        predictions = model.predict(x_test)
        metrics = {
            "accuracy": float(accuracy_score(y_test, predictions)),
            "precision": float(precision_score(y_test, predictions, average="weighted", zero_division=0)),
            "recall": float(recall_score(y_test, predictions, average="weighted", zero_division=0)),
            "f1": float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
        }

        
        report = classification_report(
            y_test,
            predictions,
            labels=CATEGORY_ORDER,
            target_names=CATEGORY_ORDER,
            output_dict=True,
            zero_division=0,
        )
        metrics["report"] = report


        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        model_path = MODELS_DIR / "ids_pipeline.joblib"
        metadata_path = ARTIFACTS_DIR / "training_summary.json"
        bundle = {
            "preprocessor": preprocessor,
            "selector": selector,
            "model": model,
            "classes": CATEGORY_ORDER,
            "feature_order": feature_order,
            "metrics": metrics,
        }
        joblib.dump(bundle, model_path)
        with metadata_path.open("w", encoding="utf-8") as handle:
            json.dump({"metrics": metrics, "classes": CATEGORY_ORDER}, handle, indent=2)

        return metrics


def train_model_from_dataset() -> dict:
    train_df, test_df = load_nsl_kdd_data()
    trainer = IDSModelTrainer(train_df, test_df)
    return trainer.train()
