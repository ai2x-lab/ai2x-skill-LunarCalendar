"""Fixed lunar date rule evaluator."""

from __future__ import annotations

from calendar_engine.models.festival import FestivalRule
from calendar_engine.rules.base import EvalContext


class LunarFixedEvaluator:
    """Matches rules based on lunar month/day and leap flag."""

    def matches(self, rule: FestivalRule, ctx: EvalContext) -> bool:
        month = int(rule.rule.payload["month"])
        day = int(rule.rule.payload["day"])
        leap_month = bool(rule.rule.payload.get("leap_month", False))
        return (
            ctx.lunar_month == month
            and ctx.lunar_day == day
            and ctx.is_leap_month == leap_month
        )

