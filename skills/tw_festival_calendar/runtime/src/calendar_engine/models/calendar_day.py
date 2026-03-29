"""Calendar day record model for cached data."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .festival import FestivalEntry


@dataclass(frozen=True)
class CalendarDayRecord:
    """Single Gregorian day with lunar and festival metadata."""

    solar_date: str
    weekday: int
    weekday_name: str
    lunar_year: int
    lunar_month: int
    lunar_day: int
    lunar_month_name: str
    lunar_day_name: str
    is_leap_month: bool
    solar_term: str | None
    festivals: list[FestivalEntry] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-friendly dictionary representation."""
        return asdict(self)

