from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
APP_NAME = os.getenv("APP_NAME", "SkillForge")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(BASE_DIR / "skillforge.db")))
CORS_ORIGINS = [
    item.strip()
    for item in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if item.strip()
]
