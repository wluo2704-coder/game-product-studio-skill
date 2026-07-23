# Game Product Studio

**Version: v0.2.1**

A Codex Skill for turning vague game ideas into confirmed core gameplay loops, then guiding a controlled and recoverable multi-agent MVP workflow.

## What it does

- Helps users clarify the core gameplay loop before discussing implementation details, engines, or Agent features.
- Separates reference games, candidate features, game-internal Agents, and development collaboration roles.
- Uses one user-facing Lead to integrate source, configuration, Candidate artifacts, and formal delivery.
- Supports Prototype, Agent-MVP, Standard, Studio, and Takeover collaboration modes.
- Lets QA directly reach in-scope scenes through a Lead-owned, Candidate-bound GM command allowlist.
- Requires Candidate, QA, Reflection, and recovery evidence before delivery.

## Core gameplay-loop rule

The Skill establishes this minimum chain before implementation:

```text
player action → game response → player decision → observable result
A reference game or a request such as “add an Agent” is not automatically the core loop. The user must confirm the complete Vibe-to-Build Brief before the workflow moves to implementation.
Controlled Agent collaboration
Development roles
Role	Responsibility
Lead	Only user-facing voice; sole owner of integrated source, configuration, Candidate, and formal delivery
Prototype Architect	Plans small core-loop experiments
Product-Agent Designer	Specifies a confirmed game-internal Agent feature
QA	Verifies runtime behavior and evidence
Reflection	Independently verifies player-promise and experience fit

Game-internal Agent vs. development Agent
A game-internal Agent is a possible product feature for players.
Development roles are collaborators used to build and validate the game.
They are separate concepts and must never be confused.
QA direct-scene GM access
When QA needs to test a Boss scene or another specific scene directly, the Lead provides a controlled GM command surface inside the frozen Candidate.
Lead creates and owns GM allowlist
→ Candidate is frozen with a buildId
→ QA invokes approved runtime commands
→ QA records scene and command evidence
→ QA resets the test state
→ QA and Reflection validate the same buildId
QA may
Invoke only Lead-provided, Candidate-bound GM commands.
Load approved in-scope scenes.
Apply predefined test fixtures or test resources.
Reset the run to a known baseline.
Capture screenshots, recordings, logs, defects, and evidence.
QA may not
Modify source code, configuration, assets, gameplay values, saves, or Candidate files.
Add or extend GM commands.
Run arbitrary code, scripts, shell commands, file operations, or network calls.
Change acceptance criteria.
Use a GM surface that is not bound to the frozen Candidate buildId.
Minimum GM allowlist
Command	Purpose
load_scene	Open an approved in-scope scene
set_test_state	Apply a predefined test fixture
grant_test_resource	Grant a predefined test resource
reset_run	Restore the known baseline

All GM invocations must record:
time / buildId / QA identity / command / parameters / result / evidence path
The GM surface is enabled only for QA testing and is disabled by default for formal delivery.
Delivery gates
VIBE_GATE
→ ENGINE_DECISION
→ COLLABORATION_GATE
→ CANDIDATE
→ QA_GM_ACCESS_GATE (when direct-scene testing is in scope)
→ QA_GATE + REFLECTION_GATE
→ DELIVERY
VIBE_GATE: the user confirms the core gameplay Brief.
ENGINE_DECISION: presentation and engine are confirmed before engine initialization.
CANDIDATE: the Lead freezes a build identity.
QA_GM_ACCESS_GATE: the Lead-provided GM manifest is bound to the Candidate buildId and passes validation.
QA_GATE: runtime and structural evidence pass.
REFLECTION_GATE: player promise and experience claims pass.
QA, Reflection, and GM access evidence must reference the same Candidate buildId.
Install in Codex
Copy or symlink the game-product-studio folder into your Codex Skills directory.
Windows
Copy-Item -Recurse .\game-product-studio "$HOME\.codex\skills\game-product-studio"
Restart or reload Codex after installation.
Project-local installation
You can also place the Skill inside a project:
your-project/
└── .agents/
    └── skills/
        └── game-product-studio/
Use
Use $game-product-studio to help me turn my game idea into a confirmed MVP plan.
Example:
I want to make a game like Plants vs. Zombies, but with an Agent feature.
The Skill first clarifies what the player repeatedly does, sees, and decides. It returns to the Agent idea only after the core loop is clear.
Package contents
Path	Purpose
SKILL.md	Main workflow, collaboration rules, and safety boundaries
agents/openai.yaml	Codex display metadata
references/	Discovery, classification, implementation, collaboration, recovery, and QA GM rules
references/qa-gm-access-contract.md	Lead-owned QA GM access rules
assets/project-templates/	Brief, Agent spec, collaboration, QA, Reflection, and recovery templates
assets/project-templates/qa_gm_access_manifest.json	Candidate-bound QA GM allowlist template
scripts/validate_vibe_brief.py	Validates a confirmed Vibe-to-Build Brief
scripts/bootstrap_project.py	Creates a governed, engine-neutral workspace
scripts/generate_role_packets.py	Generates manual role startup packets without creating tasks
scripts/generate_build_identity.py	Creates a frozen Candidate build identity
scripts/validate_qa_gm_access.py	Validates QA GM access scope and Candidate build binding
scripts/validate_delivery_gates.py	Validates same-build QA, Reflection, and GM evidence
scripts/quick_validate.py	Validates Skill metadata frontmatter

Validation
Run the dependency-free structural check:
python .\game-product-studio\scripts\validate_package_structure.py .\game-product-studio
Expected result:
PACKAGE_STRUCTURE_VALIDATION=PASS
Validate Skill frontmatter:
$env:PYTHONUTF8 = "1"
python .\game-product-studio\scripts\quick_validate.py .\game-product-studio
Expected result:
Skill is valid!
quick_validate.py requires PyYAML. Prefer an isolated Python environment; do not install dependencies globally unless you explicitly choose to.
Safety boundaries
The user remains the decision-maker for game direction, scope, engine, model provider, credentials, and release.
The Skill does not initialize an engine before Brief and engine confirmation.
The Skill does not automatically create long-lived tasks, install dependencies, create keys, publish projects, or change accounts or networking.
Lead is the only integrated source and Candidate writer.
QA and Reflection are read-only.
Runtime-relevant changes invalidate earlier QA and Reflection evidence.
License
This project is released under the MIT License.
Contributing
Issues and pull requests are welcome.
When contributing:
Preserve the core-loop-first rule.
Keep game-internal Agent features separate from development collaboration roles.
Keep QA GM access Lead-owned, Candidate-bound, allowlisted, logged, resettable, and disabled by default for delivery.
Do not add automatic installation, credential, publishing, or task-creation behavior without explicit user authorization.
Include validation evidence for script changes.
