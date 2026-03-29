from pathlib import Path
from subprocess import run
import os
import sys


def test_cli_lookup_date_json(tmp_path: Path):
    cmd = [
        sys.executable,
        "-m",
        "calendar_engine.cli.app",
        "--cache-dir",
        str(tmp_path / "cache"),
        "lookup-date",
        "2026-09-25",
        "--json",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    completed = run(cmd, capture_output=True, text=True, check=True, env=env)
    assert '"status": "ok"' in completed.stdout

