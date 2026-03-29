"""Base rule protocol."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol

from calendar_engine.models.festival import FestivalRule


@dataclass(frozen=True)
class EvalContext:
    """Runtime context for evaluating a festival rule."""

    solar_date: date
    lunar_month: int
    lunar_day: int
    is_leap_month: bool
    solar_term: str | None


class RuleEvaluator(Protocol):
    """Interface for a festival rule evaluator."""

    def matches(self, rule: FestivalRule, ctx: EvalContext) -> bool:
        """Return True when the rule applies to the date context."""

