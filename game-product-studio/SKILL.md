---
name: game-product-studio
description: Turn a vague game idea into a user-confirmed Vibe-to-Build Brief, then create and govern a recoverable multi-agent game MVP workspace. Use when a user wants to vibe-code a game, add a game-internal Agent feature, choose a browser/desktop/mobile presentation and engine, organize Codex roles, or add Candidate, QA, Reflection, and recovery gates to an existing game project.
---

# Game Product Studio

Turn a personal game idea into a confirmed first-playable hypothesis and a governed delivery workspace. Do not promise a commercial-quality game in one call.

## Operating boundaries

- Keep core game direction, presentation, engine, scope, model provider, key use, and release authority with the user.
- Do not initialize an engine project until `VIBE_GATE: PASS` and `ENGINE_DECISION: CONFIRMED` are both recorded.
- Do not create a long-lived task, install globally, install dependencies, create a key, publish, change accounts/networking, or write outside the approved root without explicit authorization.
- Treat a **game-internal Agent** as a product feature, not as a development collaborator. Treat Codex collaborators as development roles, not as in-game features.
- The integration Lead is the only writer of game source, configuration, Candidate, and formal delivery. QA and Reflection are read-only.
- For direct-scene testing, the Lead provides a candidate-bound, QA-only GM allowlist. QA may invoke it only at runtime; it never grants source, configuration, file, network, or arbitrary-code access.
- Treat `NOT TESTED` as unverified. QA and Reflection PASS must name the same frozen buildId; runtime-relevant changes invalidate both.

## 1. Discover the game with one user-facing voice

Read [vibe-to-build-discovery.md](references/vibe-to-build-discovery.md) and [intent-classification.md](references/intent-classification.md).

Use one **Discovery Lead** as the only user-facing voice. Start with one plain-language question, never a form. Classify every answer before choosing the next question:

- `core_loop_evidence`: repeated player action, game response, choice, or observable result.
- `core_loop_modifier`: changes a repeated choice or feedback.
- `candidate_feature`: requested but not yet placed in the loop.
- `auxiliary_feature`, `reference_or_flavor`, or `delivery_choice`.

Do not treat a reference or requested feature as a confirmed loop. Prefer filling the smallest missing link in: player repeats an action → game responds → player chooses → player sees a result. Use at most 15 user-visible questions; normally summarize after 5–8. If the user does not understand a question, explain concretely without a question mark, then retry once; a retry still counts.

Write `vibe_to_build_brief.md` from the bundled template. It must label all content `confirmed`, `suggested`, or `undecided`. Before advancing, present the complete brief and obtain explicit confirmation. Run `scripts/validate_vibe_brief.py --brief <json> --require-confirmed` when a machine-readable brief is available. If not confirmed, keep `VIBE_GATE: BLOCKED`.

If the game includes an Agent feature, first place it in the confirmed loop. Only then read [product-agent-spec.md](references/product-agent-spec.md) and create `product_agent_spec.md`. Do not choose a model, backend, key, or chat scope until its player value, trigger, player override, and fallback are confirmed.

## 2. Decide implementation only after the brief

Read [implementation-decisions.md](references/implementation-decisions.md) and [engine-selection.md](references/engine-selection.md).

First confirm presentation: browser-local, native desktop, mobile, cloud-streamed, console, XR, or editor-only. Then compare Unity, Unreal, and Godot against the confirmed brief and current official documentation when version-dependent facts matter. Record recommendation, tradeoffs, minimum spike, unknowns, and user confirmation in `engine_decision.md`.

Without a concrete, user-confirmed engine and presentation, record `ENGINE_DECISION: BLOCKED` and do not generate engine files. For model-backed features, request separate authority before any credential or backend action.

## 3. Select the smallest useful collaboration mode

Read [collaboration-modes.md](references/collaboration-modes.md), [role-selection-rules.md](references/role-selection-rules.md), and [delivery-contracts.md](references/delivery-contracts.md).

Write `collaboration_plan.md` before role packets. Use only independently testable roles with stable handoffs:

- **Discovery cell**: Discovery Lead only; optional short-lived Loop Analyst or Feature Critic writes read-only notes and never asks the user.
- **Prototype mode**: Lead plus bounded Prototype Architect input, then QA and Reflection.
- **Agent-MVP mode**: add Product-Agent Designer only when a confirmed in-game Agent changes the loop.
- **Standard / Studio / Takeover**: add design, art, technical, audio, release, or audit roles only for demonstrated complexity.

Long-lived roles need explicit user authorization and available task creation. Otherwise generate manual startup packets. Lead remains sole integrator.

For QA that must reach a scene directly, read [qa-gm-access-contract.md](references/qa-gm-access-contract.md). After Candidate freeze, Lead creates the bundled `qa_gm_access_manifest.json` from its template and QA validates it with `scripts/validate_qa_gm_access.py`. The GM surface must be test-only, candidate-bound, logged, resettable, and disabled by default for delivery.

Do not introduce a separate "GM" or "product owner" role for this access. The Lead alone owns the GM surface. Before QA starts a direct-scene test, it must receive: the frozen Candidate buildId, `qa_gm_access_manifest.json`, the in-scope scene/fixture list, and the reset baseline. QA may only invoke the listed commands and return command/scene/reset evidence; it cannot alter acceptance criteria, gameplay values, source, assets, configuration, saves, or Candidate files.

## 4. Bootstrap a governed workspace

After Brief, engine, collaboration plan, and output root are confirmed, use the bundled scripts:

```powershell
& python scripts/bootstrap_project.py --output-root 'D:\GameWork' --project-name 'Sky Hop' --mode greenfield --engine godot --engine-confirmed --vibe-brief 'D:\brief.json' --vibe-confirmed
& python scripts/generate_role_packets.py --project-root 'D:\GameWork\sky-hop' --scale prototype --capability startup-packets
```

`bootstrap_project.py` rejects nonempty targets and creates governance only, not an engine project. `generate_role_packets.py` creates contracts but never tasks. `generate_build_identity.py` freezes Candidate identity. `validate_delivery_gates.py` enforces matching QA/Reflection evidence.

For a package metadata check, run `scripts/quick_validate.py <skill-folder>`. It requires PyYAML; use an already-approved isolated environment and do not install it globally or add dependencies without explicit user authorization. `scripts/validate_package_structure.py` is the no-dependency fallback for local structural checks.

## 5. Build, freeze, validate, recover

1. Confirm Vibe Brief, implementation decisions, and collaboration plan.
2. Let bounded roles deliver inbound artifacts; Lead integrates.
3. Freeze Candidate and create buildId.
4. Lead exposes the frozen Candidate's QA GM allowlist when direct-scene coverage is in scope; QA verifies runtime facts through it and records command/scene evidence.
5. Reflection verifies Brief promise and experience claims.
6. Deliver only when GM access (when in scope), QA, and Reflection PASS on that buildId.

For recovery read task card → progress recap → execution log → confirmed briefs/decisions → Candidate/evidence. Read [recovery-and-invalidation.md](references/recovery-and-invalidation.md) when a decision or runtime artifact changes.
