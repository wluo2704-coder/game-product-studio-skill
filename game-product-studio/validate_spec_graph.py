#!/usr/bin/env python3
"""Validate a Lead-provided, candidate-bound QA GM manifest derived from testability."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SAFE_COMMANDS = {"load_scene", "set_test_state", "grant_test_resource", "reset_run"}


def load(path_text: str, label: str) -> dict:
    value = json.loads(Path(path_text).read_text(encoding="utf-8"))
    if not isinstance(value, dict): raise ValueError(f"{label} must be a JSON object")
    return value


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "REPLACE_WITH" not in value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-manifest", required=True)
    parser.add_argument("--testability-contract", required=True)
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
        contract = load(args.testability_contract, "testability contract")
        access = load(args.gm_access, "GM access manifest")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        candidate, contract, access = {}, {}, {}
        issues.append(f"cannot read input: {exc}")
    build_id = candidate.get("buildId")
    contract_scenarios = contract.get("scenarios") if isinstance(contract.get("scenarios"), list) else []
    expected_scenarios = {row.get("id") for row in contract_scenarios if isinstance(row, dict)}
    expected_scenes = {(row.get("sceneId"), row.get("entryStateId"), (row.get("reset") or {}).get("baselineId")) for row in contract_scenarios if isinstance(row, dict)}
    commands = access.get("commands") if isinstance(access.get("commands"), list) else []
    names = {row.get("name") for row in commands if isinstance(row, dict)}
    if candidate.get("status") != "FROZEN": issues.append("candidate manifest is not FROZEN")
    if not build_id: issues.append("candidate buildId is missing")
    if access.get("candidateBuildId") != build_id: issues.append("GM access buildId does not match Candidate")
    if access.get("gate") != "QA_GM_ACCESS: PASS": issues.append("GM access gate is not PASS")
    if access.get("owner") != "Lead": issues.append("GM access owner must be Lead")
    if access.get("runtimeScope") != "QA_TEST_ONLY": issues.append("GM access must be QA_TEST_ONLY")
    if access.get("deliveryDefault") != "DISABLED": issues.append("GM access must default DISABLED for delivery")
    if access.get("masterSpecVersion") != contract.get("masterSpecVersion"): issues.append("GM access masterSpecVersion does not match testability contract")
    if not {"load_scene", "reset_run"}.issubset(names): issues.append("GM allowlist needs load_scene and reset_run")
    if not names.issubset(SAFE_COMMANDS): issues.append("GM allowlist contains a non-approved command")
    if not isinstance(access.get("auditLogPath"), str) or not access["auditLogPath"].strip(): issues.append("GM auditLogPath is required")
    supplied_scenarios = set(access.get("testScenarioIds", [])) if isinstance(access.get("testScenarioIds"), list) else set()
    if supplied_scenarios != expected_scenarios or not supplied_scenarios: issues.append("GM testScenarioIds must exactly match the testability contract")
    scenes = access.get("scenes") if isinstance(access.get("scenes"), list) else []
    supplied_scenes = {(row.get("sceneId"), row.get("stateId"), row.get("baselineId")) for row in scenes if isinstance(row, dict)}
    if supplied_scenes != expected_scenes or any(not all(nonempty(value) for value in row) for row in supplied_scenes): issues.append("GM scene/state/baseline entries must exactly match the testability contract")
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "buildId": build_id,
              "masterSpecVersion": contract.get("masterSpecVersion"), "result": "PASS" if not issues else "FAIL", "issues": issues,
              "rule": "QA invokes only the Lead-provided, Candidate-bound GM allowlist derived from approved testability scenarios."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
