#!/usr/bin/env python3
"""Dependency-free structural validation for this Game Product Studio package."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = (
    "SKILL.md", "agents/openai.yaml", "references/vibe-to-build-discovery.md",
    "references/intent-classification.md", "references/collaboration-modes.md",
    "references/collaboration-and-gates.md", "assets/project-templates/vibe_to_build_brief.md",
    "references/master-design-and-spec-graph.md", "references/vertical-slice-and-testability.md",
    "assets/project-templates/master_game_design_spec.md", "assets/project-templates/master_game_design_spec.json",
    "assets/project-templates/module_design_spec.md", "assets/project-templates/spec_graph.json",
    "assets/project-templates/vertical_slice_gate.json", "assets/project-templates/runtime_testability_contract.json",
    "assets/project-templates/product_agent_spec.md", "assets/project-templates/collaboration_plan.md",
    "scripts/validate_vibe_brief.py", "scripts/bootstrap_project.py",
    "scripts/generate_role_packets.py", "scripts/generate_build_identity.py",
    "scripts/validate_master_spec.py", "scripts/validate_spec_graph.py", "scripts/validate_vertical_slice.py",
    "scripts/validate_runtime_testability.py", "scripts/validate_delivery_gates.py", "scripts/validate_qa_gm_access.py", "scripts/quick_validate.py",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    root = args.package.resolve()
    errors = [f"missing: {path}" for path in REQUIRED if not (root / path).is_file()]
    skill = root / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        if not re.match(r"\A---\r?\nname: game-product-studio\r?\ndescription: .+\r?\n---", text):
            errors.append("SKILL.md must begin with name and non-empty description frontmatter")
        for marker in ("VIBE_GATE", "MASTER_SPEC_GATE", "SPEC_GRAPH_GATE", "SLICE_GATE", "TESTABILITY_GATE", "game-internal Agent", "Discovery Lead", "QA", "Reflection"):
            if marker not in text:
                errors.append(f"SKILL.md missing required operating marker: {marker}")
    result = "PASS" if not errors else "FAIL"
    print(f"PACKAGE_STRUCTURE_VALIDATION={result}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
