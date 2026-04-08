#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path

checks = []

def add(name, ok, detail):
    checks.append({"name": name, "ok": ok, "detail": detail})

add('python_version', sys.version_info >= (3, 10), sys.version.split()[0])
add('python_venv_module', shutil.which('python3') is not None, shutil.which('python3') or 'python3 not found')

pyproject = Path('pyproject.toml')
add('pyproject', pyproject.exists(), str(pyproject))

try:
    out = subprocess.check_output('python3 -m pip --version', shell=True, text=True, stderr=subprocess.STDOUT, timeout=15)
    add('pip', True, out.strip())
except Exception as e:
    add('pip', False, str(e))

entry = Path('src/calendar_engine/cli/app.py')
add('twcal_entry', entry.exists(), str(entry))

print(json.dumps({
    'status': 'ok' if all(c['ok'] for c in checks) else 'degraded',
    'checks': checks,
}, ensure_ascii=False, indent=2))
