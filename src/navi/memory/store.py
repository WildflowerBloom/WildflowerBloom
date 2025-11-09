"""SQLite-backed persistence layer for Navi interactions."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Protocol


class MemoryStore(Protocol):
    def log_interaction(self, record: Dict[str, Any]) -> int: ...

    def retrieve_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]: ...


@dataclass
class SQLiteMemoryStore:
    """Simple SQLite storage for interactions and mode transitions."""

    path: Path

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            self._init_db(conn)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL
            )
            """
        )

    def log_interaction(self, record: Dict[str, Any]) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO interactions (timestamp, data) VALUES (?, ?)",
                (record.get("timestamp"), json.dumps(record)),
            )
            return int(cursor.lastrowid)

    def retrieve_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Placeholder similarity using LIKE search."""
        if not query:
            return []
        pattern = f"%{query[:32]}%"
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT data FROM interactions WHERE data LIKE ? ORDER BY id DESC LIMIT ?",
                (pattern, limit),
            ).fetchall()
        return [json.loads(row["data"]) for row in rows]

