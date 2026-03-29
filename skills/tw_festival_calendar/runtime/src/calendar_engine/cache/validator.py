"""Cache validator."""

from __future__ import annotations

from typing import Any

from calendar_engine.config import CACHE_SCHEMA_VERSION


def is_valid_year_document(payload: dict[str, Any], year: int) -> bool:
    """Validate essential fields for safe query usage."""
    return (
        payload.get("schema_version") == CACHE_SCHEMA_VERSION
        and payload.get("year") == year
        and isinstance(payload.get("days"), list)
    )

