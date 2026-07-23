# Engine and presentation selection

Recheck version-sensitive statements in official Unity, Epic/Unreal, and Godot documentation at decision time. Write the URLs and check date in `engine_decision.md`.

| Candidate | Good initial fit | Costs / questions to disclose |
| --- | --- | --- |
| Unity | Cross-platform 2D/3D, mobile, desktop, XR, and teams already comfortable with its workflow. | For browser-local delivery, validate browser performance, memory, package size, threading, networking, audio, storage, and target-browser support. |
| Unreal | High-fidelity 3D, complex scenes, PC/console/XR, Blueprint/C++ workflows, and teams that can sustain heavier production. | Browser experience may instead be Pixel Streaming: a packaged app renders on server hardware and streams through WebRTC; disclose hosting, GPU, networking, latency, and operational cost rather than calling it a local Web export. |
| Godot | Lightweight open-source work, fast prototypes, 2D and modest 3D, small teams, and ownership/control priorities. | For browser-local delivery, validate WebAssembly/WebGL rendering mode, C# compatibility, threading headers, browser/mobile limits, storage, audio, and service configuration. |

## Decision record

For each candidate state: fit to confirmed brief, benefits, meaningful costs, unknowns, small validation spike, official source URLs/date, and recommendation. Record the user's final explicit choice. No choice means `ENGINE_DECISION: BLOCKED`.
