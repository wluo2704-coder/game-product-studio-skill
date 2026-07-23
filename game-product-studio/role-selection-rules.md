# Recovery and invalidation

Any change to a confirmed Brief, Master Spec, engine decision, source, configuration, asset, scene, schema, build, or hosting that can alter behavior invalidates affected downstream evidence. When direction or scope changes, record a Master Spec decision, raise its version, mark dependent module requirements and scenarios stale, refresh the collaboration plan if necessary, freeze a new Candidate, and rerun the checks that depend on the changed artifact.

Recover in this order:

`task card -> progress recap -> execution log -> decision log -> confirmed Vibe Brief and Master Spec -> spec graph -> vertical slice/testability contract -> Candidate manifest -> QA/Reflection evidence`

Do not use a child module document, a previous test report, or chat memory to silently override the confirmed master design.
