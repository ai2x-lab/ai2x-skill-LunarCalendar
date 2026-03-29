"""Project-level configuration constants."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_ROOT / "data"
DEFAULT_CACHE_DIR = Path.cwd() / "cache"
CACHE_SCHEMA_VERSION = "1.0.0"
ENGINE_VERSION = "0.1.0"
TIMEZONE_NAME = "Asia/Taipei"
CREATOR_NAME = "Weichien"
CREATOR_EMAIL = "Weichien68@gmail.com"

