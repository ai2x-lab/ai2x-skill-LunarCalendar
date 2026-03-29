"""Cache store for JSON year files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from calendar_engine.exceptions import CacheError


class JsonYearCacheStore:
    """Reads and writes one cache JSON file per year."""

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def year_path(self, year: int) -> Path:
        """Return cache file path for a year."""
        return self.cache_dir / f"{year}.json"

    def save_year(self, year: int, data: dict[str, object]) -> None:
        """Persist one cache document."""
        path = self.year_path(year)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_year(self, year: int) -> dict[str, Any]:
        """Load one cache document."""
        path = self.year_path(year)
        if not path.exists():
            raise CacheError(f"Cache file missing for year {year}")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CacheError(f"Cache file invalid for year {year}") from exc

    def exists(self, year: int) -> bool:
        """Return whether cache exists for year."""
        return self.year_path(year).exists()

