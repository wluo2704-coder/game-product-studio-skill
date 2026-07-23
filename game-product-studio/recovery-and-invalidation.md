# QA GM access contract

## Purpose

The Lead provides a candidate-bound GM command surface so QA can directly reach an in-scope scene or test state without changing game source, configuration, assets, or Candidate files.

## Authority and lifecycle

- Lead implements and owns the surface; QA may invoke it but may not extend its commands.
- Create the access manifest only after the Candidate buildId exists. Bind it to exactly that buildId.
- Derive allowed scenes, entry states, reset baselines, and test scenario IDs from the approved runtime testability contract. Record the matching master-spec version in the GM manifest.
- The surface is enabled only for the QA test build. Production or formal delivery defaults to disabled.
- A command changes runtime state only. It must not execute arbitrary code, write files, alter source/configuration, make network calls, or publish.
- Every invocation logs time, buildId, QA identity, command, parameters, result, and evidence path.
- `reset_run` restores a known baseline before each independent scenario. A GM-surface change invalidates QA and Reflection evidence.

## Minimum allowlist

| Command | Purpose | Minimum parameters |
| --- | --- | --- |
| `load_scene` | Open an in-scope scene | `sceneId` |
| `set_test_state` | Set a predefined fixture only | `stateId` |
| `grant_test_resource` | Grant a predefined test resource only | `resourceId`, `amount` |
| `reset_run` | Restore the baseline | none |

Do not expose arbitrary scene paths, script evaluation, shell commands, file operations, networking, configuration mutation, or unbounded resource IDs.

## Gate

`QA_GM_ACCESS_GATE: PASS` requires a manifest that names the frozen buildId, matching master-spec version, contract-derived scenario/scene/state/reset entries, an allowlist containing `load_scene` and `reset_run`, an audit-log path, and `deliveryDefault: DISABLED`. QA cannot issue `QA_GATE: PASS` without it when direct-scene testing is in scope.
