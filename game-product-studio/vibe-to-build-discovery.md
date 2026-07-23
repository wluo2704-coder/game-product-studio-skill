# Vertical slice and runtime testability

## Vertical slice gate

Build one small but real traversal of the confirmed loop before scaling content or modules. The slice must use representative player input, runtime response, a meaningful decision or outcome, and the intended feedback direction; mocked art or reduced content is acceptable when recorded.

For each iteration, change one bounded thing, run it, observe it, and adjust from evidence. Do not call a static mockup, a menu-only flow, or an unobserved code path a playable slice.

`SLICE_GATE: PASS` requires:

- a focused master requirement and matching test ID;
- entry `sceneId` and `stateId`;
- a concrete player action, expected response, and observable result;
- reset evidence and runtime-state, visual, and console/log evidence;
- `decision: RETAIN` and recorded follow-up scope.

Use `REVISE` or `STOP` honestly when the slice falsifies the promise. They are valuable outcomes, but they do not open broad implementation.

## Runtime testability contract

Make testing a property of the game build, not a memory of how someone clicked through it. For every in-scope test, declare:

- stable `sceneId`, entry `stateId`, and reset baseline;
- allowed player/test actions and expected observable assertions;
- a machine-readable state snapshot, e.g. browser `window.render_game_to_text()` or an engine-equivalent export;
- deterministic time advancement, engine-step equivalent, or a documented manual-time limitation;
- visual and console/log evidence outputs;
- test/acceptance IDs and master requirement traceability.

For browser games, provide `window.advanceTime(ms)` and `window.render_game_to_text()` when practical. For Unity, Godot, or other engines, expose the smallest documented equivalent through a QA-only test adapter. Do not expose a player cheat interface just to satisfy this contract.

## QA GM derivation

If direct-scene testing is in scope, derive GM `load_scene`, fixture, and `reset_run` entries from the contract's declared scene/state/baseline IDs. Lead owns the generated allowlist. QA receives runtime-only access after Candidate freeze and cannot add a scene, state, resource, command, or acceptance condition.

## Regression rule

When a runtime-relevant item changes, rerun every scenario that traces to it. Inspect the visual observation, state snapshot, and console/log; passing launch or loading a scene is never enough.
