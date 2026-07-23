# Discovery interview

## Interview sequence

1. Ask who will play, the desired feeling, and the one thing they should repeatedly do.
2. Ask for adjacent references, one-session length, visual direction, devices, and presentation/release channel.
3. Ask online/offline needs, content scale, time/budget, technical capability, and how hands-on the user wants to be.
4. Explain the remaining consequential tradeoffs, propose the smallest feasible MVP, then ask for confirmation.

Use plain language: “browser-local” means the game downloads and runs on the player's device; “cloud streaming” means a server renders it and the browser receives interactive video. Do not use an acronym before explaining it.

## Brief schema

Use a Markdown table with `field`, `value`, and `status`. Required fields are `players`, `core_experience`, `core_loop`, `references`, `session_length`, `visual_direction`, `target_devices`, `presentation`, `release`, `online`, `content_scope`, `time_budget`, `user_capability`, `user_involvement`, `mvp_hypothesis`, and `risks`.

## Guardrails

- Ask a follow-up instead of treating silence as consent.
- Mark inferred defaults as `suggested`.
- If a user changes a confirmed field, preserve the old decision in a decision log and update downstream assumptions.
- Do not choose an engine during discovery; hand off to engine selection.
