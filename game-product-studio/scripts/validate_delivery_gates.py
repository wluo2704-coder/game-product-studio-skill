#!/usr/bin/env python3
"""Validate same-build QA and Reflection gate records; return nonzero on a blocked delivery."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load(path_text: str, label: str) -> dict:
    path = Path(path_text).expanduser().resolve()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--qa-gate", required=True)
    parser.add_argument("--qa-gm-access", required=True, help="PASS report from validate_qa_gm_access.py")
    parser.add_argument("--reflection-gate", required=True)
    parser.add_argument("--output", required=True, help="JSON validation report; existing files are rejected")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    if output.exists():
        print(f"ERROR: refusing to overwrite existing output: {output}", file=sys.stderr)
        return 2
    issues: list[str] = []
    try:
        manifest = load(args.manifest, "manifest")
        qa = load(args.qa_gate, "qa gate")
        gm_access = load(args.qa_gm_access, "QA GM access report")
        reflection = load(args.reflection_gate, "reflection gate")
    except ValueError as exc:
        issues.append(str(exc))
        manifest, qa, gm_access, reflection = {}, {}, {}, {}
    build_id = manifest.get("buildId")
    if manifest.get("status") != "FROZEN":
        issues.append("manifest status is not FROZEN")
    if not build_id:
        issues.append("manifest buildId is missing")
    if qa.get("gate") != "QA_GATE: PASS":
        issues.append("QA gate is not PASS")
    if gm_access.get("result") != "PASS":
        issues.append("QA GM access gate is not PASS")
    if reflection.get("gate") != "REFLECTION_GATE: PASS":
        issues.append("Reflection gate is not PASS")
    if qa.get("buildId") != build_id:
        issues.append("QA buildId does not match manifest")
    if gm_access.get("buildId") != build_id:
        issues.append("QA GM access buildId does not match manifest")
    if reflection.get("buildId") != build_id:
        issues.append("Reflection buildId does not match manifest")
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "manifestBuildId": build_id,
              "result": "PASS" if not issues else "FAIL", "issues": issues,
              "rule": "QA GM access, QA, and Reflection PASS records must bind the same frozen manifest buildId."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
