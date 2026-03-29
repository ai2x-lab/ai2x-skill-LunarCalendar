"""Enumerations used by the engine."""

from __future__ import annotations

from enum import Enum


class FestivalType(str, Enum):
    TRADITIONAL = "traditional"
    SEASONAL = "seasonal"
    RELIGIOUS = "religious"
    CUSTOM = "custom"


class RuleType(str, Enum):
    LUNAR_FIXED = "lunar_fixed"
    SOLAR_FIXED = "solar_fixed"
    SOLAR_TERM = "solar_term"
    WEEKDAY_BASED = "weekday_based"

