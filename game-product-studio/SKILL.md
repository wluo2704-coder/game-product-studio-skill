#!/usr/bin/env python3
"""Validate evidence that a vertical slice proves the confirmed core loop."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


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
    parser.add_argument("--slice-gate", required=True)
    parser.add_argument("--output", required=True, help="new JSON report path")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    if output.exists(): print(f"ERROR: refusing to overwrite existing output: {output}"); return 2
    issues: list[str] = []
    try:
        master = load(args.master_spec, "master spec")
        graph = load(args.spec_graph, "spec graph")
        slice_gate = load(args.slice_gate, "slice gate")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        master, graph, slice_gate = {}, {}, {}
        issues.append(f"cannot read input: {exc}")
    confirmed = {row.get("id") for row in master.get("requirements", []) if isinstance(row, dict) and row.get("status") == "confirmed"}
    tests = {row.get("id") for row in graph.get("tests", []) if isinstance(row, dict)}
    if slice_gate.get("schema") != "game-product-studio.vertical-slice/v1": issues.append("unexpected vertical slice schema")
    if slice_gate.get("masterSpecVersion") != master.get("version"): issues.append("slice masterSpecVersion does not match master spec")
    if slice_gate.get("specGraphVersion") != graph.get("masterSpecVersion"): issues.append("slice specGraphVersion does not match spec graph")
    if slice_gate.get("status") != "PASS": issues.append("slice status must be PASS")
    if slice_gate.get("decision") != "RETAIN": issues.append("slice decision must be RETAIN")
    focus = slice_gate.get("focusRequirementIds") if isinstance(slice_gate.get("focusRequirementIds"), list) else []
    if not focus or any(item not in confirmed for item in focus): issues.append("slice focus requirements must be confirmed master requirements")
    test_ids = slice_gate.get("testIds") if isinstance(slice_gate.get("testIds"), list) else []
    if not test_ids or any(item not in tests for item in test_ids): issues.append("slice test IDs must exist in spec graph")
    scenario = slice_gate.get("scenario") if isinstance(slice_gate.get("scenario"), dict) else {}
    for key in ("sceneId", "stateId", "action", "expectedResponse", "observableResult"):
        if not nonempty(scenario.get(key)): issues.append(f"slice scenario.{key} is required")
    reset = slice_gate.get("reset") if isinstance(slice_gate.get("reset"), dict) else {}
    if not nonempty(reset.get("baselineId")) or not nonempty(reset.get("evidencePath")): issues.append("slice reset baseline and evidence are required")
    evidence = slice_gate.get("evidence") if isinstance(slice_gate.get("evidence"), list) else []
    kinds = {item.get("kind") for item in evidence if isinstance(item, dict) and nonempty(item.get("path"))}
    missing = {"runtime_state", "visual", "console_log"} - kinds
    if missing: issues.append("slice evidence missing: " + ", ".join(sorted(missing)))
    if not nonempty(slice_gate.get("followUpScope")): issues.append("slice followUpScope is required")
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "masterSpecVersion": master.get("version"),
              "gate": "SLICE_GATE: PASS" if not issues else "SLICE_GATE: FAIL", "issues": issues}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__": raise SystemExit(main())
