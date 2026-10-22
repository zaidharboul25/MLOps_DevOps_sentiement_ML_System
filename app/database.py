import os
import sqlite3
from pathlib import Path
from typing import Iterator

from fastapi import Request


def database_path(request: Request) -> Path:
    return Path(request.app.state.database_path)


def connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL CHECK(length(trim(content)) > 0 AND length(content) <= 5000),
                created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now'))
            )"""
        )


def get_database_path() -> Path:
    return Path(os.environ.get("SENTIMENTAI_DATABASE_PATH", "data/sentimentai.db"))
