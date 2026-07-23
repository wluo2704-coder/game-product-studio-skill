#!/usr/bin/env python3
"""Create a deterministic identity manifest for a frozen Candidate directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def tree_hash(root: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    count = 0
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        count += 1
    return digest.hexdigest(), count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source", help="Optional frozen source snapshot directory")
    parser.add_argument("--schema", default="unknown")
    args = parser.parse_args()
    candidate = Path(args.candidate).expanduser().resolve()
    if not candidate.is_dir() or not any(candidate.rglob("*")):
        fail("--candidate must be a nonempty frozen directory")
    output = Path(args.output).expanduser().resolve()
    if output.exists():
        fail(f"refusing to overwrite existing manifest: {output}")
    candidate_hash, file_count = tree_hash(candidate)
    source_hash = None
    if args.source:
        source = Path(args.source).expanduser().resolve()
        if not source.is_dir():
            fail("--source must be a directory")
        source_hash, _ = tree_hash(source)
    build_id = f"{args.version}-{candidate_hash[:12]}"
    manifest = {"version": args.version, "buildId": build_id, "createdAt": datetime.now(timezone.utc).isoformat(),
                "candidatePath": str(candidate), "candidateSha256": candidate_hash, "candidateFileCount": file_count,
                "sourceSha256": source_hash, "schema": args.schema, "status": "FROZEN",
                "invalidationRule": "Any runtime-relevant source, config, asset, scene, schema, build or hosting change invalidates this manifest and all associated gates."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
