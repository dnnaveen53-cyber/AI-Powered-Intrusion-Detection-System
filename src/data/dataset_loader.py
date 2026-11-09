from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config.settings import CATEGORY_MAPPING, RAW_DATA_DIR
from src.data.dataset_fetcher import download_dataset_if_missing


def read_field_names(raw_dir: Path | None = None) -> list[str]:
    raw_dir = raw_dir or RAW_DATA_DIR
    field_names_path = raw_dir / "Field Names.csv"
    if not field_names_path.exists():
        download_dataset_if_missing()
    names = pd.read_csv(field_names_path, header=None).iloc[:, 0].tolist()
    return [str(name).strip() for name in names]


def load_nsl_kdd_data(raw_dir: Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw_dir = raw_dir or RAW_DATA_DIR
    if not (raw_dir / "KDDTrain+.txt").exists() or not (raw_dir / "KDDTest+.txt").exists():
        download_dataset_if_missing()

    
    field_names = read_field_names(raw_dir)
    feature_columns = field_names[:41]
    columns = feature_columns + ["attack_type", "difficulty"]

    train_df = pd.read_csv(
        raw_dir / "KDDTrain+.txt",
        header=None,
        names=columns,
    )
    test_df = pd.read_csv(
        raw_dir / "KDDTest+.txt",
        header=None,
        names=columns,
    )

    def map_attack_families(df: pd.DataFrame) -> pd.Series:
        attack_names = (
            df["attack_type"]
            .astype(str)
            .str.strip()
            .str.lower()
            .str.rstrip(".")
        )

        mapped = attack_names.map(CATEGORY_MAPPING)
        unknown = sorted(attack_names[mapped.isna()].unique())

        if unknown:
            raise ValueError(
                "Unmapped NSL-KDD attack types found: "
                + ", ".join(unknown)
                + ". Update CATEGORY_MAPPING before training."
            )

        return mapped

    train_df["family"] = map_attack_families(train_df)
    test_df["family"] = map_attack_families(test_df)

    return train_df, test_df

