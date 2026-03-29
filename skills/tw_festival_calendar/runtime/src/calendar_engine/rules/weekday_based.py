"""Weekday-based rule evaluator."""

from __future__ import annotations

from calendar_engine.models.festival import FestivalRule
from calendar_engine.rules.base import EvalContext


class WeekdayBasedEvaluator:
    """Matches nth weekday in a Gregorian month."""

    def matches(self, rule: FestivalRule, ctx: EvalContext) -> bool:
        month = int(rule.rule.payload["month"])
        weekday = int(rule.rule.payload["weekday"])
        nth = int(rule.rule.payload["nth"])
        if ctx.solar_date.month != month or ctx.solar_date.weekday() != weekday:
            return False
        occurrence = (ctx.solar_date.day - 1) // 7 + 1
        return occurrence == nth

