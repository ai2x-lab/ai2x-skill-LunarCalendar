"""Fixed Gregorian date rule evaluator."""

from __future__ import annotations

from calendar_engine.models.festival import FestivalRule
from calendar_engine.rules.base import EvalContext


class SolarFixedEvaluator:
    """Matches rules based on fixed Gregorian month/day."""

    def matches(self, rule: FestivalRule, ctx: EvalContext) -> bool:
        month = int(rule.rule.payload["month"])
        day = int(rule.rule.payload["day"])
        return ctx.solar_date.month == month and ctx.solar_date.day == day

