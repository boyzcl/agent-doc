#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json

from runtime_memory_lib import iter_capture_records, load_json, resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Report local agent-doc runtime governance metrics.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown.")
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    runtime_root = resolution.runtime_root
    queue = load_json(runtime_root / "inbox" / "review-queue.json")
    ledger = load_json(runtime_root / "state" / "promotion-ledger.json")
    reuse = load_json(runtime_root / "state" / "reuse-ledger.json")
    captures = iter_capture_records(runtime_root)

    report = {
        "runtime_root": str(runtime_root),
        "host": resolution.host_id,
        "support_tier": resolution.support_tier,
        "capture_count": len(captures),
        "pending_backlog_size": len(queue.get("pending", [])),
        "reviewed_count": len(queue.get("reviewed", [])),
        "field_note_count": len(list((runtime_root / "promoted" / "field-notes").glob("*.md"))),
        "repo_candidate_count": len(list((runtime_root / "promoted" / "repo-candidates").glob("*.md"))),
        "archive_count": len(list((runtime_root / "promoted" / "archive").glob("*.md"))),
        "reuse_event_count": len(reuse.get("events", [])),
        "last_run_id": ledger.get("last_run_id"),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
        return 0

    lines = [
        "# agent-doc runtime governance report",
        "",
        f"- runtime_root: `{report['runtime_root']}`",
        f"- host: `{report['host']}`",
        f"- support_tier: `{report['support_tier']}`",
        f"- capture_count: `{report['capture_count']}`",
        f"- pending_backlog_size: `{report['pending_backlog_size']}`",
        f"- reviewed_count: `{report['reviewed_count']}`",
        f"- field_note_count: `{report['field_note_count']}`",
        f"- repo_candidate_count: `{report['repo_candidate_count']}`",
        f"- archive_count: `{report['archive_count']}`",
        f"- reuse_event_count: `{report['reuse_event_count']}`",
        f"- last_run_id: `{report['last_run_id']}`",
    ]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
