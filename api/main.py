from __future__ import annotations

import json
from typing import Any

from fastapi import FastAPI

from src.alerts.alert_manager import AlertManager
from src.config.settings import DATASET_SELECTION_NOTE
from src.prediction.inference_service import IDSInferenceService
from src.utils.logger import setup_logging

logger = setup_logging("api")

app = FastAPI(title="AI-Powered Intrusion Detection System")
service = IDSInferenceService()
alert_manager = AlertManager()


@app.get("/health")
def health() -> dict[str, Any]:
    logger.info("Health check requested")
    return {
        "status": "ok",
        "service": "AI-Powered IDS",
        "dataset": "NSL-KDD",
        "dataset_note": DATASET_SELECTION_NOTE,
    }


@app.post("/predict")
def predict(payload: dict[str, Any]) -> dict[str, Any]:
    logger.info("Prediction request received")
    record = payload.get("record", payload)
    if isinstance(record, list):
        if not record:
            logger.warning("Empty prediction record list supplied")
            return {"status": "error", "message": "No records provided."}
        result = service.predict_record(record[0])
    else:
        result = service.predict_record(record)

    if result["prediction"] != "Normal":
        alert_manager.create_alert(
            result["prediction"],
            result["confidence"],
            source_ip=str(payload.get("source_ip", "unknown")),
            details=json.dumps({"feature_record": record}),
        )
        logger.info("Intrusion alert recorded for category %s", result["prediction"])

    return {"status": "ok", **result}


@app.get("/alerts")
def recent_alerts() -> dict[str, Any]:
    logger.info("Recent alerts requested")
    return {"alerts": alert_manager.recent_alerts(10)}
