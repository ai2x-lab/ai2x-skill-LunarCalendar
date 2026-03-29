"""Festival models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import FestivalType, RuleType


@dataclass(frozen=True)
class RuleSpec:
    """Concrete rule payload."""

    payload: dict[str, Any]


@dataclass(frozen=True)
class FestivalRule:
    """Declarative rule loaded from JSON."""

    id: str
    name_zh: str
    name_en: str | None
    type: FestivalType
    category: str
    rule_type: RuleType
    rule: RuleSpec
    tags: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    source: str = "base"


@dataclass(frozen=True)
class FestivalEntry:
    """Festival entry attached to a day record."""

    id: str
    name_zh: str
    name_en: str | None
    type: str
    category: str
    source_rule: str
    tags: list[str]
    notes: list[str]

