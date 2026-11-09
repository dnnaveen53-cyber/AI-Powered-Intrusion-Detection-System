from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.alerts.alert_manager import AlertManager
from src.data.dataset_loader import load_nsl_kdd_data
from src.prediction.inference_service import IDSInferenceService
from src.preprocessing.processor import normalize_attack_value


def test_attack_family_mapping() -> None:
    assert normalize_attack_value("smurf") == "DoS"
    assert normalize_attack_value("satan") == "Probe"
    assert normalize_attack_value("guess_passwd") == "R2L"
    assert normalize_attack_value("buffer_overflow") == "U2R"
    assert normalize_attack_value("normal") == "normal"


def test_dataset_download_and_load() -> None:
    train_df, test_df = load_nsl_kdd_data()
    assert not train_df.empty
    assert not test_df.empty
    assert "family" in train_df.columns
    assert "family" in test_df.columns


def test_alert_manager_records_intrusion(tmp_path: Path) -> None:
    db_path = tmp_path / "alerts.db"
    manager = AlertManager(db_path=db_path)
    result = manager.create_alert("Probe", 0.98, source_ip="10.0.0.2", details="suspicious scan")
    assert result["category"] == "Probe"
    assert result["risk_score"] == 98
    assert manager.summary()["total_alerts"] >= 1


def test_inference_service_predicts_real_dataset_row() -> None:
    service = IDSInferenceService()
    train_df, _ = load_nsl_kdd_data()
    row = train_df.iloc[0].to_dict()
    row.pop("family", None)
    row.pop("attack_type", None)
    row.pop("difficulty", None)
    result = service.predict_record(row)
    assert result["prediction"] in {"normal", "DoS", "Probe", "R2L", "U2R"}
    assert 0.0 <= result["confidence"] <= 1.0
