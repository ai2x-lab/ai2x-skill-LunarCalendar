"""Cache generation logic."""

from __future__ import annotations

from datetime import date, timedelta

from calendar_engine.cache.schema import build_year_document
from calendar_engine.cache.store import JsonYearCacheStore
from calendar_engine.engine.festival_evaluator import FestivalEvaluator


class CacheBuilder:
    """Builds year cache files from deterministic local logic."""

    def __init__(self, evaluator: FestivalEvaluator, store: JsonYearCacheStore, timezone_name: str) -> None:
        self.evaluator = evaluator
        self.store = store
        self.timezone_name = timezone_name

    def build_year(self, year: int) -> None:
        """Generate one year cache."""
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        records = []
        cur = start
        while cur <= end:
            records.append(self.evaluator.build_day_record(cur))
            cur += timedelta(days=1)
        doc = build_year_document(year, records, self.timezone_name)
        self.store.save_year(year, doc)

    def build_years(self, years: list[int]) -> None:
        """Generate multiple years."""
        for year in years:
            self.build_year(year)

