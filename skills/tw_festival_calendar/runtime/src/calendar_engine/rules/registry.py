"""Rule loader and evaluator registry."""

from __future__ import annotations

import json
from pathlib import Path

from calendar_engine.exceptions import RuleError
from calendar_engine.models.enums import FestivalType, RuleType
from calendar_engine.models.festival import FestivalEntry, FestivalRule, RuleSpec
from calendar_engine.rules.base import EvalContext, RuleEvaluator
from calendar_engine.rules.lunar_fixed import LunarFixedEvaluator
from calendar_engine.rules.solar_fixed import SolarFixedEvaluator
from calendar_engine.rules.solar_term import SolarTermEvaluator
from calendar_engine.rules.weekday_based import WeekdayBasedEvaluator


class RuleRegistry:
    """Loads festival rules and evaluates them against date contexts."""

    def __init__(self, base_rules_path: Path, user_rules_path: Path | None = None) -> None:
        self.base_rules_path = base_rules_path
        self.user_rules_path = user_rules_path
        self._evaluators: dict[RuleType, RuleEvaluator] = {
            RuleType.LUNAR_FIXED: LunarFixedEvaluator(),
            RuleType.SOLAR_FIXED: SolarFixedEvaluator(),
            RuleType.SOLAR_TERM: SolarTermEvaluator(),
            RuleType.WEEKDAY_BASED: WeekdayBasedEvaluator(),
        }
        self._rules = self._load_rules()

    @property
    def rules(self) -> list[FestivalRule]:
        """Return loaded rules."""
        return list(self._rules)

    def evaluate(self, ctx: EvalContext) -> list[FestivalEntry]:
        """Evaluate all rules and return matching festival entries."""
        matches: list[FestivalEntry] = []
        for rule in self._rules:
            evaluator = self._evaluators[rule.rule_type]
            if evaluator.matches(rule, ctx):
                matches.append(
                    FestivalEntry(
                        id=rule.id,
                        name_zh=rule.name_zh,
                        name_en=rule.name_en,
                        type=rule.type.value,
                        category=rule.category,
                        source_rule=rule.rule_type.value,
                        tags=rule.tags,
                        notes=rule.notes,
                    )
                )
        return matches

    def add_user_rule(self, rule_dict: dict[str, object]) -> None:
        """Persist a custom rule and reload registry."""
        if self.user_rules_path is None:
            raise RuleError("User rules path is not configured")
        payload = {"schema_version": "1.0.0", "rules": []}
        if self.user_rules_path.exists():
            payload = json.loads(self.user_rules_path.read_text(encoding="utf-8"))
        rules = payload.setdefault("rules", [])
        assert isinstance(rules, list)
        rules.append(rule_dict)
        self.user_rules_path.parent.mkdir(parents=True, exist_ok=True)
        self.user_rules_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._rules = self._load_rules()

    def remove_user_rule(self, rule_id: str) -> bool:
        """Remove a custom rule by id and reload registry."""
        if self.user_rules_path is None or not self.user_rules_path.exists():
            return False
        payload = json.loads(self.user_rules_path.read_text(encoding="utf-8"))
        rules = payload.get("rules", [])
        if not isinstance(rules, list):
            raise RuleError("user rules file has invalid format")
        filtered = [r for r in rules if r.get("id") != rule_id]
        if len(filtered) == len(rules):
            return False
        payload["rules"] = filtered
        self.user_rules_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._rules = self._load_rules()
        return True

    def _load_rules(self) -> list[FestivalRule]:
        rule_objects: dict[str, FestivalRule] = {}
        for path, source in self._iter_rule_sources():
            payload = self._read_json(path)
            entries = payload.get("rules", [])
            if not isinstance(entries, list):
                raise RuleError(f"Invalid rules format in {path}")
            for entry in entries:
                parsed = self._parse_rule(entry, source)
                rule_objects[parsed.id] = parsed
        return list(rule_objects.values())

    def _iter_rule_sources(self) -> list[tuple[Path, str]]:
        sources = [(self.base_rules_path, "base")]
        if self.user_rules_path is not None:
            sources.append((self.user_rules_path, "user"))
        return [pair for pair in sources if pair[0].exists()]

    def _read_json(self, path: Path) -> dict[str, object]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RuleError(f"Invalid JSON in {path}") from exc

    def _parse_rule(self, data: object, source: str) -> FestivalRule:
        if not isinstance(data, dict):
            raise RuleError("Rule entry must be an object")
        try:
            return FestivalRule(
                id=str(data["id"]),
                name_zh=str(data["name_zh"]),
                name_en=str(data["name_en"]) if data.get("name_en") is not None else None,
                type=FestivalType(str(data["type"])),
                category=str(data["category"]),
                rule_type=RuleType(str(data["rule_type"])),
                rule=RuleSpec(payload=dict(data["rule"])),
                tags=[str(tag) for tag in data.get("tags", [])],
                notes=[str(note) for note in data.get("notes", [])],
                source=source,
            )
        except KeyError as exc:
            raise RuleError(f"Missing field {exc.args[0]} in rule") from exc

