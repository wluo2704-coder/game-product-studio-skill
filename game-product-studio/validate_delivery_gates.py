#!/usr/bin/env python3
"""Generate bounded role contracts and manual startup packets; never create Codex tasks."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROLES = {
    "lead": ("Own source, configuration, integration, Candidate and formal delivery.", "04_implementation/ and 06_candidates/"),
    "prototype_architect": ("Plan and prove the smallest core-loop vertical slice; return action-response-result, reset, visual, state, and console/log evidence.", "05_validation/vertical_slice/"),
    "product_agent_designer": ("Specify a confirmed game-internal Agent's value, trigger, override and fallback; do not choose providers or keys.", "02_design/product_agent/"),
    "design": ("Branch approved master requirements into traceable module specifications and acceptance criteria; never rewrite the master loop.", "02_design/modules/"),
    "art": ("Create a bounded asset package and integration notes.", "03_art_content/"),
    "technical": ("Define engine/platform risk and the runtime testability adapter; deliver plans, not integrated source.", "04_implementation/testability/"),
    "audio": ("Deliver a bounded audio package and implementation notes.", "03_art_content/audio/"),
    "qa": ("Verify facts and runtime evidence without changing Candidate or source.", "05_validation/QA/"),
    "reflection": ("Audit Vibe Brief fit, experience and delivery claims without changing Candidate or source.", "05_validation/Reflection/"),
    "release": ("Prepare approved release checklist and rollback notes; do not publish without authorization.", "07_delivery/release_support/"),
}
SCALES = {
    "single": ("lead", "qa", "reflection"),
    "prototype": ("lead", "prototype_architect", "qa", "reflection"),
    "agent-mvp": ("lead", "prototype_architect", "product_agent_designer", "qa", "reflection"),
    "standard": ("lead", "design", "art", "qa", "reflection"),
    "studio": ("lead", "design", "art", "technical", "audio", "qa", "reflection", "release"),
    "takeover": ("lead", "qa", "reflection"),
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--scale", choices=tuple(SCALES), required=True)
    parser.add_argument("--capability", choices=("startup-packets", "task-capable"), required=True)
    args = parser.parse_args()
    project = Path(args.project_root).expanduser().resolve()
    admin = project / "00_admin"
    if not admin.is_dir() or not (admin / "task_card.md").is_file():
        fail("--project-root must be a bootstrapped project with 00_admin/task_card.md")
    target = project / "role_startup_packets"
    target.mkdir(parents=True, exist_ok=True)
    roles = SCALES[args.scale]
    for role in roles:
        goal, output = ROLES[role]
        forbidden = "All game source/configuration/integration/Candidate/formal delivery writes" if role != "lead" else "Unapproved external publication, task creation, or account/network changes"
        qa_gm = "\n\n## QA GM runtime access\n\nWhen direct-scene testing is in scope, invoke only the Lead-provided allowlist derived from `runtime_testability_contract.json` and bound to the frozen buildId. Record command, parameters, scene/state, result, evidence path, and reset state. It grants no source/configuration/file/network/arbitrary-code access." if role == "qa" else ""
        text = f"# Role Startup Packet: {role.title()}\n\n## Role boundary\n\nThis is a development role, not a game-internal Agent feature. Only the Lead speaks with the user.\n\n## Goal\n\n{goal}\n\n## Source of truth\n\n`00_admin/task_card.md`, confirmed Vibe Brief, `01_product/master_game_design_spec.json`, current spec graph, progress recap, and assigned inputs. A child artifact cannot change master-loop or scope requirements.\n\n## Allowed output directory\n\n`{output}`\n\n## Forbidden writes\n\n{forbidden}.{qa_gm}\n\n## Acceptance checks\n\nState master requirement trace IDs, test/acceptance IDs, evidence, unresolved assumptions, and `NOT TESTED` items.\n\n## Handoff\n\nSend the artifact path, pinned master version, decisions, evidence, and recovery notes to the Lead.\n\n## Escalate when\n\nScope, master-spec version, engine, user decision, external authorization, or write boundary must change.\n\n## Recovery order\n\nTask card -> progress recap -> execution log -> master spec -> spec graph -> slice/testability -> current Candidate/evidence.\n"
        write(target / f"{role}_startup_packet.md", text)
    note = "Task creation capability may exist, but this script did not create tasks. Obtain explicit user authorization before creating a long-lived task." if args.capability == "task-capable" else "Task creation is unavailable or unauthorized. Copy the packets manually in the listed order."
    write(target / "START_HERE.md", "# Startup Order\n\n1. Lead confirms Master Spec and spec graph\n2. Prototype Architect proves the vertical slice\n3. Technical contributor defines the testability adapter when needed\n4. Selected module contributors return traceable artifacts\n5. Lead integration and frozen Candidate\n6. QA\n7. Reflection\n\n" + note + "\n")
    log = {"event": "generate_role_packets", "created_at": datetime.now(timezone.utc).isoformat(), "project": str(project), "scale": args.scale, "roles": roles, "capability": args.capability, "tasks_created": False}
    write(admin / "role_packets.log.json", json.dumps(log, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(log, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
