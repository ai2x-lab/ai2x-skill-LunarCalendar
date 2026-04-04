---
name: tw-festival-calendar
description: Query Taiwan lunar/festival data locally via twcal CLI with deterministic JSON outputs.
version: 0.1.0
entrypoint: twcal
cwd: skills/tw_festival_calendar/runtime
---

# TW Festival Calendar Skill

## Purpose

Use this skill to answer Taiwan lunar calendar and traditional festival questions through local CLI commands, including hour-level fortune queries for scenarios like祭祀時段建議.

## Workspace And Runtime

Run all commands in:

`skills/tw_festival_calendar/runtime`

Recommended isolated setup:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Operating Rules

1. Always use `--json` for agent flows.
2. Prefer narrow commands (`lookup-date`, `search-festival`, `range`) to avoid large outputs.
3. For ambiguous names, use `search-festival --mode fuzzy`.
4. After rule updates, rebuild cache (`--rebuild auto` or specific years).

## Command Playbook

```bash
twcal today --json
twcal lookup-date 2026-09-25 --json
twcal lookup-lunar --year 2026 --month 8 --day 15 --json
twcal next-festival --from 2026-03-01 --json
twcal search-festival --year 2026 --name 中秋 --mode contains --json
twcal search-festival --year 2026 --name 仲秋 --mode fuzzy --json
twcal range --start 2026-08-01 --end 2026-10-01 --json
twcal list-festivals --year 2026 --ignore-lunar-1-15 --json
twcal list-festivals --year 2026 --ignore-religious --json
twcal lookup-story --id mid_autumn --json
twcal search-story --keyword 普渡 --json
twcal hour-fortune --date 2026-04-04 --json
```

## Custom Festival Lifecycle

```bash
twcal add-festival --id temple_fair --name-zh 廟會日 --rule-type lunar_fixed --rule '{"month":3,"day":23,"leap_month":false}' --rebuild auto --json
twcal remove-festival --id temple_fair --rebuild auto --json
```

## Maintenance Files

- `src/calendar_engine/data/festival_rules_base.json`
- `src/calendar_engine/data/festival_rules_user.json`
- `src/calendar_engine/data/festival_aliases.json`
- `src/calendar_engine/data/festival_stories.json`
- `src/calendar_engine/data/stories/*.md`

## Output Contract

Every operation returns:

- `status`
- `action`
- `data`
- `meta`
- `errors`

Schemas: `runtime/agent/*.schema.json`
