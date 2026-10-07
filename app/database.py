from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import DATABASE_PATH


class AnalysisDatabase:
    def __init__(self, database_path: str | Path | None = None) -> None:
        self.database_path = Path(database_path) if database_path else DATABASE_PATH
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_description TEXT NOT NULL,
                    resume_text TEXT NOT NULL,
                    match_score REAL NOT NULL,
                    matched_skills TEXT NOT NULL,
                    missing_skills TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def create_analysis(
        self,
        job_description: str,
        resume_text: str,
        match_score: float,
        matched_skills: list[str],
        missing_skills: list[str],
    ) -> int:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO analyses (job_description, resume_text, match_score, matched_skills, missing_skills, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    job_description,
                    resume_text,
                    float(match_score),
                    json.dumps(matched_skills),
                    json.dumps(missing_skills),
                    created_at,
                ),
            )
            return int(cursor.lastrowid)

    def list_analyses(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM analyses ORDER BY created_at DESC"
            ).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_analysis(self, analysis_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM analyses WHERE id = ?",
                (analysis_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_dict(row)

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "job_description": row["job_description"],
            "resume_text": row["resume_text"],
            "match_score": float(row["match_score"]),
            "matched_skills": json.loads(row["matched_skills"]),
            "missing_skills": json.loads(row["missing_skills"]),
            "created_at": row["created_at"],
        }
