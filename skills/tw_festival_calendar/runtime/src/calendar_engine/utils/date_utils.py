"""Date helper functions."""

from __future__ import annotations

from datetime import date


def parse_iso_date(value: str) -> date:
    """Parse YYYY-MM-DD into a date."""
    return date.fromisoformat(value)


def ensure_ordered_range(start: date, end: date) -> tuple[date, date]:
    """Ensure date range order."""
    if start <= end:
        return start, end
    return end, start

