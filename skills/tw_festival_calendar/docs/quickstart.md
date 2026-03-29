# Skill Quickstart

## 0. Change directory

```bash
cd skills/tw_festival_calendar/runtime
```

## 1. Install in isolated environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## 2. Verify cache readiness

```bash
twcal check-cache --json
```

If missing or invalid:

```bash
twcal rebuild-cache --years 2026,2027 --json
```

## 3. Run common queries

```bash
twcal today --json
twcal lookup-date 2026-09-25 --json
twcal search-festival --year 2026 --name 中秋 --mode contains --json
```

## 4. Ambiguous name strategy

1. `--mode contains`
2. `--mode fuzzy`
3. Add alias in `src/calendar_engine/data/festival_aliases.json`
