"""Solar term rule evaluator."""

from __future__ import annotations

from calendar_engine.models.festival import FestivalRule
from calendar_engine.rules.base import EvalContext


class SolarTermEvaluator:
    """Matches rules when the day solar term equals the configured term."""

    def matches(self, rule: FestivalRule, ctx: EvalContext) -> bool:
        term = str(rule.rule.payload["term"])
        return ctx.solar_term == term

