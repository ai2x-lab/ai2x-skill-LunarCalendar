"""Solar term extraction using lunar_python."""

from __future__ import annotations

from datetime import date

from lunar_python import Solar


class SolarTermProvider:
    """Provides exact solar term for a Gregorian date if present."""

    def get_term(self, d: date) -> str | None:
        solar = Solar.fromYmd(d.year, d.month, d.day)
        lunar = solar.getLunar()
        term = lunar.getJieQi()
        if term == "":
            return None
        return term

