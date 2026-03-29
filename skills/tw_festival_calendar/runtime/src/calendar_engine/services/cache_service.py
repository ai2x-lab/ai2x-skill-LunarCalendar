"""Cache service orchestration."""

from __future__ import annotations

from datetime import datetime

from calendar_engine.cache.builder import CacheBuilder
from calendar_engine.cache.store import JsonYearCacheStore
from calendar_engine.cache.validator import is_valid_year_document
from calendar_engine.exceptions import CacheError


class CacheService:
    """Ensures cache availability for query operations."""

    def __init__(self, builder: CacheBuilder, store: JsonYearCacheStore) -> None:
        self.builder = builder
        self.store = store

    def ensure_years(self, years: list[int]) -> list[int]:
        """Ensure all requested years are available and valid."""
        rebuilt: list[int] = []
        for year in years:
            if not self.store.exists(year):
                self.builder.build_year(year)
                rebuilt.append(year)
                continue
            payload = self.store.load_year(year)
            if not is_valid_year_document(payload, year):
                self.builder.build_year(year)
                rebuilt.append(year)
        return rebuilt

    def initialize_two_year_cache(self, current_year: int | None = None) -> list[int]:
        """Build current year plus next year if missing or invalid."""
        year = current_year if current_year is not None else datetime.now().year
        return self.ensure_years([year, year + 1])

    def rebuild(self, years: list[int]) -> list[int]:
        """Force rebuild selected years."""
        self.builder.build_years(years)
        return years

    def check(self, years: list[int]) -> dict[int, str]:
        """Return health status per year."""
        status: dict[int, str] = {}
        for year in years:
            if not self.store.exists(year):
                status[year] = "missing"
                continue
            try:
                payload = self.store.load_year(year)
            except CacheError:
                status[year] = "invalid_json"
                continue
            status[year] = "ok" if is_valid_year_document(payload, year) else "schema_mismatch"
        return status

