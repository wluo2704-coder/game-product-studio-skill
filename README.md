# Game Product Studio

Turn a vague game idea into a player-confirmed, testable first playable — from core-loop discovery through a master game design specification, traceable module specs, vertical-slice proof, and governed multi-agent delivery.

> Version: v0.3.0

## What it does

Game Product Studio is a Codex Skill for personal game vibecoding. It helps turn “I want to make a game like…” into a concrete, user-confirmed product direction before agents begin broad implementation.

It is designed for a personal playable MVP, not an automatic commercial-game factory.

- Uses one plain-language, adaptive discovery conversation to find the player’s actual core loop.
- Separates references, desired features, core-loop evidence, and game-internal Agent ideas.
- Compiles the confirmed result into a versioned Master Game Design Specification.
- Branches only needed module specs — combat, systems, balance, content, UI/scene flow, Agent features, art/audio, or technical testability.
- Makes every module requirement traceable to a master requirement and test/acceptance ID.
- Requires a runnable core-loop vertical slice before broad production.
- Creates a runtime testability contract for scenes, states, actions, reset baselines, state snapshots, timing, and evidence.
- Coordinates a bounded Lead / specialist / QA / Reflection workflow with Candidate and same-build gates.

## The workflow

```text
Vague idea
  -> Discovery Lead conversation
  -> Confirmed Vibe Brief                 (VIBE_GATE)
  -> Confirmed Master Game Design Spec    (MASTER_SPEC_GATE)
  -> Engine and presentation decision     (ENGINE_DECISION)
  -> Traceable module-spec graph          (SPEC_GRAPH_GATE)
  -> Runnable core-loop vertical slice    (SLICE_GATE)
  -> Runtime testability contract          (TESTABILITY_GATE)
  -> Bounded collaboration plan
  -> Frozen Candidate
  -> QA GM / QA / Reflection on one build
  -> Personal playable delivery
```

## The design source of truth

After discovery, the Lead creates both a human-readable and a machine-readable master spec:

```text
master_game_design_spec.md
master_game_design_spec.json
  -> spec_graph.json
      -> module design specs
      -> acceptance and test IDs
      -> runtime_testability_contract.json
      -> QA-only GM access manifest
```

The master spec contains the player promise, core loop, first-playable boundary, scene/experience flow, requirements, assumptions, deferred decisions, and user confirmation.

Child module specs refine implementation detail. They cannot silently change the core loop or MVP scope. A direction change requires a logged, user-confirmed new master-spec version; affected modules, test scenarios, QA GM manifests, and runtime evidence then become stale.

## Core-loop-first discovery

The Skill asks at most 15 user-visible questions and only one at a time. It first clarifies what the player repeatedly does and sees:

```text
player action -> game response -> player decision -> observable result
```

A reference game is not automatically a loop. “Add an Agent” is not automatically a loop either. The Lead records both, but first confirms where an Agent feature serves the player’s already-confirmed game loop.

Before implementation starts, the Skill presents a full summary and waits for explicit user confirmation.

## Vertical slice and testability

Before broad module work, the Skill requires a real, smallest traversal of the core loop. Each critical scenario records:

- stable `sceneId` and entry `stateId`;
- player/test action and expected response;
- observable result and assertions;
- `reset_run` baseline;
- runtime-state, visual, and console/log evidence;
- retain, revise, or stop decision.

The intended operating rhythm is deliberately short:

```text
make one bounded change -> run -> observe -> adjust
```

For browser games, expose `window.advanceTime(ms)` and `window.render_game_to_text()` where practical. Other engines should provide a small documented equivalent through a QA-only test adapter. Launching a game or loading a scene is not sufficient evidence that the interaction works.

## Controlled QA GM access

The GM surface is not a separate product owner or a development role. The integration Lead owns it; QA may only invoke a frozen Candidate’s runtime-only allowlist.

Allowed examples:

- `load_scene(sceneId)` for an in-scope test scene;
- `set_test_state(stateId)` for a predefined fixture;
- `grant_test_resource(resourceId, amount)` for a predefined test resource;
- `reset_run()` for the declared baseline.

The allowlist is derived from `runtime_testability_contract.json`, bound to one Candidate build ID, logged, and disabled by default in delivery builds. QA cannot modify gameplay values, acceptance criteria, source, assets, configuration, saves, files, network state, or run arbitrary code/scripts/commands.

## Collaboration model

The Lead is the only writer of source, configuration, Candidate, and formal delivery. All other roles have bounded outputs and must hand back trace IDs, evidence, assumptions, and `NOT TESTED` items.

| Mode | Typical roles |
| --- | --- |
| Single | Lead, QA, Reflection |
| Prototype | Lead, Prototype Architect, QA, Reflection |
| Agent MVP | Prototype roles plus Product-Agent Designer |
| Standard / Studio | Add Design, Art, Technical, Audio, or Release only when needed |

The Skill generates manual startup packets by default. It never creates long-lived tasks unless the user explicitly authorizes it.

## Install

### From this repository

1. Download or clone this repository.
2. Locate the `game-product-studio/` directory from the release package.
3. Install it into your Codex Skills location using your normal Codex Skill installation workflow, or copy the directory into a user-approved local Skills directory.
4. Restart or refresh Codex if your environment requires it.

Do not copy `README.md`, release notes, or archives into the Skill directory. The package itself starts at `game-product-studio/SKILL.md`.

### Validate the package

```powershell
python scripts/validate_package_structure.py .
python scripts/quick_validate.py .
```

`quick_validate.py` needs PyYAML. Use an already-approved isolated Python environment if it is not installed; do not globally install dependencies merely to validate the Skill.

## Quick start

```text
Use $game-product-studio to help me turn this game idea into a first playable:
I want a game where I draw creatures that then fight for me.
```

The Skill will guide the discovery conversation, summarize the confirmed Vibe Brief, compile and ask confirmation for the Master Spec, then move through engine choice, vertical slice, testability, and controlled implementation.

## Included package layout

```text
game-product-studio/
├── SKILL.md
├── agents/openai.yaml
├── assets/project-templates/
│   ├── master_game_design_spec.md / .json
│   ├── module_design_spec.md
│   ├── spec_graph.json
│   ├── vertical_slice_gate.json
│   ├── runtime_testability_contract.json
│   └── qa_gm_access_manifest.json
├── references/
│   ├── master-design-and-spec-graph.md
│   ├── vertical-slice-and-testability.md
│   └── qa-gm-access-contract.md
└── scripts/
    ├── bootstrap_project.py
    ├── validate_master_spec.py
    ├── validate_spec_graph.py
    ├── validate_vertical_slice.py
    ├── validate_runtime_testability.py
    ├── validate_qa_gm_access.py
    └── validate_delivery_gates.py
```

## Safety and scope

- No engine project is initialized before confirmed Vibe Brief, Master Spec, engine, and presentation decisions.
- No global installs, API keys, account/network changes, external publishing, or writes outside the approved root happen without explicit authorization.
- Game-internal Agent features remain optional and require player value, trigger, override, and fallback.
- Online services, monetization, analytics, live operations, multiplayer, and public release are out of scope unless the user explicitly requests them.

## Version notes

See [UPDATE_NOTES_v0.3.md](UPDATE_NOTES_v0.3.md) for the v0.3.0 changes and migration notes from v0.2.1.

## License

See [LICENSE](LICENSE).
