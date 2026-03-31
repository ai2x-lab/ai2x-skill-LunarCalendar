"""Command-line entrypoint."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from calendar_engine.cli.output import render
from calendar_engine.cli.parsers import build_parser
from calendar_engine.config import DATA_DIR
from calendar_engine.services.lookup_service import LookupService, default_rule_template
from calendar_engine.utils.date_utils import parse_iso_date
from calendar_engine.utils.io_utils import read_json


def _parse_rebuild(value: str) -> list[int]:
    year = datetime.now().year
    if value == "auto":
        return [year, year + 1]
    if value == "none":
        return []
    if value.startswith("years="):
        return [int(item.strip()) for item in value.removeprefix("years=").split(",") if item.strip()]
    raise ValueError("invalid --rebuild value")


def _split_csv(value: str) -> list[str]:
    if value.strip() == "":
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    """Run CLI command dispatcher."""
    parser = build_parser()
    args = parser.parse_args()
    service = LookupService.create_default(cache_dir=Path(args.cache_dir))

    if args.command == "today":
        result = service.today()
    elif args.command == "lookup-date":
        result = service.lookup_date(parse_iso_date(args.date))
    elif args.command == "lookup-lunar":
        result = service.lookup_lunar(args.year, args.month, args.day, args.leap_month)
    elif args.command == "next-festival":
        result = service.next_festival(parse_iso_date(args.from_date))
    elif args.command == "list-festivals":
        include = list(args.include_category or [])
        exclude = list(args.exclude_category or [])
        if args.ignore_lunar_1_15:
            exclude.append("lunar_1_15")
        if args.ignore_religious:
            exclude.append("buddhist_taoist")
        result = service.list_festivals(
            year=args.year,
            month=args.month,
            festival_type=args.festival_type,
            include_categories=include,
            exclude_categories=exclude,
        )
    elif args.command == "search-festival":
        result = service.search_festival(args.year, args.name, mode=args.mode)
    elif args.command == "range":
        result = service.range_query(parse_iso_date(args.start), parse_iso_date(args.end))
    elif args.command == "rebuild-cache":
        years = [int(item.strip()) for item in args.years.split(",") if item.strip()]
        result = service.rebuild_cache(years)
    elif args.command == "check-cache":
        year = args.year or datetime.now().year
        result = service.check_cache([year, year + 1] if args.year is None else [year])
    elif args.command == "add-festival":
        rule_payload = json.loads(args.rule)
        result = service.add_custom_festival(
            default_rule_template(
                id_=args.id,
                name_zh=args.name_zh,
                name_en=args.name_en,
                type_=args.type,
                category=args.category,
                rule_type=args.rule_type,
                rule_payload=rule_payload,
                tags=_split_csv(args.tags),
                notes=_split_csv(args.notes),
            ),
            rebuild_years=_parse_rebuild(args.rebuild),
        )
    elif args.command == "remove-festival":
        result = service.remove_custom_festival(args.id, rebuild_years=_parse_rebuild(args.rebuild))
    elif args.command == "list-custom-festivals":
        data = read_json(DATA_DIR / "festival_rules_user.json") if (DATA_DIR / "festival_rules_user.json").exists() else {"rules": []}
        result = service._ok("list_custom_festivals", {"items": data.get("rules", [])}, {})
    elif args.command == "lookup-story":
        result = service.lookup_story(args.id)
    elif args.command == "search-story":
        result = service.search_story(args.keyword)
    else:
        raise ValueError("Unknown command")

    as_json = bool(getattr(args, "json", False))
    print(render(result.to_dict(), as_json))


if __name__ == "__main__":
    main()

