# Delivery contracts

## Role packet required fields

Include the role goal, current SOT, inputs, allowed output directory, forbidden writes, acceptance checks, handoff recipient, escalation conditions, and recovery order. Never grant overlapping source-write access.

## QA report required fields

Include candidate absolute path, version/buildId, manifest path, scope, evidence, coverage matrix, `PASS | FAIL | BLOCKED | NOT TESTED`, defects, and next action. QA cannot modify candidate files.

## Reflection report required fields

Include user goal, scope, candidate path, version/buildId, evidence-level assessment, goal-fit conclusion, module matrix, risks, and `REFLECTION_GATE: PASS | REVISE | BLOCKED`. `PASS` is the only delivery authorization.

## Manual fallback

When task creation is unavailable or unauthorized, provide a numbered start order and one copyable prompt per role. State that copying a packet does not transfer write authority or authorize external actions.
