#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from runtime_memory_lib import (
    ensure_runtime_root,
    load_json,
    read_capture_record,
    resolve_runtime_resolution,
    sanitize_text,
    write_json,
)


TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]+")
STOP_TOKENS = {
    "agent",
    "current",
    "docs",
    "document",
    "field",
    "for",
    "from",
    "into",
    "local",
    "note",
    "runtime",
    "skill",
    "that",
    "the",
    "this",
    "with",
}


def slugify(text: str, limit: int = 80) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return (slug or "runtime-note")[:limit].strip("-") or "runtime-note"


def textify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(textify(item) for item in value if textify(item))
    return str(value)


def string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [textify(item) for item in value if textify(item)]
    rendered = textify(value)
    return [rendered] if rendered else []


def normalize_tokens(*parts: str) -> set[str]:
    tokens: set[str] = set()
    for part in parts:
        for token in TOKEN_RE.findall(part.lower()):
            if token in STOP_TOKENS or len(token) < 3:
                continue
            tokens.add(token)
            for subtoken in token.replace("_", "-").split("-"):
                if subtoken not in STOP_TOKENS and len(subtoken) >= 3:
                    tokens.add(subtoken)
    return tokens


def combined_record_text(record: dict[str, Any]) -> str:
    return "\n".join(
        [
            textify(record.get("scene")),
            textify(record.get("project_profile")),
            textify(record.get("doc_type")),
            textify(record.get("governance_problem")),
            textify(record.get("objective")),
            textify(record.get("what_worked")),
            textify(record.get("what_failed")),
            textify(record.get("local_fix_applied")),
            textify(record.get("remaining_risk")),
            textify(record.get("next_input")),
            textify(record.get("candidate_pattern_tags")),
            textify(record.get("candidate_failure_tags")),
        ]
    )


def score_record(
    record: dict[str, Any],
    policy: dict[str, Any],
    scene_counts: Counter[str],
    doc_type_counts: Counter[str],
    project_counts: Counter[str],
) -> tuple[int, dict[str, bool]]:
    pattern_tags = string_list(record.get("candidate_pattern_tags"))
    failure_tags = string_list(record.get("candidate_failure_tags"))
    repeat_signal = scene_counts[record.get("scene", "")] > 1 or doc_type_counts[record.get("doc_type", "")] > 1
    transfer_signal = len(set(pattern_tags + failure_tags)) >= 2
    specificity_signal = min(
        len(textify(record.get("what_worked"))),
        len(textify(record.get("local_fix_applied"))),
        len(textify(record.get("remaining_risk"))),
    ) >= 24
    future_judgment_signal = (
        len(textify(record.get("next_input"))) >= 24
        or any(
            keyword in combined_record_text(record).lower()
            for keyword in ["authority", "scope", "template", "audit", "check", "gate", "policy"]
        )
    )
    multi_project_signal = project_counts[record.get("project_profile", "")] > 1
    signals = {
        "repeat_signal": repeat_signal,
        "transfer_signal": transfer_signal,
        "specificity_signal": specificity_signal,
        "future_judgment_signal": future_judgment_signal,
        "multi_project_signal": multi_project_signal,
    }
    weights = policy.get("scoring", {})
    score = 0
    for key, enabled in signals.items():
        if enabled:
            score += int(weights.get(key, 1))
    return score, signals


def note_slug(record: dict[str, Any]) -> str:
    return slugify(f"{record.get('doc_type', '')}-{record.get('scene', '')}")


def render_field_note(record: dict[str, Any], score: int, signals: dict[str, bool], existing_sessions: list[str]) -> str:
    title = f"{record.get('doc_type', 'doc').replace('-', ' ').title()} - {record.get('scene', 'runtime note').replace('-', ' ').title()}"
    lines = [
        f"scene: {record.get('scene', '')}",
        f"doc_type: {record.get('doc_type', '')}",
        f"project_profile: {record.get('project_profile', '')}",
        f"promotion_score: {score}",
        f"source_session_ids: {', '.join(existing_sessions)}",
        "",
        f"# {title}",
        "",
        "## Governance Problem",
        "",
        sanitize_text(textify(record.get("governance_problem"))),
        "",
        "## What Worked",
        "",
        sanitize_text(textify(record.get("what_worked"))),
        "",
        "## What Failed",
        "",
        sanitize_text(textify(record.get("what_failed"))),
        "",
        "## Local Fix Applied",
        "",
        sanitize_text(textify(record.get("local_fix_applied"))),
        "",
        "## Remaining Risk",
        "",
        sanitize_text(textify(record.get("remaining_risk"))),
        "",
        "## Next Input",
        "",
        sanitize_text(textify(record.get("next_input"))),
        "",
        "## Promotion Signals",
        "",
    ]
    for key, enabled in signals.items():
        lines.append(f"- {key}: {'yes' if enabled else 'no'}")
    lines.extend(
        [
            "",
            "## Tags",
            "",
            f"- pattern_tags: {', '.join(string_list(record.get('candidate_pattern_tags'))) or 'none'}",
            f"- failure_tags: {', '.join(string_list(record.get('candidate_failure_tags'))) or 'none'}",
        ]
    )
    return "\n".join(lines) + "\n"


def render_repo_candidate(
    record: dict[str, Any],
    score: int,
    gate_count: int,
    source_note_slug: str,
    signals: dict[str, bool],
) -> str:
    title = f"Repo Candidate - {record.get('doc_type', 'doc').replace('-', ' ').title()} / {record.get('scene', '').replace('-', ' ').title()}"
    lines = [
        f"repo_candidate_slug: {slugify(f'{source_note_slug}-candidate')}",
        "review_status: pending",
        "review_reason: ",
        f"reviewed_at: ",
        f"source_note_slug: {source_note_slug}",
        f"scene: {record.get('scene', '')}",
        f"doc_type: {record.get('doc_type', '')}",
        f"project_profile: {record.get('project_profile', '')}",
        f"promotion_score: {score}",
        f"gate_count: {gate_count}",
        "",
        f"# {title}",
        "",
        "## Why This Stays Runtime-Safe",
        "",
        "- This file is a repo candidate only.",
        "- It does not contain raw runtime jsonl records.",
        "- It should be reviewed before any public repo change is drafted.",
        "",
        "## Candidate Pattern",
        "",
        sanitize_text(textify(record.get("what_worked"))),
        "",
        "## Candidate Failure Mode",
        "",
        sanitize_text(textify(record.get("what_failed"))),
        "",
        "## Potential Repo Impact",
        "",
        sanitize_text(textify(record.get("next_input"))),
        "",
        "## Signals",
        "",
    ]
    for key, enabled in signals.items():
        lines.append(f"- {key}: {'yes' if enabled else 'no'}")
    return "\n".join(lines) + "\n"


def detect_archive_reason(record: dict[str, Any], policy: dict[str, Any], score: int) -> str | None:
    text = combined_record_text(record).lower()
    for keyword in policy.get("archive_keywords", []):
        if keyword in text:
            return f"matched archive keyword '{keyword}'"
    if score <= int(policy.get("keep_raw_max_score", 1)):
        return "insufficient promotion score"
    return None


def gate_repo_candidate(record: dict[str, Any], signals: dict[str, bool]) -> tuple[int, dict[str, bool]]:
    abstraction_ready = bool(string_list(record.get("candidate_pattern_tags")) or string_list(record.get("candidate_failure_tags")))
    judgment_change = signals.get("future_judgment_signal", False)
    repeated = signals.get("repeat_signal", False)
    multi_project = signals.get("multi_project_signal", False)
    gate_signals = {
        "repeated": repeated,
        "multi_project": multi_project,
        "abstraction_ready": abstraction_ready,
        "judgment_change": judgment_change,
    }
    gate_count = sum(1 for enabled in gate_signals.values() if enabled)
    return gate_count, gate_signals


def upsert_note_stats(
    ledger: dict[str, Any],
    slug: str,
    *,
    session_id: str,
    action: str,
    note_path: str | None = None,
    repo_candidate_path: str | None = None,
) -> None:
    timestamp = datetime.now().astimezone().isoformat()
    stats = ledger.setdefault("note_stats", {}).setdefault(
        slug,
        {
            "source_session_ids": [],
            "reuse_count": 0,
            "merge_count": 0,
            "repo_candidate_paths": [],
            "last_action": None,
            "last_updated_at": None,
            "note_path": None,
        },
    )
    if session_id not in stats["source_session_ids"]:
        stats["source_session_ids"].append(session_id)
    if note_path:
        stats["note_path"] = note_path
    if repo_candidate_path and repo_candidate_path not in stats["repo_candidate_paths"]:
        stats["repo_candidate_paths"].append(repo_candidate_path)
    if action == "merge":
        stats["merge_count"] = int(stats.get("merge_count", 0)) + 1
    stats["last_action"] = action
    stats["last_updated_at"] = timestamp


def write_archive_note(runtime_root: Path, record: dict[str, Any], reason: str) -> str:
    slug = slugify(f"{record.get('doc_type', '')}-{record.get('scene', '')}-{record.get('session_id', '')}")
    path = runtime_root / "promoted" / "archive" / f"{slug}.md"
    content = "\n".join(
        [
            f"scene: {record.get('scene', '')}",
            f"doc_type: {record.get('doc_type', '')}",
            f"archive_reason: {reason}",
            "",
            f"# Archived Runtime Note - {record.get('scene', '')}",
            "",
            sanitize_text(textify(record.get("objective"))),
        ]
    )
    path.write_text(content + "\n", encoding="utf-8")
    return str(path)


def append_reviewed_history(queue: dict[str, Any], entry: dict[str, Any], max_history: int = 200) -> None:
    reviewed = queue.setdefault("reviewed", [])
    reviewed.append(entry)
    if len(reviewed) > max_history:
        queue["reviewed"] = reviewed[-max_history:]


def process_pending(runtime_root: Path, limit: int, trigger_source: str) -> dict[str, Any]:
    queue_path = runtime_root / "inbox" / "review-queue.json"
    policy_path = runtime_root / "state" / "promotion-policy.json"
    ledger_path = runtime_root / "state" / "promotion-ledger.json"
    trigger_history_path = runtime_root / "state" / "trigger-history.jsonl"

    queue = load_json(queue_path)
    policy = load_json(policy_path)
    ledger = load_json(ledger_path)
    pending = list(queue.get("pending", []))
    to_process = pending[:limit]
    remaining = pending[limit:]

    all_records = []
    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line in capture_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                all_records.append(json.loads(line))

    scene_counts = Counter(record.get("scene", "") for record in all_records)
    doc_type_counts = Counter(record.get("doc_type", "") for record in all_records)
    project_counts = Counter(record.get("project_profile", "") for record in all_records)

    run_id = datetime.now().astimezone().strftime("runtime-promotion-%Y%m%d%H%M%S")
    results = []

    for item in to_process:
        record = read_capture_record(Path(item["capture_file"]).expanduser(), item["session_id"])
        score, signals = score_record(record, policy, scene_counts, doc_type_counts, project_counts)
        archive_reason = detect_archive_reason(record, policy, score)
        reviewed_entry = {
            "session_id": record["session_id"],
            "scene": record["scene"],
            "doc_type": record["doc_type"],
            "timestamp": record["timestamp"],
            "score": score,
            "trigger_source": trigger_source,
        }

        if archive_reason:
            archive_path = write_archive_note(runtime_root, record, archive_reason)
            reviewed_entry["action"] = "archive"
            reviewed_entry["archive_path"] = archive_path
            append_reviewed_history(queue, reviewed_entry)
            results.append(reviewed_entry)
            continue

        slug = note_slug(record)
        note_path = runtime_root / "promoted" / "field-notes" / f"{slug}.md"
        note_exists = note_path.exists()
        stats = ledger.setdefault("note_stats", {}).get(slug, {})
        session_ids = list(stats.get("source_session_ids", []))
        if record["session_id"] not in session_ids:
            session_ids.append(record["session_id"])

        if score >= int(policy.get("promote_min_score", 2)):
            note_text = render_field_note(record, score, signals, session_ids)
            note_path.write_text(note_text, encoding="utf-8")
            action = "merge" if note_exists else "promote_to_field_note"
            upsert_note_stats(
                ledger,
                slug,
                session_id=record["session_id"],
                action=action,
                note_path=str(note_path),
            )
            reviewed_entry["action"] = action
            reviewed_entry["note_path"] = str(note_path)

            gate_count, gate_signals = gate_repo_candidate(record, signals)
            if score >= int(policy.get("repo_candidate_min_score", 3)) and gate_count >= int(
                policy.get("repo_candidate_gate_min", 2)
            ):
                candidate_slug = slugify(f"{slug}-candidate")
                candidate_path = runtime_root / "promoted" / "repo-candidates" / f"{candidate_slug}.md"
                candidate_text = render_repo_candidate(record, score, gate_count, slug, gate_signals)
                candidate_path.write_text(candidate_text, encoding="utf-8")
                reviewed_entry["repo_candidate_path"] = str(candidate_path)
                upsert_note_stats(
                    ledger,
                    slug,
                    session_id=record["session_id"],
                    action="repo_candidate",
                    note_path=str(note_path),
                    repo_candidate_path=str(candidate_path),
                )
                repo_stats = ledger.setdefault("repo_candidate_stats", {})
                repo_stats[candidate_slug] = {
                    "source_note_slug": slug,
                    "review_status": "pending",
                    "last_updated_at": datetime.now().astimezone().isoformat(),
                }
            append_reviewed_history(queue, reviewed_entry)
            results.append(reviewed_entry)
            continue

        reviewed_entry["action"] = "keep_raw"
        append_reviewed_history(queue, reviewed_entry)
        results.append(reviewed_entry)

    queue["pending"] = remaining
    write_json(queue_path, queue)

    ledger["updated_at"] = datetime.now().astimezone().isoformat()
    ledger["last_run_id"] = run_id
    ledger.setdefault("runs", []).append(
        {
            "run_id": run_id,
            "timestamp": ledger["updated_at"],
            "trigger_source": trigger_source,
            "processed": len(results),
            "remaining_pending": len(remaining),
        }
    )
    write_json(ledger_path, ledger)

    trigger_event = {
        "run_id": run_id,
        "timestamp": ledger["updated_at"],
        "trigger_source": trigger_source,
        "processed": len(results),
        "remaining_pending": len(remaining),
    }
    with trigger_history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(trigger_event, ensure_ascii=True) + "\n")

    return {
        "run_id": run_id,
        "processed": len(results),
        "remaining_pending": len(remaining),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Consume the local agent-doc runtime review queue.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    parser.add_argument("--limit", type=int, default=5, help="Maximum pending items to process.")
    parser.add_argument(
        "--trigger-source",
        default="manual",
        help="Identifier for this promotion cycle trigger.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    ensure_runtime_root(resolution.runtime_root, resolution)
    summary = process_pending(resolution.runtime_root, args.limit, args.trigger_source)
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
