"""CLI argument parser."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build command parser for twcal."""
    parser = argparse.ArgumentParser(prog="twcal")
    parser.add_argument("--cache-dir", default="cache", help="Cache directory path")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("today").add_argument("--json", action="store_true")

    lookup_date = sub.add_parser("lookup-date")
    lookup_date.add_argument("date")
    lookup_date.add_argument("--json", action="store_true")

    lookup_lunar = sub.add_parser("lookup-lunar")
    lookup_lunar.add_argument("--year", type=int, required=True)
    lookup_lunar.add_argument("--month", type=int, required=True)
    lookup_lunar.add_argument("--day", type=int, required=True)
    lookup_lunar.add_argument("--leap-month", action="store_true")
    lookup_lunar.add_argument("--json", action="store_true")

    next_festival = sub.add_parser("next-festival")
    next_festival.add_argument("--from", dest="from_date", required=True)
    next_festival.add_argument("--json", action="store_true")

    list_festivals = sub.add_parser("list-festivals")
    list_festivals.add_argument("--year", type=int, required=True)
    list_festivals.add_argument("--month", type=int)
    list_festivals.add_argument("--type", dest="festival_type")
    list_festivals.add_argument("--include-category", action="append")
    list_festivals.add_argument("--exclude-category", action="append")
    list_festivals.add_argument("--ignore-lunar-1-15", action="store_true")
    list_festivals.add_argument("--ignore-religious", action="store_true")
    list_festivals.add_argument("--json", action="store_true")

    search_festival = sub.add_parser("search-festival")
    search_festival.add_argument("--year", type=int, required=True)
    search_festival.add_argument("--name", required=True)
    search_festival.add_argument(
        "--mode",
        choices=["exact", "contains", "fuzzy"],
        default="contains",
        help="Search mode for festival names",
    )
    search_festival.add_argument("--json", action="store_true")

    range_cmd = sub.add_parser("range")
    range_cmd.add_argument("--start", required=True)
    range_cmd.add_argument("--end", required=True)
    range_cmd.add_argument("--json", action="store_true")

    rebuild = sub.add_parser("rebuild-cache")
    rebuild.add_argument("--years", required=True, help="Comma-separated years, e.g. 2026,2027")
    rebuild.add_argument("--json", action="store_true")

    check = sub.add_parser("check-cache")
    check.add_argument("--year", type=int)
    check.add_argument("--json", action="store_true")

    add_festival = sub.add_parser("add-festival")
    add_festival.add_argument("--id", required=True)
    add_festival.add_argument("--name-zh", required=True)
    add_festival.add_argument("--name-en")
    add_festival.add_argument("--type", default="custom")
    add_festival.add_argument("--category", default="custom_user")
    add_festival.add_argument("--rule-type", required=True)
    add_festival.add_argument("--rule", required=True, help='JSON object string e.g. {"month":8,"day":15}')
    add_festival.add_argument("--tags", default="")
    add_festival.add_argument("--notes", default="")
    add_festival.add_argument("--rebuild", default="auto", help="auto|none|years=2026,2027")
    add_festival.add_argument("--json", action="store_true")

    remove = sub.add_parser("remove-festival")
    remove.add_argument("--id", required=True)
    remove.add_argument("--rebuild", default="auto", help="auto|none|years=2026,2027")
    remove.add_argument("--json", action="store_true")

    sub.add_parser("list-custom-festivals").add_argument("--json", action="store_true")

    return parser

