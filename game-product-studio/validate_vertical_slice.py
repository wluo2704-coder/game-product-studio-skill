#!/usr/bin/env python3
"""Validate a runtime testability contract and its QA-only direct-scene derivation."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


TIME_POLICIES = {"DETERMINISTIC_ADVANCE", "ENGINE_STEP_EQUIVALENT", "MANUAL_TIME_JUSTIFIED"}
REQUIRED_EVIDENCE = {"runtime_state", "visual", "console_log"}
REQUIRED_AUDIT = {"time", "buildId", "qaIdentity", "command", "parameters", "result", "evidencePath"}


def load(path_text: str, label: str) -> dict:
    value = json.loads(Path(path_text).read_text(encoding="utf-8"))
    if not isinstance(value, dict): raise ValueError(f"{label} must be a JSON object")
    return value


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "CHANGE_ME" not in value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-spec", required=True)
    parser.add_argument("--spec-graph", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output", required=True, help="new JSON report path")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    if output.exists(): print(f"ERROR: refusing to overwrite existing output: {output}"); return 2
    issues: list[str] = []
    try:
        master = load(args.master_spec, "master spec")
        graph = load(args.spec_graph, "spec graph")
        contract = load(args.contract, "testability contract")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        master, graph, contract = {}, {}, {}
        issues.append(f"cannot read input: {exc}")
    confirmed = {row.get("id") for row in master.get("requirements", []) if isinstance(row, dict) and row.get("status") == "confirmed"}
    graph_tests = {row.get("id") for row in graph.get("tests", []) if isinstance(row, dict)}
    if contract.get("schema") != "game-product-studio.runtime-testability/v1": issues.append("unexpected testability schema")
    if contract.get("masterSpecVersion") != master.get("version"): issues.append("contract masterSpecVersion does not match master spec")
    if contract.get("specGraphVersion") != graph.get("masterSpecVersion"): issues.append("contract specGraphVersion does not match spec graph")
    adapter = contract.get("adapter") if isinstance(contract.get("adapter"), dict) else {}
    if not nonempty(adapter.get("engine")): issues.append("adapter engine is required")
    if adapter.get("timePolicy") not in TIME_POLICIES: issues.append("adapter timePolicy is invalid")
    if not nonempty(adapter.get("stateSnapshotHook")): issues.append("machine-readable stateSnapshotHook is required")
    if adapter.get("timePolicy") != "MANUAL_TIME_JUSTIFIED" and not nonempty(adapter.get("advanceTimeHook")): issues.append("advanceTimeHook is required unless manual time is justified")
    scenarios = contract.get("scenarios") if isinstance(contract.get("scenarios"), list) else []
    seen: set[str] = set()
    if not scenarios: issues.append("at least one testability scenario is required")
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict): issues.append(f"scenarios[{index}] must be an object"); continue
        sid = scenario.get("id")
        if sid not in graph_tests: issues.append(f"scenarios[{index}] id must be a spec graph test ID")
        elif sid in seen: issues.append(f"duplicate scenario id: {sid}")
        else: seen.add(sid)
        reqs = scenario.get("requirementIds") if isinstance(scenario.get("requirementIds"), list) else []
        if not reqs or any(item not in confirmed for item in reqs): issues.append(f"scenarios[{index}] must trace only confirmed master requirements")
        for key in ("sceneId", "entryStateId"):
            if not nonempty(scenario.get(key)): issues.append(f"scenarios[{index}].{key} is required")
        if not isinstance(scenario.get("allowedActions"), list) or not scenario["allowedActions"]: issues.append(f"scenarios[{index}] needs allowedActions")
        if not isinstance(scenario.get("expectedAssertions"), list) or not scenario["expectedAssertions"]: issues.append(f"scenarios[{index}] needs expectedAssertions")
        reset = scenario.get("reset") if isinstance(scenario.get("reset"), dict) else {}
        if reset.get("command") != "reset_run" or not nonempty(reset.get("baselineId")): issues.append(f"scenarios[{index}] needs reset_run and baselineId")
        evidence = set(scenario.get("evidenceKinds", [])) if isinstance(scenario.get("evidenceKinds"), list) else set()
        missing = REQUIRED_EVIDENCE - evidence
        if missing: issues.append(f"scenarios[{index}] missing evidence kinds: {', '.join(sorted(missing))}")
    missing_scenarios = graph_tests - seen
    if missing_scenarios: issues.append("spec graph tests missing testability scenarios: " + ", ".join(sorted(str(x) for x in missing_scenarios)))
    direct = contract.get("directSceneCoverage") if isinstance(contract.get("directSceneCoverage"), dict) else {}
    if direct.get("inScope") is True:
        commands = set(direct.get("allowlistedCommands", [])) if isinstance(direct.get("allowlistedCommands"), list) else set()
        if not {"load_scene", "reset_run"}.issubset(commands): issues.append("direct scene coverage needs load_scene and reset_run")
        audit = set(direct.get("auditFields", [])) if isinstance(direct.get("auditFields"), list) else set()
        missing = REQUIRED_AUDIT - audit
        if missing: issues.append("direct scene coverage missing audit fields: " + ", ".join(sorted(missing)))
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "masterSpecVersion": master.get("version"),
              "gate": "TESTABILITY_GATE: PASS" if not issues else "TESTABILITY_GATE: FAIL", "issues": issues}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__": raise SystemExit(main())
