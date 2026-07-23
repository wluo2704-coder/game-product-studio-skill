#!/usr/bin/env python3
"""Create an engine-neutral, governed game workspace after brief confirmation."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_CORE = (
    "one_line_game_idea", "player_promise", "player_action_response",
    "repeated_decision", "observable_result", "first_playable_core",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not result:
        fail("project name must contain at least one ASCII letter or digit")
    return result


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_confirmed_vibe_brief(path: str) -> dict[str, object]:
    try:
        brief = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read Vibe Brief JSON: {exc}")
    if not isinstance(brief, dict):
        fail("--vibe-brief must contain a JSON object")
    if brief.get("confirmation_state") != "CONFIRMED":
        fail("Vibe Brief confirmation_state must be CONFIRMED")
    for key in REQUIRED_CORE:
        item = brief.get(key)
        if not isinstance(item, dict) or not isinstance(item.get("value"), str) or not item["value"].strip() or item.get("status") != "confirmed":
            fail(f"Vibe Brief requires confirmed non-empty {key}")
    return brief


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, help="Existing user-approved parent directory")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--mode", choices=("greenfield", "takeover"), required=True)
    parser.add_argument("--engine", choices=("unconfirmed", "unity", "unreal", "godot"), required=True)
    parser.add_argument("--engine-confirmed", action="store_true", help="record only after explicit user confirmation")
    parser.add_argument("--vibe-brief", required=True, help="UTF-8 JSON Vibe-to-Build Brief")
    parser.add_argument("--vibe-confirmed", action="store_true", help="assert explicit user confirmation of that brief")
    args = parser.parse_args()

    if not args.vibe_confirmed:
        fail("v0.2 bootstrap requires --vibe-confirmed")
    if args.engine_confirmed and args.engine == "unconfirmed":
        fail("--engine-confirmed requires a concrete --engine")
    brief = read_confirmed_vibe_brief(args.vibe_brief)
    root = Path(args.output_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        fail("--output-root must be an existing directory approved by the user")
    project = root / slug(args.project_name)
    if project.exists() and any(project.iterdir()):
        fail(f"refusing to overwrite nonempty project directory: {project}")

    engine_state = "CONFIRMED" if args.engine != "unconfirmed" and args.engine_confirmed else "BLOCKED"
    now = datetime.now(timezone.utc).isoformat()
    for relative in ("00_admin", "01_product", "02_design", "03_art_content", "04_implementation", "05_validation/QA", "05_validation/Reflection", "06_candidates", "07_delivery", "role_startup_packets"):
        (project / relative).mkdir(parents=True, exist_ok=True)

    write(project / "01_product/vibe_to_build_brief.json", json.dumps(brief, ensure_ascii=False, indent=2) + "\n")
    rows = "\n".join(f"| {key} | {value.get('value', '') if isinstance(value, dict) else value} | {value.get('status', 'undecided') if isinstance(value, dict) else 'undecided'} |" for key, value in brief.items() if key != "confirmation_state")
    write(project / "01_product/product_brief.md", "# Product Brief\n\nVIBE_GATE: PASS\n\n| Field | Value | Status |\n| --- | --- | --- |\n" + rows + "\n")
    write(project / "01_product/engine_decision.md", "# Engine and Presentation Decision\n\n" + f"ENGINE_DECISION: {engine_state}\n\n- Requested engine: `{args.engine}`\n- Presentation mode: undecided\n- User confirmation: record it before engine initialization.\n\nThis bootstrap created governance only; it did not create engine files.\n")
    write(project / "00_admin/task_card.md", "# Task Card\n\n" + f"- Mode: `{args.mode}`\n- VIBE_GATE: PASS\n- Engine decision: `{engine_state}`\n- Scope: confirmed brief and approved MVP only.\n- Out of scope: unapproved platforms, services, release, and engine initialization.\n- Source authority: Lead is the sole writer for game source, configuration, integration, Candidate, and formal delivery.\n")
    write(project / "00_admin/validation_protocol.md", "# Validation Protocol\n\nVerify structure, runtime evidence, and Vibe Brief fit. QA and Reflection must cite one frozen buildId.\n")
    write(project / "00_admin/execution_plan.md", "# Execution Plan\n\nConfirmed brief -> engine decision -> collaboration plan -> role packets -> Lead integration -> frozen Candidate -> QA -> Reflection -> delivery.\n")
    write(project / "00_admin/execution_log.md", f"# Execution Log\n\n- {now}: governance workspace bootstrapped; no engine project created.\n")
    write(project / "00_admin/progress_recap.md", "# Progress Recap\n\n## completed\n- Governed workspace and confirmed Vibe Brief recorded.\n\n## incomplete\n- Presentation, engine, collaboration plan, implementation, and validation gates.\n\n## last evidence\n- Bootstrap log.\n\n## next action\n- Confirm presentation and engine decision, then write collaboration_plan.md.\n")
    write(project / "00_admin/failure_memory.md", "# Failure Memory\n\n- Do not initialize an engine before explicit engine and presentation confirmation.\n- Runtime-relevant changes invalidate QA and Reflection evidence.\n")
    write(project / "00_admin/sot_and_decisions.md", "# SOT and Decisions\n\n1. User-confirmed task card\n2. Confirmed Vibe Brief and engine decision\n3. Frozen Candidate manifest and same-build evidence\n")
    log = {"event": "bootstrap", "created_at": now, "project": str(project), "mode": args.mode, "vibe_gate": "PASS", "requested_engine": args.engine, "engine_decision": engine_state, "engine_project_created": False}
    write(project / "00_admin/bootstrap.log.json", json.dumps(log, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(log, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
