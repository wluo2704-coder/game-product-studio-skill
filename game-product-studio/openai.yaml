#!/usr/bin/env python3
"""Validate a machine-readable Vibe-to-Build Brief without external dependencies."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


CORE_FIELDS = (
    "one_line_game_idea", "player_promise", "player_action_response",
    "repeated_decision", "observable_result", "first_playable_core",
)
ALL_FIELDS = CORE_FIELDS + ("largest_unknown",)
VALID_STATUSES = {"confirmed", "suggested", "undecided"}


def validate(brief: object, require_confirmed: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(brief, dict):
        return ["brief must be a JSON object"]
    for field in ALL_FIELDS:
        item = brief.get(field)
        if not isinstance(item, dict):
            errors.append(f"{field} must be an object with value and status")
            continue
        if not isinstance(item.get("value"), str) or not item["value"].strip():
            errors.append(f"{field}.value must be a non-empty string")
        if item.get("status") not in VALID_STATUSES:
            errors.append(f"{field}.status must be confirmed, suggested, or undecided")
        if require_confirmed and field in CORE_FIELDS and item.get("status") != "confirmed":
            errors.append(f"{field}.status must be confirmed for VIBE_GATE")
    if require_confirmed and brief.get("confirmation_state") != "CONFIRMED":
        errors.append("confirmation_state must be CONFIRMED for VIBE_GATE")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", required=True, help="UTF-8 JSON Vibe-to-Build Brief")
    parser.add_argument("--require-confirmed", action="store_true", help="require explicit user confirmation and confirmed loop fields")
    args = parser.parse_args()
    try:
        brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [f"cannot read brief: {exc}"]}, ensure_ascii=False))
        return 2
    errors = validate(brief, args.require_confirmed)
    print(json.dumps({"valid": not errors, "vibe_gate": "PASS" if not errors and args.require_confirmed else "NOT_EVALUATED", "errors": errors}, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
