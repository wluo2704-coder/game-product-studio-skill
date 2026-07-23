#!/usr/bin/env python3
"""Validate that module requirements and tests trace to one confirmed master spec."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


MODULE_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


def load(path_text: str, label: str) -> dict:
    value = json.loads(Path(path_text).read_text(encoding="utf-8"))
    if not isinstance(value, dict): raise ValueError(f"{label} must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-spec", required=True)
    parser.add_argument("--spec-graph", required=True)
    parser.add_argument("--output", required=True, help="new JSON report path")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    if output.exists(): print(f"ERROR: refusing to overwrite existing output: {output}"); return 2
    issues: list[str] = []
    try:
        master = load(args.master_spec, "master spec")
        graph = load(args.spec_graph, "spec graph")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        master, graph = {}, {}
        issues.append(f"cannot read input: {exc}")
    confirmed = {row.get("id") for row in master.get("requirements", []) if isinstance(row, dict) and row.get("status") == "confirmed"}
    if master.get("state") != "CONFIRMED": issues.append("master spec is not CONFIRMED")
    if graph.get("schema") != "game-product-studio.spec-graph/v1": issues.append("unexpected spec graph schema")
    if graph.get("masterSpecVersion") != master.get("version"): issues.append("spec graph masterSpecVersion does not match master spec")
    tests = graph.get("tests") if isinstance(graph.get("tests"), list) else []
    test_ids = {row.get("id") for row in tests if isinstance(row, dict) and isinstance(row.get("id"), str)}
    if not tests or len(test_ids) != len(tests): issues.append("tests require unique string IDs")
    modules = graph.get("modules") if isinstance(graph.get("modules"), list) else []
    if not modules: issues.append("at least one module is required")
    module_ids: set[str] = set()
    requirement_ids: set[str] = set()
    for index, module in enumerate(modules):
        if not isinstance(module, dict): issues.append(f"modules[{index}] must be an object"); continue
        mid = module.get("id")
        if not isinstance(mid, str) or not MODULE_RE.fullmatch(mid): issues.append(f"modules[{index}] has invalid id")
        elif mid in module_ids: issues.append(f"duplicate module id: {mid}")
        else: module_ids.add(mid)
        if not isinstance(module.get("path"), str) or not module["path"].strip(): issues.append(f"modules[{index}] needs path")
        rows = module.get("requirements") if isinstance(module.get("requirements"), list) else []
        if not rows: issues.append(f"modules[{index}] needs at least one requirement")
        for rindex, row in enumerate(rows):
            if not isinstance(row, dict): issues.append(f"modules[{index}].requirements[{rindex}] must be an object"); continue
            rid = row.get("id")
            if not isinstance(rid, str) or not rid.strip(): issues.append(f"modules[{index}].requirements[{rindex}] needs id")
            elif rid in requirement_ids: issues.append(f"duplicate module requirement id: {rid}")
            else: requirement_ids.add(rid)
            trace = row.get("tracesTo") if isinstance(row.get("tracesTo"), list) else []
            if not trace or any(item not in confirmed for item in trace): issues.append(f"modules[{index}].requirements[{rindex}] must trace only confirmed master requirements")
            acceptance = row.get("acceptanceIds") if isinstance(row.get("acceptanceIds"), list) else []
            if not acceptance or any(item not in test_ids for item in acceptance): issues.append(f"modules[{index}].requirements[{rindex}] has missing test mapping")
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "masterSpecVersion": master.get("version"),
              "gate": "SPEC_GRAPH_GATE: PASS" if not issues else "SPEC_GRAPH_GATE: FAIL", "issues": issues}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__": raise SystemExit(main())
