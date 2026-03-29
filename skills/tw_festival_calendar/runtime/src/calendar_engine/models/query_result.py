"""Query response models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OperationResult:
    """Standard machine-friendly operation output."""

    status: str
    action: str
    data: dict[str, Any]
    meta: dict[str, Any]
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-compatible output."""
        return {
            "status": self.status,
            "action": self.action,
            "data": self.data,
            "meta": self.meta,
            "errors": self.errors,
        }

