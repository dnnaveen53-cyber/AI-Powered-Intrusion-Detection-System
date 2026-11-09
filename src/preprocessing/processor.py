from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config.settings import CATEGORY_MAPPING


def normalize_attack_value(value: str) -> str:
    normalized = str(value).strip().lower()
    return CATEGORY_MAPPING.get(normalized, "normal")


def sanitize_numeric_columns(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    output = frame.copy()
    for column in columns:
        if column not in output.columns:
            continue
        output[column] = pd.to_numeric(output[column], errors="coerce")
    return output


def sanitize_categorical_columns(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    output = frame.copy()
    for column in columns:
        if column not in output.columns:
            continue
        output[column] = output[column].replace({"?": "missing", "": "missing", "NaN": "missing", "nan": "missing"})
        output[column] = output[column].fillna("missing").astype(str).str.strip().str.lower()
    return output


def build_preprocessor(X: pd.DataFrame, target_column: str | None = None) -> tuple[ColumnTransformer, list[str], list[str]]:
    numeric_columns = [column for column in X.columns if pd.api.types.is_numeric_dtype(X[column])]
    categorical_columns = [column for column in X.columns if not pd.api.types.is_numeric_dtype(X[column])]

    if target_column is not None and target_column in categorical_columns:
        categorical_columns.remove(target_column)

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_columns),
            ("categorical", categorical_transformer, categorical_columns),
        ],
        remainder="drop",
    )
    return preprocessor, numeric_columns, categorical_columns


def prepare_features(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    processed = frame.copy()
    labels = processed["family"].copy() if "family" in processed.columns else processed["attack_type"].copy()

    if "attack_type" in processed.columns:
        processed = processed.drop(columns=["attack_type"])
    if "difficulty" in processed.columns:
        processed = processed.drop(columns=["difficulty"])

    numeric_columns = [column for column in processed.columns if column not in {"protocol_type", "service", "flag"}]
    processed = sanitize_numeric_columns(processed, numeric_columns)
    processed = sanitize_categorical_columns(processed, ["protocol_type", "service", "flag"])
    processed["family"] = labels.map(normalize_attack_value)
    return processed, labels.map(normalize_attack_value)
