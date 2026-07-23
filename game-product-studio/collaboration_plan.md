---
name: game-product-studio
description: Turn a vague game idea into a user-confirmed master game design specification, a traceable module-spec tree, a tested core-loop vertical slice, and a governed multi-agent game MVP workspace. Use when a user wants to vibe-code a game, compile game ideas into design documents, add a game-internal Agent feature, choose a browser/desktop/mobile presentation and engine, organize Codex roles, or add Candidate, QA, Reflection, and recovery gates to an existing game project.
---

# Game Product Studio

Turn a personal game idea into a confirmed, testable first playable. Keep the experience focused on a personal playable product; do not silently expand it into commercial launch or live operations.

## Operating boundaries

- Keep game direction, scope, presentation, engine, model provider, key use, release authority, and public publishing with the user.
- Do not initialize an engine project until `VIBE_GATE: PASS`, `MASTER_SPEC_GATE: PASS`, and `ENGINE_DECISION: CONFIRMED` are recorded.
- Do not create a long-lived task, install globally, install dependencies, create a key, publish, change accounts/networking, or write outside the approved root without explicit authorization.
- Treat a **game-internal Agent** as a product feature, not as a development collaborator. It may not replace a player-confirmed core loop.
- The integration Lead is the only writer of game source, configuration, Candidate, and formal delivery. QA and Reflection are read-only.
- A module spec, test plan, slice, or QA finding cannot alter the confirmed master loop or MVP scope. Propose a versioned master-spec decision to the user instead.
- Do not treat a slice as ready for broad implementation until `SLICE_GATE: PASS` and `TESTABILITY_GATE: PASS` are both recorded.
- For direct-scene testing, the Lead provides a candidate-bound, QA-only GM allowlist. QA may invoke it only at runtime; it never grants source, configuration, file, network, or arbitrary-code access.
- Treat `NOT TESTED` as unverified. QA and Reflection PASS must name the same frozen buildId; runtime-relevant changes invalidate both.

## 1. Discover with one user-facing voice

Read [vibe-to-build-discovery.md](references/vibe-to-build-discovery.md) and [intent-classification.md](references/intent-classification.md).

Use one **Discovery Lead** as the only user-facing voice. Start with one plain-language question, never a form. Classify every answer before choosing the next question:

- `core_loop_evidence`: repeated player action, game response, choice, or observable result.
- `core_loop_modifier`: changes a repeated choice or feedback.
- `candidate_feature`: requested but not yet placed in the loop.
- `auxiliary_feature`, `reference_or_flavor`, or `delivery_choice`.

Do not treat a reference or requested feature as a confirmed loop. Fill the smallest missing link in: player acts -> game responds -> player chooses -> player sees a result. Use at most 15 user-visible questions; normally summarize after 5–8. If the user does not understand a question, explain concretely without a question mark, then retry once; a retry still counts.

Write `vibe_to_build_brief.md` from the bundled template. Label all content `confirmed`, `suggested`, or `undecided`. Present the complete brief and obtain explicit confirmation before advancing. Run `scripts/validate_vibe_brief.py --brief <json> --require-confirmed` when a machine-readable brief is available. If not confirmed, keep `VIBE_GATE: BLOCKED`.

If the game includes an Agent feature, first place it in the confirmed loop. Only then read [product-agent-spec.md](references/product-agent-spec.md) and create `product_agent_spec.md`. Do not choose a model, backend, key, or chat scope until its player value, trigger, player override, and fallback are confirmed.

## 2. Compile and confirm the master design tree

Read [master-design-and-spec-graph.md](references/master-design-and-spec-graph.md). Compile the confirmed brief into both a human-readable `master_game_design_spec.md` and machine-readable `master_game_design_spec.json`, using the bundled templates.

The master spec is the sole design source of truth. Include a versioned core loop, player promise, first-playable scope, success/failure states, scene flow, explicit assumptions, deferred decisions, requirement IDs, and user confirmation. Preserve the distinction between `confirmed`, `suggested`, and `undecided`; never present an inference as user-confirmed.

Present the complete master-spec summary to the user and request one explicit confirmation. Do not reopen the interview unless a missing fact blocks the first playable; ask at most one plain-language blocking question at a time. Run `scripts/validate_master_spec.py --master-spec <json> --output <new-report.json>`. Advance only on `MASTER_SPEC_GATE: PASS`.

Then branch only the modules needed for this MVP, such as combat, systems, balance, content, UI/scene flow, game-internal Agent, art/audio, or technical/testability. Each module requirement must trace to a master requirement and map to an acceptance/test ID in `spec_graph.json`. Use the module and graph templates, then run `scripts/validate_spec_graph.py --master-spec <json> --spec-graph <json> --output <new-report.json>`. `SPEC_GRAPH_GATE: PASS` is required before independent module work.

When a master decision changes, increment its version, record the decision, identify affected modules/tests, and invalidate their downstream evidence. Do not patch child specs silently.

## 3. Decide implementation after the design is confirmed

Read [implementation-decisions.md](references/implementation-decisions.md) and [engine-selection.md](references/engine-selection.md).

First confirm presentation: browser-local, native desktop, mobile, cloud-streamed, console, XR, or editor-only. Then compare engines against the confirmed master spec and current official documentation when version-dependent facts matter. Record recommendation, tradeoffs, minimum spike, unknowns, and user confirmation in `engine_decision.md`.

Without a concrete, user-confirmed engine and presentation, record `ENGINE_DECISION: BLOCKED` and do not generate engine files. For model-backed features, request separate authority before any credential or backend action.

## 4. Prove the loop through a slice and a testability contract

Read [vertical-slice-and-testability.md](references/vertical-slice-and-testability.md) before implementation.

Build the smallest runnable vertical slice for the master core loop. Work in short cycles: make one bounded change -> run -> observe -> adjust. For each tested scenario, record entry scene/state, action, expected response, observable result, reset baseline, and evidence. Include a runtime-state snapshot, a visual observation, and console/log evidence. Reset before each independent scenario and record a retain/revise/stop decision.

Write `vertical_slice_gate.json` and run `scripts/validate_vertical_slice.py --master-spec <json> --spec-graph <json> --slice-gate <json> --output <new-report.json>`. Only `SLICE_GATE: PASS` with `decision: RETAIN` opens broad module implementation.

Write `runtime_testability_contract.json` from the bundled template and run `scripts/validate_runtime_testability.py --master-spec <json> --spec-graph <json> --contract <json> --output <new-report.json>`. It must map every in-scope test to stable scene/state IDs, allowed actions, observable state, reset baseline, timing policy, and evidence. For browser projects, expose `window.advanceTime(ms)` and `window.render_game_to_text()` when feasible; for other engines provide documented equivalent hooks. This is a test interface, not a player-facing cheat system.

Test controls and causal interactions, not only page load. Verify each critical action changes the intended state/result, inspect screenshots or video visually, inspect state/console output, and rerun affected scenarios after each runtime-relevant change.

## 5. Select the smallest useful collaboration mode

Read [collaboration-modes.md](references/collaboration-modes.md), [role-selection-rules.md](references/role-selection-rules.md), and [delivery-contracts.md](references/delivery-contracts.md).

Write `collaboration_plan.md` before role packets. Use only independently testable roles with stable handoffs:

- **Discovery cell**: Discovery Lead only; optional short-lived Loop Analyst or Feature Critic writes read-only notes and never asks the user.
- **Prototype mode**: Lead plus bounded Prototype Architect input for the vertical slice, then QA and Reflection.
- **Agent-MVP mode**: add Product-Agent Designer only when a confirmed in-game Agent changes the loop.
- **Standard / Studio / Takeover**: add design, art, technical, audio, release, or audit roles only for demonstrated complexity.

Long-lived roles need explicit user authorization and available task creation. Otherwise generate manual startup packets. Lead remains sole integrator.

For QA that must reach a scene directly, read [qa-gm-access-contract.md](references/qa-gm-access-contract.md). Derive the Lead-owned `qa_gm_access_manifest.json` from the approved runtime testability contract only after Candidate freeze. QA validates it with `scripts/validate_qa_gm_access.py`. The GM surface must be test-only, candidate-bound, logged, resettable, and disabled by default for delivery.

Do not introduce a separate “GM” or “product owner” role. Before direct-scene QA starts, it must receive the frozen Candidate buildId, GM manifest, in-scope scene/fixture list, and reset baseline. QA may only invoke listed commands and return command/scene/reset evidence; it cannot alter acceptance criteria, gameplay values, source, assets, configuration, saves, or Candidate files.

## 6. Bootstrap, freeze, validate, recover

After Brief, Master Spec, engine, collaboration plan, and output root are confirmed, use the bundled scripts:

```powershell
& python scripts/bootstrap_project.py --output-root 'D:\GameWork' --project-name 'Sky Hop' --mode greenfield --engine godot --engine-confirmed --vibe-brief 'D:\brief.json' --vibe-confirmed --master-spec 'D:\master_game_design_spec.json' --master-confirmed
& python scripts/generate_role_packets.py --project-root 'D:\GameWork\sky-hop' --scale prototype --capability startup-packets
```

`bootstrap_project.py` rejects nonempty targets and creates governance only, not an engine project. `generate_role_packets.py` creates contracts but never tasks. `generate_build_identity.py` freezes Candidate identity. `validate_delivery_gates.py` enforces the design, slice, testability, QA GM, QA, and Reflection gates.

For a package metadata check, run `scripts/quick_validate.py <skill-folder>`. It requires PyYAML; use an already-approved isolated environment and do not install it globally or add dependencies without explicit user authorization. `scripts/validate_package_structure.py` is the no-dependency fallback for local structural checks.

For recovery read task card -> progress recap -> execution log -> confirmed brief/master spec/decisions -> graph/slice/testability -> Candidate/evidence. Read [recovery-and-invalidation.md](references/recovery-and-invalidation.md) when a decision or runtime artifact changes.
