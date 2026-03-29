# Taiwan Festival Calendar Engine (Runtime)

This runtime is self-contained under the skill folder to avoid conflicts with user projects.

## Path

`skills/tw_festival_calendar/runtime`

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Core Commands

```bash
twcal today --json
twcal lookup-date 2026-09-25 --json
twcal lookup-lunar --year 2026 --month 8 --day 15 --json
twcal search-festival --year 2026 --name 中秋 --mode contains --json
twcal range --start 2026-08-01 --end 2026-10-01 --json
```

## Docs

- `docs/architecture.md`
- `docs/cache-schema.md`
- `docs/festival-rules.md`
- `docs/usage-examples.md`

## Agent Schemas

- `agent/query_result.schema.json`
- `agent/festival_record.schema.json`
- `agent/ops_result.schema.json`
