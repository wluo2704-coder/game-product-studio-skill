#!/usr/bin/env python3
"""Validate a Lead-provided, candidate-bound QA GM access manifest."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load(path_text: str, label: str) -> dict:
    try:
        value = json.loads(Path(path_text).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-manifest", required=True)
    parser.add_argument("--gm-access", required=True)
    parser.add_argument("--output", required=True, help="new JSON report path")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    if output.exists():
        print(f"ERROR: refusing to overwrite existing output: {output}")
        return 2
    issues: list[str] = []
    try:
        candidate = load(args.candidate_manifest, "candidate manifest")
        access = load(args.gm_access, "GM access manifest")
    except ValueError as exc:
        candidate, access = {}, {}
        issues.append(str(exc))
    build_id = candidate.get("buildId")
    command_rows = access.get("commands") if isinstance(access.get("commands"), list) else []
    names = {row.get("name") for row in command_rows if isinstance(row, dict)}
    forbidden = {name for name in names if any(term in str(name).lower() for term in ("shell", "exec", "script", "file", "network", "config"))}
    if candidate.get("status") != "FROZEN": issues.append("candidate manifest is not FROZEN")
    if not build_id: issues.append("candidate buildId is missing")
    if access.get("candidateBuildId") != build_id: issues.append("GM access buildId does not match Candidate")
    if access.get("gate") != "QA_GM_ACCESS: PASS": issues.append("GM access gate is not PASS")
    if access.get("owner") != "Lead": issues.append("GM access owner must be Lead")
    if access.get("runtimeScope") != "QA_TEST_ONLY": issues.append("GM access must be QA_TEST_ONLY")
    if access.get("deliveryDefault") != "DISABLED": issues.append("GM access must default DISABLED for delivery")
    if not {"load_scene", "reset_run"}.issubset(names): issues.append("GM allowlist needs load_scene and reset_run")
    if forbidden: issues.append("GM allowlist contains forbidden capability names: " + ", ".join(sorted(forbidden)))
    if not isinstance(access.get("auditLogPath"), str) or not access["auditLogPath"].strip(): issues.append("GM auditLogPath is required")
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "buildId": build_id, "result": "PASS" if not issues else "FAIL", "issues": issues, "rule": "QA invokes only the Lead-provided, candidate-bound GM allowlist."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
