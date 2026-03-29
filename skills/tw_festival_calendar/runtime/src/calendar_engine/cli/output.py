"""CLI output formatting."""

from __future__ import annotations

import json
from typing import Any


def render(data: dict[str, Any], as_json: bool) -> str:
    """Render output in JSON or concise text mode."""
    if as_json:
        return json.dumps(data, ensure_ascii=False, indent=2)

    lines = [f"status: {data.get('status')}", f"action: {data.get('action')}"]
    payload = data.get("data", {})
    if isinstance(payload, dict):
        for key, value in payload.items():
            lines.append(f"{key}: {value}")
    errors = data.get("errors", [])
    if errors:
        lines.append("errors:")
        for err in errors:
            lines.append(f"- {err}")
    return "\n".join(lines)

