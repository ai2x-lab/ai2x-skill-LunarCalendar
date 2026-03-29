"""Gregorian and lunar conversion wrapper around lunar_python."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from lunar_python import Lunar, Solar


@dataclass(frozen=True)
class LunarInfo:
    """Lunar date information from converted Gregorian date."""

    lunar_year: int
    lunar_month: int
    lunar_day: int
    lunar_month_name: str
    lunar_day_name: str
    is_leap_month: bool


class CalendarConverter:
    """Conversion helper using local deterministic algorithms."""

    def solar_to_lunar(self, d: date) -> LunarInfo:
        solar = Solar.fromYmd(d.year, d.month, d.day)
        lunar = solar.getLunar()
        month = lunar.getMonth()
        return LunarInfo(
            lunar_year=lunar.getYear(),
            lunar_month=abs(month),
            lunar_day=lunar.getDay(),
            lunar_month_name=lunar.getMonthInChinese(),
            lunar_day_name=lunar.getDayInChinese(),
            is_leap_month=month < 0,
        )

    def lunar_to_solar_dates(self, year: int, month: int, day: int, leap_month: bool = False) -> list[date]:
        lunar_month = -month if leap_month else month
        lunar = Lunar.fromYmd(year, lunar_month, day)
        solar = lunar.getSolar()
        return [date(solar.getYear(), solar.getMonth(), solar.getDay())]

