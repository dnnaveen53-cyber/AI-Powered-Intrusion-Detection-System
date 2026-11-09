from __future__ import annotations

import sqlite3
from pathlib import Path

from src.config.settings import PROJECT_ROOT


class DatabaseManager:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path) if db_path is not None else PROJECT_ROOT / "data" / "alerts.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source_ip TEXT,
                    details TEXT,
                    risk_score INTEGER,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()

    def insert_alert(
        self,
        event_type: str,
        category: str,
        confidence: float,
        source_ip: str | None = None,
        details: str | None = None,
        risk_score: int | None = None,
    ) -> int:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO alerts (event_type, category, confidence, source_ip, details, risk_score)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (event_type, category, confidence, source_ip, details, risk_score),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def fetch_recent_alerts(self, limit: int = 20) -> list[dict]:
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT id, event_type, category, confidence, source_ip, details, risk_score, created_at
                FROM alerts
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [
                {
                    "id": row[0],
                    "event_type": row[1],
                    "category": row[2],
                    "confidence": row[3],
                    "source_ip": row[4],
                    "details": row[5],
                    "risk_score": row[6],
                    "created_at": row[7],
                }
                for row in rows
            ]

    def get_dashboard_summary(self) -> dict:
        with sqlite3.connect(self.db_path) as connection:
            category_counts = connection.execute(
                """
                SELECT category, COUNT(*)
                FROM alerts
                GROUP BY category
                """
            ).fetchall()
            total_alerts = connection.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
            return {"total_alerts": total_alerts, "category_counts": {category: count for category, count in category_counts}}
