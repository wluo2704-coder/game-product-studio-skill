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
    parser.add_argument("--master-spec-gate", required=True)
    parser.add_argument("--spec-graph-gate", required=True)
    parser.add_argument("--slice-gate", required=True)
    parser.add_argument("--testability-gate", required=True)
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
        master_gate = load(args.master_spec_gate, "master spec gate")
        graph_gate = load(args.spec_graph_gate, "spec graph gate")
        slice_gate = load(args.slice_gate, "vertical slice gate")
        testability_gate = load(args.testability_gate, "testability gate")
        manifest = load(args.manifest, "manifest")
        qa = load(args.qa_gate, "qa gate")
        gm_access = load(args.qa_gm_access, "QA GM access report")
        reflection = load(args.reflection_gate, "reflection gate")
    except ValueError as exc:
        issues.append(str(exc))
        master_gate, graph_gate, slice_gate, testability_gate, manifest, qa, gm_access, reflection = {}, {}, {}, {}, {}, {}, {}, {}
    build_id = manifest.get("buildId")
    master_version = master_gate.get("masterSpecVersion")
    if master_gate.get("gate") != "MASTER_SPEC_GATE: PASS":
        issues.append("Master Spec gate is not PASS")
    if graph_gate.get("gate") != "SPEC_GRAPH_GATE: PASS":
        issues.append("Spec graph gate is not PASS")
    if slice_gate.get("gate") != "SLICE_GATE: PASS":
        issues.append("Vertical slice gate is not PASS")
    if testability_gate.get("gate") != "TESTABILITY_GATE: PASS":
        issues.append("Testability gate is not PASS")
    for label, record in (("spec graph", graph_gate), ("vertical slice", slice_gate), ("testability", testability_gate)):
        if record.get("masterSpecVersion") != master_version:
            issues.append(f"{label} masterSpecVersion does not match Master Spec gate")
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
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "masterSpecVersion": master_version, "manifestBuildId": build_id,
              "result": "PASS" if not issues else "FAIL", "issues": issues,
              "rule": "Master Spec, trace graph, vertical slice, testability, QA GM access, QA, and Reflection gates must pass; runtime gates bind one frozen manifest buildId."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
