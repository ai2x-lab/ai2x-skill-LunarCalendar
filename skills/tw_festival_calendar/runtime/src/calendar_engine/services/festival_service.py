"""Festival-focused query helpers."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from difflib import SequenceMatcher, get_close_matches
from typing import Any


class FestivalService:
    """Search and list festivals from cache day records."""

    def __init__(self, alias_map: dict[str, list[str]] | None = None) -> None:
        self.alias_map = alias_map or {}

    def list_festivals(
        self,
        days: list[dict[str, Any]],
        month: int | None = None,
        festival_type: str | None = None,
        include_categories: list[str] | None = None,
        exclude_categories: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """List day records that contain festivals with optional filtering."""
        results: list[dict[str, Any]] = []
        for day in days:
            solar_date = str(day["solar_date"])
            if month is not None and int(solar_date[5:7]) != month:
                continue
            festivals = self._filter_festivals(
                list(day.get("festivals", [])),
                festival_type,
                include_categories,
                exclude_categories,
            )
            if festivals:
                row = dict(day)
                row["festivals"] = festivals
                results.append(row)
        return results

    def search_by_name(
        self,
        days: list[dict[str, Any]],
        keyword: str,
        mode: str = "contains",
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Search festivals by Chinese, English, or configured aliases."""
        normalized_keyword = self._normalize_text(keyword)
        if normalized_keyword == "":
            return [], []
        results: list[dict[str, Any]] = []
        suggestion_candidates: dict[str, dict[str, Any]] = {}
        for day in days:
            matched = []
            for festival in day.get("festivals", []):
                name_zh = str(festival.get("name_zh", ""))
                name_en = str(festival.get("name_en", ""))
                name_zh_n = self._normalize_text(name_zh)
                name_en_n = self._normalize_text(name_en)
                alias_keys = [
                    self._normalize_text(alias)
                    for alias in self._aliases_for_festival(festival)
                    if self._normalize_text(alias) != ""
                ]
                alias_match = any(self._is_match(normalized_keyword, alias, mode) for alias in alias_keys)
                if (
                    self._is_match(normalized_keyword, name_zh_n, mode)
                    or self._is_match(normalized_keyword, name_en_n, mode)
                    or alias_match
                ):
                    matched.append(festival)
                for alias in alias_keys:
                    suggestion_candidates[alias] = festival
            if matched:
                row = {"solar_date": day["solar_date"], "festivals": matched}
                results.append(row)
        suggestions = self._build_suggestions(normalized_keyword, suggestion_candidates)
        return results, suggestions

    def next_festival_from(self, days: list[dict[str, Any]], start: date) -> dict[str, Any] | None:
        """Return next festival day on or after the start date."""
        candidates = [d for d in days if date.fromisoformat(str(d["solar_date"])) >= start and d.get("festivals")]
        if not candidates:
            return None
        return sorted(candidates, key=lambda x: x["solar_date"])[0]

    def category_summary(self, days: list[dict[str, Any]]) -> dict[str, int]:
        """Return aggregated category counts."""
        counts: dict[str, int] = defaultdict(int)
        for day in days:
            for festival in day.get("festivals", []):
                counts[str(festival.get("category", "unknown"))] += 1
        return dict(counts)

    def _filter_festivals(
        self,
        festivals: list[dict[str, Any]],
        festival_type: str | None,
        include_categories: list[str] | None,
        exclude_categories: list[str] | None,
    ) -> list[dict[str, Any]]:
        results = festivals
        if festival_type is not None:
            results = [f for f in results if str(f.get("type")) == festival_type]
        if include_categories:
            include = set(include_categories)
            results = [f for f in results if str(f.get("category")) in include]
        if exclude_categories:
            exclude = set(exclude_categories)
            results = [f for f in results if str(f.get("category")) not in exclude]
        return results

    def _normalize_text(self, value: str) -> str:
        return value.strip().lower().replace(" ", "").replace("\u7bc0", "")

    def _is_match(self, keyword: str, candidate: str, mode: str) -> bool:
        if candidate == "":
            return False
        if mode == "exact":
            return keyword == candidate
        if mode == "contains":
            return keyword in candidate
        if mode == "fuzzy":
            if keyword in candidate:
                return True
            return SequenceMatcher(None, keyword, candidate).ratio() >= 0.72
        return keyword in candidate

    def _aliases_for_festival(self, festival: dict[str, Any]) -> list[str]:
        name_zh = str(festival.get("name_zh", ""))
        name_en = str(festival.get("name_en", ""))
        festival_id = str(festival.get("id", ""))
        aliases = [name_zh, name_en, festival_id]
        aliases.extend(self.alias_map.get(festival_id, []))
        return [a for a in aliases if a]

    def _build_suggestions(
        self,
        keyword: str,
        candidates: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if not candidates:
            return []
        keys = list(candidates.keys())
        matched = get_close_matches(keyword, keys, n=5, cutoff=0.55)
        result: list[dict[str, Any]] = []
        seen: set[str] = set()
        for k in matched:
            festival = candidates[k]
            festival_id = str(festival.get("id", ""))
            if festival_id in seen:
                continue
            seen.add(festival_id)
            score = SequenceMatcher(None, keyword, k).ratio()
            result.append(
                {
                    "id": festival.get("id"),
                    "name_zh": festival.get("name_zh"),
                    "name_en": festival.get("name_en"),
                    "score": round(score, 3),
                }
            )
        result.sort(key=lambda x: float(x["score"]), reverse=True)
        return result
