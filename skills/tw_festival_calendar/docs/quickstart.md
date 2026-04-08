# Skill Quickstart

## 0. Change directory

```bash
cd skills/tw_festival_calendar/runtime
```

## 1. Requirements
- Python 3.10+
- `pip`
- On Debian/Ubuntu, you may need:
  ```bash
  sudo apt install python3-venv
  ```

## 2. Recommended install

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

## 3. Run doctor first
```bash
python3 doctor.py
```

## 4. Verify cache readiness
```bash
twcal check-cache --json
```

If missing or invalid:
```bash
twcal rebuild-cache --years 2026,2027 --json
```

## 5. Run common queries
```bash
twcal today --json
twcal lookup-date 2026-09-25 --json
twcal search-festival --year 2026 --name 中秋 --mode contains --json
```
