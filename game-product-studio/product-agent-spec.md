# Master design and specification graph

## Purpose

The master design spec is the single design source of truth after the Vibe Brief. It converts a confirmed player intention into an implementable first-playable contract without pretending that every later detail is already known.

## Required master-spec sections

1. **Intent and promise** — target player, one-line game, intended feeling, and reference boundaries.
2. **Core loop** — player action -> game response -> repeated decision -> observable result. State its success/failure condition and first-playable non-negotiable.
3. **MVP boundary** — in scope, explicitly out of scope, and deferred decisions.
4. **Experience map** — entry, key scenes/states, first five-minute flow, feedback, and end/return state.
5. **Requirements** — stable `MASTER-<AREA>-<NNN>` IDs. Mark each as `confirmed`, `suggested`, or `undecided` and quote/source the confirmation.
6. **Assumptions and risks** — smallest experiment that can invalidate each important assumption.
7. **Version and confirmation** — version, decision log link, summary shown to the user, and explicit response.

## Branching rules

- Create only MVP-relevant modules. A small game may need only `combat`, `ui_scene_flow`, and `technical_testability`.
- Pin every module to `masterSpecVersion` and list the master requirement IDs it refines. A module may add implementation detail, not game direction.
- Every in-scope module requirement needs at least one acceptance/test ID. Put cross-module dependencies in `spec_graph.json`, not only prose.
- When a master requirement changes, record the decision, raise the master version, and mark dependent module requirements, scenarios, QA GM manifests, and Candidate evidence stale.
- Agent features are their own module only if they are inside the confirmed loop. Their requirements must trace to loop/player-value requirements rather than “use AI”.

## Graph model

```text
confirmed Vibe Brief
  -> Master requirements (versioned)
     -> Module requirements (traceTo master IDs)
        -> Acceptance/test IDs
           -> Scenario/state/evidence in the testability contract
              -> QA GM allowlist and Candidate evidence
```

No arrow may be skipped. `NOT TESTED`, a missing trace, or a stale parent version blocks the affected item rather than becoming an implicit PASS.
