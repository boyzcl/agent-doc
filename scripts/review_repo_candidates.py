#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import re

from runtime_memory_lib import load_json, resolve_runtime_resolution, write_json


STATUS_RE = re.compile(r"^(review_status:[ \t]*)([^\n]*)$", re.MULTILINE)
REASON_RE = re.compile(r"^(review_reason:[ \t]*)([^\n]*)$", re.MULTILINE)
REVIEWED_AT_RE = re.compile(r"^(reviewed_at:[ \t]*)([^\n]*)$", re.MULTILINE)
SOURCE_NOTE_RE = re.compile(r"^source_note_slug:[ \t]*([^\n]+)$", re.MULTILINE)


def parse_candidate_metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    metadata = {"slug": path.stem, "path": str(path)}
    for key in ["review_status", "review_reason", "reviewed_at", "source_note_slug", "scene", "doc_type"]:
        match = re.search(rf"^{key}:[ \t]*([^\n]*)$", text, re.MULTILINE)
        metadata[key] = match.group(1).strip() if match else ""
    return metadata


def update_candidate(path: Path, status: str, reason: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = STATUS_RE.sub(rf"\1{status}", text, count=1)
    text = REASON_RE.sub(rf"\1{reason}", text, count=1)
    text = REVIEWED_AT_RE.sub(rf"\1{datetime.now().astimezone().isoformat()}", text, count=1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="List or update local agent-doc repo candidates.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    parser.add_argument("--slug", default=None, help="Repo candidate slug to update.")
    parser.add_argument(
        "--status",
        choices=["pending", "accepted", "rejected"],
        default=None,
        help="New review status for the selected repo candidate.",
    )
    parser.add_argument("--reason", default="", help="Optional reason recorded with the review decision.")
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    candidate_dir = resolution.runtime_root / "promoted" / "repo-candidates"
    ledger_path = resolution.runtime_root / "state" / "promotion-ledger.json"
    ledger = load_json(ledger_path)

    if args.slug and args.status:
        path = candidate_dir / f"{args.slug}.md"
        if not path.exists():
            raise SystemExit(f"repo candidate does not exist: {args.slug}")
        update_candidate(path, args.status, args.reason)
        repo_stats = ledger.setdefault("repo_candidate_stats", {})
        repo_stats.setdefault(args.slug, {})
        repo_stats[args.slug]["review_status"] = args.status
        repo_stats[args.slug]["review_reason"] = args.reason
        repo_stats[args.slug]["last_updated_at"] = datetime.now().astimezone().isoformat()
        source_match = SOURCE_NOTE_RE.search(path.read_text(encoding="utf-8"))
        if source_match:
            repo_stats[args.slug]["source_note_slug"] = source_match.group(1).strip()
        write_json(ledger_path, ledger)

    items = [parse_candidate_metadata(path) for path in sorted(candidate_dir.glob("*.md"))]
    print(json.dumps(items, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
