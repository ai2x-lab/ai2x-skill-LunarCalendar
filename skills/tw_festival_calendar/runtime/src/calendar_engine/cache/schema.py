"""Cache schema helpers."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

from calendar_engine.config import CACHE_SCHEMA_VERSION, ENGINE_VERSION
from calendar_engine.models.calendar_day import CalendarDayRecord


def build_year_document(
    year: int,
    records: list[CalendarDayRecord],
    timezone_name: str,
) -> dict[str, object]:
    """Create a stable cache document for one Gregorian year."""
    return {
        "schema_version": CACHE_SCHEMA_VERSION,
        "generated_at": datetime.now().astimezone().isoformat(),
        "year": year,
        "engine_version": ENGINE_VERSION,
        "source": {
            "lunar_library": "lunar_python",
            "solar_term_library": "lunar_python",
            "timezone": timezone_name,
        },
        "days": [asdict(record) for record in records],
    }

