import pytest
from pathlib import Path

from calendar_engine.services.lookup_service import LookupService


@pytest.fixture()
def service(tmp_path: Path) -> LookupService:
    return LookupService.create_default(cache_dir=tmp_path / "cache")

