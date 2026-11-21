"""
Persistent SQLite key-value cache for embeddings and LLM responses.
Ensures zero redundant API/local calls and instant reproducibility.
"""

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

CACHE_DB_PATH = Path(__file__).resolve().parent.parent / ".cache" / "cache.db"


def _get_connection() -> sqlite3.Connection:
    CACHE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(CACHE_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS kv_cache (
            namespace TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            PRIMARY KEY (namespace, key)
        )
        """
    )
    return conn


def hash_key(data: Any) -> str:
    """Computes deterministic SHA256 hex digest for any JSON-serializable object or string."""
    if isinstance(data, str):
        content = data
    else:
        content = json.dumps(data, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get(namespace: str, key: str) -> Optional[str]:
    """Retrieves a cached value, or returns None if not found."""
    with _get_connection() as conn:
        cursor = conn.execute(
            "SELECT value FROM kv_cache WHERE namespace = ? AND key = ?",
            (namespace, key),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def set(namespace: str, key: str, value: str) -> None:
    """Stores a value in the cache."""
    with _get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO kv_cache (namespace, key, value) VALUES (?, ?, ?)",
            (namespace, key, value),
        )
