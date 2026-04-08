# Taiwan Festival Calendar Engine (Runtime)

This runtime is self-contained under the skill folder to avoid conflicts with user projects.

## Path

`skills/tw_festival_calendar/runtime`

## Requirements
- Python 3.10+
- pip
- On Debian/Ubuntu, install `python3-venv` if virtualenv creation fails

## Install

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Preflight Check
```bash
python3 doctor.py
```

## Core Commands
```bash
twcal today --json
twcal lookup-date 2026-09-25 --json
twcal lookup-lunar --year 2026 --month 8 --day 15 --json
twcal search-festival --year 2026 --name 中秋 --mode contains --json
twcal range --start 2026-08-01 --end 2026-10-01 --json
```

## Deployment Notes
- Agent flows should always use `--json`
- Prefer isolated cron when using this skill in scheduled jobs
- Run `doctor.py` before deploying to a new machine
- Do not commit `.venv/`, `*.egg-info/`, or cache artifacts
