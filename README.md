# Game Product Studio

Turn a vague game idea into a confirmed first-playable concept, then create a controlled and recoverable multi-agent MVP workflow.

> A Codex Skill for personal game vibecoding. It helps clarify what the player repeatedly does before discussing implementation details, engines, or Agent features.

## What it does

- Guides a plain-language conversation from a vague game idea to a user-confirmed Vibe-to-Build Brief.
- Identifies the core gameplay loop:

  ```text
  player action → game response → player decision → observable result
Separates:reference games and aesthetic inspiration;
candidate features;
game-internal Agent features;
development collaboration roles.

Uses one user-facing Lead and controlled handoffs for prototype, design, QA, and reflection work.
Provides templates and scripts for governed project bootstrap, role packets, Candidate identity, validation gates, and recovery.
Core principles
Core loop first
A reference game or a request such as “add an Agent” is not automatically the gameplay loop.

User confirmation before implementation
The Skill summarizes the complete Vibe-to-Build Brief and waits for the user to confirm it before progressing.

Game Agent ≠ development Agent
A game-internal Agent is a possible player-facing feature. Development roles are collaborators. They have different responsibilities and permissions.

One integration owner
The Lead is the only role that writes integrated source, configuration, Candidate artifacts, and formal delivery.

Evidence-based delivery
QA and Reflection are read-only gates. Both must validate the same frozen Candidate build.

What it does not do
It does not promise to build a complete commercial game in one run.
It does not create engine projects before the Vibe Brief and engine decision are confirmed.
It does not automatically create long-lived tasks, install dependencies globally, create credentials, publish projects, or change accounts/network settings.
It does not force an Agent feature into the game loop before the player value is clear.
Install in Codex
Copy or symlink the game-product-studio folder into your Codex Skills directory.
Windows
Copy-Item -Recurse .\game-product-studio "$HOME\.codex\skills\game-product-studio"
Restart or reload Codex after installation.
Project-local installation
You can also place the folder in a project-local Skills location:
your-project/
└── .agents/
    └── skills/
        └── game-product-studio/
Use
Invoke the Skill directly:
Use $game-product-studio to help me turn my game idea into a confirmed MVP plan.
Example input:
I want to make a game like Plants vs. Zombies, but with an Agent feature.
The Skill should first clarify the repeated player action and decision. It returns to the Agent idea only after the core loop is understood.
Package contents
Path	Purpose
SKILL.md	Main workflow, gates, and safety boundaries
agents/openai.yaml	Codex display metadata
references/	Discovery, classification, implementation, collaboration, and recovery rules
assets/project-templates/	Brief, Agent spec, collaboration, QA, Reflection, and recovery templates
scripts/	Validation, bootstrap, role-packet, Candidate, and delivery-gate helpers

Validation
Run the dependency-free structural check:
python .\game-product-studio\scripts\validate_package_structure.py .\game-product-studio
Expected result:
PACKAGE_STRUCTURE_VALIDATION=PASS
To validate the Skill frontmatter:
$env:PYTHONUTF8 = "1"
python .\game-product-studio\scripts\quick_validate.py .\game-product-studio
Expected result:
Skill is valid!
quick_validate.py requires PyYAML. Prefer an isolated virtual environment or isolated dependency directory. Do not install dependencies globally unless you explicitly choose to.
Collaboration modes
Mode	Use when	Roles
Discovery	The idea is still vague	Discovery Lead; optional read-only analyst notes
Prototype	One small loop needs a first-playable test	Lead, Prototype Architect, QA, Reflection
Agent-MVP	A confirmed game-internal Agent changes the loop	Prototype roles plus Product-Agent Designer
Standard	Sustained design or art work is needed	Lead, design, art, QA, Reflection
Studio	The project has multi-platform, technical, audio, or release complexity	Add only the relevant specialists
Takeover	An existing project lacks ownership or evidence	Lead, QA, Reflection audit first

Safety and delivery gates
The workflow uses these gates:
VIBE_GATE
→ ENGINE_DECISION
→ COLLABORATION_GATE
→ CANDIDATE
→ QA_GATE + REFLECTION_GATE
→ DELIVERY
VIBE_GATE: the user confirms the core gameplay Brief.
ENGINE_DECISION: presentation and engine are confirmed before engine initialization.
CANDIDATE: the Lead freezes a build identity after integration.
QA_GATE: verifies runtime and factual evidence.
REFLECTION_GATE: verifies player promise, experience, and delivery claims.
QA and Reflection must cite the same Candidate build ID.
License
This project is released under the MIT License.
Contributing
Issues and pull requests are welcome.
When contributing:
Preserve the core-loop-first rule.
Keep game-internal Agent features separate from development collaboration roles.
Do not add automatic installation, credential, publishing, or task-creation behavior without explicit user authorization.
Include validation evidence for script changes.
