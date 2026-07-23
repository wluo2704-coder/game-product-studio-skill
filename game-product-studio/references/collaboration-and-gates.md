# Collaboration, Candidate, and gates

## Gate sequence

1. `VIBE_GATE`: the user explicitly confirms a brief containing a playable action, response, repeated decision, observable result, and first playable core.
2. `ENGINE_DECISION`: presentation and engine are explicitly confirmed before any engine initialization.
3. `COLLABORATION_GATE`: a written collaboration plan names only the roles needed for independent, testable work.
4. `CANDIDATE`: the Lead freezes a manifest after integration.
5. `QA_GATE` and `REFLECTION_GATE`: both cite the same manifest buildId.

## Agent distinction

A game-internal Agent is a possible product feature. It must be placed inside the confirmed core loop and have a player value, trigger, override, and fallback before a Product-Agent Designer is added. Development roles are collaborators; they do not become product features and only the Discovery Lead speaks to the user.

## Candidate contract

The frozen manifest contains version, buildId, created time, candidate hash, optional source hash, schema/version, change summary, and evidence paths. Any runtime-relevant source, configuration, resource, scene, schema, build, or hosting change invalidates earlier gates.

## Delivery decision

`QA_GATE: PASS` verifies factual/running evidence. `REFLECTION_GATE: PASS` verifies Vibe Brief fit and delivery claims. `FAIL`, `BLOCKED`, `NOT TESTED` for in-scope critical behavior, missing evidence, or mismatched buildId blocks delivery.

## Recovery

Resume from task card, progress recap, execution log, confirmed briefs and decisions, then Candidate/evidence. Do not depend on chat replay.
