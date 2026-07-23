# Intent Classification

Classify each user statement before deciding the next question.

| Class | Meaning | Next action |
| --- | --- | --- |
| `core_loop_evidence` | Repeated player action, response, choice, or result. | Record it and fill the smallest missing loop link. |
| `core_loop_modifier` | Changes a repeated choice or feedback. | Record how it changes the loop. |
| `candidate_feature` | Requested feature not yet placed in the loop. | Preserve it; do not design it yet. |
| `auxiliary_feature` | Does not change repeated action, choice, or result. | Defer from core MVP unless user prioritizes it. |
| `reference_or_flavor` | Reference, theme, mood, character, visual preference. | Use as expression only. |
| `delivery_choice` | Device, presentation, engine, online, process. | Defer to implementation decisions. |

If a user says “add an Agent,” classify it as `candidate_feature`. If they say “the Agent recommends a plant and I decide whether to follow it,” classify it as `core_loop_modifier`; then determine whether it belongs in the first playable.
