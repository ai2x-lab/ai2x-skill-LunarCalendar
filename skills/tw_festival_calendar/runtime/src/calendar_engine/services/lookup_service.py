"""Main query service for CLI and AI agent integration."""

from __future__ import annotations

from datetime import date, datetime

from lunar_python import Solar
from pathlib import Path
from typing import Any
import json

from calendar_engine.cache.builder import CacheBuilder
from calendar_engine.cache.store import JsonYearCacheStore
from calendar_engine.config import (
    CREATOR_EMAIL,
    CREATOR_NAME,
    DATA_DIR,
    DEFAULT_CACHE_DIR,
    ENGINE_VERSION,
    TIMEZONE_NAME,
)
from calendar_engine.engine.converter import CalendarConverter
from calendar_engine.engine.festival_evaluator import FestivalEvaluator
from calendar_engine.engine.solar_terms import SolarTermProvider
from calendar_engine.models.query_result import OperationResult
from calendar_engine.rules.registry import RuleRegistry
from calendar_engine.services.cache_service import CacheService
from calendar_engine.services.festival_service import FestivalService
from calendar_engine.utils.date_utils import ensure_ordered_range


class LookupService:
    """Application service for calendar and festival queries."""

    def __init__(
        self,
        cache_dir: Path,
        base_rules_path: Path,
        user_rules_path: Path,
        timezone_name: str = TIMEZONE_NAME,
    ) -> None:
        self.store = JsonYearCacheStore(cache_dir)
        self.registry = RuleRegistry(base_rules_path=base_rules_path, user_rules_path=user_rules_path)
        evaluator = FestivalEvaluator(CalendarConverter(), SolarTermProvider(), self.registry)
        self.cache_builder = CacheBuilder(evaluator, self.store, timezone_name)
        self.cache_service = CacheService(self.cache_builder, self.store)
        self.festival_service = FestivalService(alias_map=self._load_alias_map(DATA_DIR / "festival_aliases.json"))
        self.story_map = self._load_story_map(DATA_DIR / "festival_stories.json")
        self.timezone_name = timezone_name

    @classmethod
    def create_default(cls, cache_dir: Path | None = None) -> "LookupService":
        """Create service with default local paths."""
        c_dir = cache_dir or DEFAULT_CACHE_DIR
        return cls(
            cache_dir=c_dir,
            base_rules_path=DATA_DIR / "festival_rules_base.json",
            user_rules_path=DATA_DIR / "festival_rules_user.json",
        )

    def initialize(self, year: int | None = None) -> OperationResult:
        """Ensure two-year cache for skill startup."""
        rebuilt = self.cache_service.initialize_two_year_cache(current_year=year)
        target = year if year is not None else datetime.now().year
        return self._ok(
            action="initialize",
            data={"cache_years": [target, target + 1]},
            meta={"regenerated_years": rebuilt},
        )

    def lookup_date(self, d: date) -> OperationResult:
        """Lookup Gregorian date details."""
        self._ensure_years_for_date(d)
        day = self._find_day(d)
        return self._ok("lookup_date", {"record": day}, {})

    def lookup_lunar(self, year: int, month: int, day: int, leap_month: bool = False) -> OperationResult:
        """Lookup Gregorian dates from lunar date in a Gregorian year."""
        self.cache_service.ensure_years([year, year + 1])
        matched: list[str] = []
        for y in [year, year + 1]:
            days = self._load_days(y)
            for row in days:
                if (
                    int(row["lunar_month"]) == month
                    and int(row["lunar_day"]) == day
                    and bool(row["is_leap_month"]) == leap_month
                ):
                    matched.append(str(row["solar_date"]))
        return self._ok(
            "lookup_lunar",
            {
                "input": {
                    "year": year,
                    "month": month,
                    "day": day,
                    "leap_month": leap_month,
                },
                "solar_dates": sorted(set(matched)),
            },
            {},
        )

    def today(self) -> OperationResult:
        """Return today's record."""
        return self.lookup_date(datetime.now().date())

    def next_festival(self, from_date: date) -> OperationResult:
        """Return next upcoming festival."""
        years = [from_date.year, from_date.year + 1]
        self.cache_service.ensure_years(years)
        days = self._load_days(from_date.year) + self._load_days(from_date.year + 1)
        hit = self.festival_service.next_festival_from(days, from_date)
        return self._ok("next_festival", {"from": from_date.isoformat(), "record": hit}, {})

    def list_festivals(
        self,
        year: int,
        month: int | None,
        festival_type: str | None,
        include_categories: list[str] | None,
        exclude_categories: list[str] | None,
    ) -> OperationResult:
        """List festivals for selected year with filters."""
        self.cache_service.ensure_years([year])
        days = self._load_days(year)
        rows = self.festival_service.list_festivals(
            days,
            month=month,
            festival_type=festival_type,
            include_categories=include_categories,
            exclude_categories=exclude_categories,
        )
        return self._ok("list_festivals", {"year": year, "items": rows}, {})

    def search_festival(self, year: int, keyword: str, mode: str = "contains") -> OperationResult:
        """Search festival by name keyword."""
        self.cache_service.ensure_years([year])
        rows, suggestions = self.festival_service.search_by_name(self._load_days(year), keyword, mode=mode)
        return self._ok(
            "search_festival",
            {
                "year": year,
                "keyword": keyword,
                "mode": mode,
                "items": rows,
                "suggestions": suggestions if not rows else [],
            },
            {},
        )

    def range_query(self, start: date, end: date) -> OperationResult:
        """Return festival days in Gregorian date range."""
        start, end = ensure_ordered_range(start, end)
        years = list(range(start.year, end.year + 1))
        self.cache_service.ensure_years(years)
        rows: list[dict[str, Any]] = []
        for year in years:
            for day in self._load_days(year):
                d = date.fromisoformat(str(day["solar_date"]))
                if start <= d <= end and day.get("festivals"):
                    rows.append(day)
        rows.sort(key=lambda x: str(x["solar_date"]))
        return self._ok(
            "range_query",
            {"start": start.isoformat(), "end": end.isoformat(), "items": rows},
            {},
        )

    def rebuild_cache(self, years: list[int]) -> OperationResult:
        """Force rebuild cache files."""
        rebuilt = self.cache_service.rebuild(years)
        return self._ok("rebuild_cache", {"years": years}, {"regenerated_years": rebuilt})

    def check_cache(self, years: list[int]) -> OperationResult:
        """Check cache health."""
        status = self.cache_service.check(years)
        return self._ok("check_cache", {"status": status}, {})

    def add_custom_festival(self, rule_dict: dict[str, object], rebuild_years: list[int]) -> OperationResult:
        """Add custom festival and optionally rebuild cache."""
        self.registry.add_user_rule(rule_dict)
        rebuilt = self.cache_service.rebuild(rebuild_years) if rebuild_years else []
        return self._ok(
            "add_custom_festival",
            {"rule_id": rule_dict.get("id")},
            {"regenerated_years": rebuilt},
        )

    def remove_custom_festival(self, rule_id: str, rebuild_years: list[int]) -> OperationResult:
        """Remove custom festival and optionally rebuild cache."""
        removed = self.registry.remove_user_rule(rule_id)
        rebuilt = self.cache_service.rebuild(rebuild_years) if removed and rebuild_years else []
        return self._ok(
            "remove_custom_festival",
            {"rule_id": rule_id, "removed": removed},
            {"regenerated_years": rebuilt},
        )

    def lookup_story(self, festival_id: str) -> OperationResult:
        """Lookup festival story by festival id."""
        record = self.story_map.get(festival_id)
        if not record:
            return self._ok("lookup_story", {"id": festival_id, "record": None}, {"found": False})
        return self._ok("lookup_story", {"id": festival_id, "record": record}, {"found": True})

    def search_story(self, keyword: str) -> OperationResult:
        """Search festival stories by keyword/id/name."""
        kw = (keyword or "").strip().lower()
        items: list[dict[str, Any]] = []
        for rec in self.story_map.values():
            hay = " ".join(
                [
                    str(rec.get("id", "")),
                    str(rec.get("name_zh", "")),
                    str(rec.get("summary", "")),
                    " ".join(str(x) for x in rec.get("keywords", []) or []),
                ]
            ).lower()
            if kw and kw in hay:
                items.append(rec)
        items.sort(key=lambda x: str(x.get("id", "")))
        return self._ok("search_story", {"keyword": keyword, "items": items}, {"count": len(items)})

    def hour_fortune(self, target: datetime) -> OperationResult:
        """Compute hour-level fortune (時辰吉凶) for a date/datetime."""
        solar = Solar.fromDate(target)
        lunar = solar.getLunar()
        times = lunar.getTimes()

        items: list[dict[str, Any]] = []
        for t in times:
            items.append(
                {
                    "ganzhi": t.toString(),
                    "branch": t.getZhi(),
                    "time_range": f"{t.getMinHm()}-{t.getMaxHm()}",
                    "tian_shen": t.getTianShen(),
                    "tian_shen_type": t.getTianShenType(),
                    "luck": t.getTianShenLuck(),
                    "yi": t.getYi(),
                    "ji": t.getJi(),
                    "chong": t.getChongDesc(),
                    "sha": t.getSha(),
                }
            )

        now_hm = target.strftime("%H:%M")
        current = None
        for it in items:
            s, e = it["time_range"].split("-")
            if s <= now_hm <= e:
                current = it
                break

        return self._ok(
            "hour_fortune",
            {
                "date": target.strftime("%Y-%m-%d"),
                "datetime": target.isoformat(),
                "lunar": lunar.toString(),
                "day_ganzhi": lunar.getDayInGanZhi(),
                "day_yi": lunar.getDayYi(),
                "day_ji": lunar.getDayJi(),
                "current_hour": current,
                "hours": items,
            },
            {},
        )

    def _ensure_years_for_date(self, d: date) -> None:
        self.cache_service.ensure_years([d.year])

    def _find_day(self, d: date) -> dict[str, Any]:
        days = self._load_days(d.year)
        wanted = d.isoformat()
        for item in days:
            if item["solar_date"] == wanted:
                return item
        raise ValueError(f"Date not found in cache: {wanted}")

    def _load_days(self, year: int) -> list[dict[str, Any]]:
        return list(self.store.load_year(year).get("days", []))

    def _ok(self, action: str, data: dict[str, object], meta: dict[str, object]) -> OperationResult:
        full_meta = {
            "schema_version": "1.0.0",
            "timestamp": datetime.now().astimezone().isoformat(),
            "timezone": self.timezone_name,
            "engine_version": ENGINE_VERSION,
            "creator": {
                "name": CREATOR_NAME,
                "email": CREATOR_EMAIL,
            },
            **meta,
        }
        return OperationResult(status="ok", action=action, data=data, meta=full_meta)

    def _load_alias_map(self, path: Path) -> dict[str, list[str]]:
        if not path.exists():
            return {}
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        raw = payload.get("aliases", {})
        if not isinstance(raw, dict):
            return {}
        result: dict[str, list[str]] = {}
        for key, value in raw.items():
            if isinstance(value, list):
                result[str(key)] = [str(item) for item in value]
        return result

    def _load_story_map(self, path: Path) -> dict[str, dict[str, Any]]:
        if not path.exists():
            return {}
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        raw = payload.get("stories", [])
        if not isinstance(raw, list):
            return {}
        out: dict[str, dict[str, Any]] = {}
        for item in raw:
            if not isinstance(item, dict):
                continue
            sid = str(item.get("id", "")).strip()
            if not sid:
                continue
            out[sid] = {
                "id": sid,
                "name_zh": item.get("name_zh", ""),
                "summary": item.get("summary", ""),
                "keywords": item.get("keywords", []) or [],
                "source_refs": item.get("source_refs", []) or [],
                "markdown_path": item.get("markdown_path", ""),
            }
        return out


def default_rule_template(
    *,
    id_: str,
    name_zh: str,
    rule_type: str,
    rule_payload: dict[str, object],
    category: str = "custom_user",
    type_: str = "custom",
    name_en: str | None = None,
    tags: list[str] | None = None,
    notes: list[str] | None = None,
) -> dict[str, object]:
    """Build a normalized custom rule payload for CLI input."""
    return {
        "id": id_,
        "name_zh": name_zh,
        "name_en": name_en,
        "type": type_,
        "category": category,
        "rule_type": rule_type,
        "rule": rule_payload,
        "tags": tags or [],
        "notes": notes or [],
    }

