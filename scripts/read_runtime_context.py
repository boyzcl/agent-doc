#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json

from runtime_memory_lib import (
    read_promoted_field_notes,
    read_recent_captures,
    record_promoted_note_reuse,
    resolve_runtime_resolution,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read recent agent-doc runtime captures.")
    parser.add_argument("--scene", default=None, help="Scene tag to filter by.")
    parser.add_argument("--doc-type", default=None, help="Doc type to filter by.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of captures to return.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    parser.add_argument(
        "--include-promoted",
        action="store_true",
        help="Return up to 3 relevant promoted field notes together with recent captures.",
    )
    parser.add_argument(
        "--record-reuse",
        action="store_true",
        help="When promoted notes are returned, write reuse-hit events into runtime state.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    captures = read_recent_captures(
        resolution.runtime_root,
        scene=args.scene,
        doc_type=args.doc_type,
        limit=args.limit,
    )
    if not args.include_promoted:
        print(json.dumps(captures, ensure_ascii=True, indent=2))
        return 0

    promoted = read_promoted_field_notes(
        resolution.runtime_root,
        scene=args.scene,
        doc_type=args.doc_type,
        limit=3,
    )
    reuse = None
    if args.record_reuse:
        reuse = record_promoted_note_reuse(
            resolution.runtime_root,
            promoted,
            scene=args.scene,
            doc_type=args.doc_type,
        )

    print(
        json.dumps(
            {
                "captures": captures,
                "promoted_field_notes": promoted,
                "reuse_recorded": reuse,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
