from __future__ import annotations

from src.database.db_manager import DatabaseManager


class AlertManager:
    def __init__(self, db_path=None) -> None:
        self.db = DatabaseManager(db_path=db_path)

    def create_alert(self, category: str, confidence: float, *, source_ip: str | None = None, details: str | None = None) -> dict:
        risk_score = int(round(confidence * 100))
        record_id = self.db.insert_alert(
            event_type="intrusion_detected",
            category=category,
            confidence=float(confidence),
            source_ip=source_ip,
            details=details,
            risk_score=risk_score,
        )
        return {"id": record_id, "category": category, "confidence": confidence, "risk_score": risk_score}

    def recent_alerts(self, limit: int = 10) -> list[dict]:
        return self.db.fetch_recent_alerts(limit=limit)

    def summary(self) -> dict:
        return self.db.get_dashboard_summary()
