"""Festival evaluation orchestration."""

from __future__ import annotations

from datetime import date

from calendar_engine.engine.converter import CalendarConverter
from calendar_engine.engine.solar_terms import SolarTermProvider
from calendar_engine.models.calendar_day import CalendarDayRecord
from calendar_engine.rules.base import EvalContext
from calendar_engine.rules.registry import RuleRegistry


class FestivalEvaluator:
    """Builds day records by combining conversion and rule matching."""

    def __init__(
        self,
        converter: CalendarConverter,
        solar_terms: SolarTermProvider,
        registry: RuleRegistry,
    ) -> None:
        self.converter = converter
        self.solar_terms = solar_terms
        self.registry = registry

    def build_day_record(self, d: date) -> CalendarDayRecord:
        lunar = self.converter.solar_to_lunar(d)
        term = self.solar_terms.get_term(d)
        ctx = EvalContext(
            solar_date=d,
            lunar_month=lunar.lunar_month,
            lunar_day=lunar.lunar_day,
            is_leap_month=lunar.is_leap_month,
            solar_term=term,
        )
        festivals = self.registry.evaluate(ctx)
        notes: list[str] = []
        for item in festivals:
            notes.extend(item.notes)
        return CalendarDayRecord(
            solar_date=d.isoformat(),
            weekday=d.weekday(),
            weekday_name=d.strftime("%A"),
            lunar_year=lunar.lunar_year,
            lunar_month=lunar.lunar_month,
            lunar_day=lunar.lunar_day,
            lunar_month_name=lunar.lunar_month_name,
            lunar_day_name=lunar.lunar_day_name,
            is_leap_month=lunar.is_leap_month,
            solar_term=term,
            festivals=festivals,
            notes=notes,
        )

