#!/usr/bin/env python3
"""Validate a user-confirmed master game design specification."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ID_RE = re.compile(r"^MASTER-[A-Z][A-Z0-9_]*-\d{3}$")
STATUSES = {"confirmed", "suggested", "undecided"}


def load(path_text: str) -> dict:
    value = json.loads(Path(path_text).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("master spec must be a JSON object")
    return value


def useful(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "CHANGE_ME" not in value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-spec", required=True)
    parser.add_argument("--output", required=True, help="new JSON report path")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    if output.exists():
        print(f"ERROR: refusing to overwrite existing output: {output}")
        return 2
    issues: list[str] = []
    try:
        spec = load(args.master_spec)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        spec = {}
        issues.append(f"cannot read master spec: {exc}")
    if spec.get("schema") != "game-product-studio.master-spec/v1": issues.append("unexpected master spec schema")
    if not useful(spec.get("version")): issues.append("master spec version is required")
    if spec.get("state") != "CONFIRMED": issues.append("master spec state must be CONFIRMED")
    if spec.get("sourceBriefState") != "CONFIRMED": issues.append("source Vibe Brief must be CONFIRMED")
    if not useful(spec.get("userConfirmation")): issues.append("explicit userConfirmation is required")
    loop = spec.get("coreLoop") if isinstance(spec.get("coreLoop"), dict) else {}
    for key in ("action", "response", "decision", "result", "successFailure"):
        if not useful(loop.get(key)):
            issues.append(f"coreLoop.{key} must be non-empty and not a placeholder")
    first = spec.get("firstPlayable") if isinstance(spec.get("firstPlayable"), dict) else {}
    if not isinstance(first.get("inScope"), list) or not first["inScope"]: issues.append("firstPlayable.inScope must name at least one item")
    if not isinstance(first.get("outOfScope"), list) or not first["outOfScope"]: issues.append("firstPlayable.outOfScope must name at least one item")
    if not useful(first.get("nonNegotiable")): issues.append("firstPlayable.nonNegotiable is required")
    requirements = spec.get("requirements") if isinstance(spec.get("requirements"), list) else []
    ids: set[str] = set()
    confirmed_kinds: set[str] = set()
    if not requirements: issues.append("at least one master requirement is required")
    for index, row in enumerate(requirements):
        if not isinstance(row, dict):
            issues.append(f"requirements[{index}] must be an object")
            continue
        rid = row.get("id")
        if not isinstance(rid, str) or not ID_RE.fullmatch(rid): issues.append(f"requirements[{index}] has invalid id")
        elif rid in ids: issues.append(f"duplicate master requirement id: {rid}")
        else: ids.add(rid)
        status = row.get("status")
        if status not in STATUSES: issues.append(f"requirements[{index}] has invalid status")
        if not useful(row.get("statement")) or not useful(row.get("source")): issues.append(f"requirements[{index}] needs statement and source")
        if status == "confirmed" and isinstance(row.get("kind"), str): confirmed_kinds.add(row["kind"])
    if "core_loop" not in confirmed_kinds: issues.append("one confirmed kind=core_loop requirement is required")
    if "scope" not in confirmed_kinds: issues.append("one confirmed kind=scope requirement is required")
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "masterSpecVersion": spec.get("version"),
              "gate": "MASTER_SPEC_GATE: PASS" if not issues else "MASTER_SPEC_GATE: FAIL", "issues": issues}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
