from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SKILL_NAME = "agent-doc"
GLOBAL_RUNTIME_ROOT_ENV = "AGENT_DOC_RUNTIME_ROOT"
GLOBAL_HOST_ENV = "AGENT_DOC_HOST"

RUNTIME_SUBDIRS = [
    "captures",
    "index",
    "inbox",
    "promoted/field-notes",
    "promoted/repo-candidates",
    "promoted/archive",
    "state",
]

INDEX_FILES = {
    "index/by-scene.json": {},
    "index/by-doc-type.json": {},
    "index/by-failure-mode.json": {},
}

STATE_FILES = {
    "inbox/review-queue.json": {"pending": [], "reviewed": []},
    "state/manifest.json": {},
    "state/promotion-policy.json": {},
    "state/promotion-ledger.json": {},
    "state/reuse-ledger.json": {},
}

REQUIRED_CAPTURE_FIELDS = [
    "timestamp",
    "session_id",
    "host",
    "skill_name",
    "scene",
    "project_profile",
    "doc_type",
    "governance_problem",
    "objective",
    "artifacts_produced",
    "what_worked",
    "what_failed",
    "local_fix_applied",
    "remaining_risk",
    "next_input",
    "candidate_pattern_tags",
    "candidate_failure_tags",
    "promotion_hint",
]

PATH_REDACTION_PATTERNS = [
    re.compile(r"/Users/[^\s`]+"),
    re.compile(r"/home/[^\s`]+"),
    re.compile(r"[A-Za-z]:\\[^\s`]+"),
    re.compile(r"~/.codex/[^\s`]+"),
    re.compile(r"~/.claude/[^\s`]+"),
    re.compile(r"~/.openclaw/[^\s`]+"),
]


@dataclass(frozen=True)
class HostSpec:
    host_id: str
    display_name: str
    support_tier: str
    default_runtime_root: str
    home_env_var: str | None = None
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeResolution:
    host_id: str
    display_name: str
    support_tier: str
    runtime_root: Path
    source: str
    is_known_host: bool


HOST_SPECS = {
    "codex": HostSpec(
        host_id="codex",
        display_name="Codex",
        support_tier="reference_ready",
        default_runtime_root="~/.codex/skills/agent-doc/runtime",
        home_env_var="CODEX_HOME",
        aliases=("openai",),
    ),
    "claude-code": HostSpec(
        host_id="claude-code",
        display_name="Claude Code",
        support_tier="experimental",
        default_runtime_root="~/.claude/skills/agent-doc/runtime",
        home_env_var="CLAUDE_CODE_HOME",
        aliases=("claude", "claude_code"),
    ),
    "openclaw": HostSpec(
        host_id="openclaw",
        display_name="OpenClaw",
        support_tier="experimental",
        default_runtime_root="~/.openclaw/skills/agent-doc/runtime",
        home_env_var="OPENCLAW_HOME",
        aliases=("open-claw",),
    ),
}


def _host_env_key(host_id: str) -> str:
    return host_id.upper().replace("-", "_")


def normalize_host(host: str | None) -> str:
    if not host:
        return "codex"

    normalized = host.strip().lower().replace("_", "-")
    for spec in HOST_SPECS.values():
        if normalized == spec.host_id or normalized in spec.aliases:
            return spec.host_id
    return normalized


def resolve_runtime_resolution(
    host: str | None = None,
    root: str | Path | None = None,
    environ: dict[str, str] | None = None,
) -> RuntimeResolution:
    env = environ or os.environ
    normalized_host = normalize_host(host or env.get(GLOBAL_HOST_ENV))

    if root:
        spec = HOST_SPECS.get(normalized_host)
        return RuntimeResolution(
            host_id=normalized_host,
            display_name=spec.display_name if spec else normalized_host,
            support_tier=spec.support_tier if spec else "custom",
            runtime_root=Path(root).expanduser(),
            source="explicit_root",
            is_known_host=spec is not None,
        )

    explicit_root = env.get(GLOBAL_RUNTIME_ROOT_ENV)
    if explicit_root:
        spec = HOST_SPECS.get(normalized_host)
        return RuntimeResolution(
            host_id=normalized_host,
            display_name=spec.display_name if spec else normalized_host,
            support_tier=spec.support_tier if spec else "custom",
            runtime_root=Path(explicit_root).expanduser(),
            source=f"env:{GLOBAL_RUNTIME_ROOT_ENV}",
            is_known_host=spec is not None,
        )

    spec = HOST_SPECS.get(normalized_host)
    if spec is None:
        raise ValueError(
            "unknown host requires --root or AGENT_DOC_RUNTIME_ROOT: "
            f"{normalized_host}"
        )

    host_runtime_env = f"AGENT_DOC_{_host_env_key(normalized_host)}_RUNTIME_ROOT"
    if env.get(host_runtime_env):
        return RuntimeResolution(
            host_id=spec.host_id,
            display_name=spec.display_name,
            support_tier=spec.support_tier,
            runtime_root=Path(env[host_runtime_env]).expanduser(),
            source=f"env:{host_runtime_env}",
            is_known_host=True,
        )

    if spec.home_env_var and env.get(spec.home_env_var):
        runtime_root = Path(env[spec.home_env_var]).expanduser() / "skills" / SKILL_NAME / "runtime"
        return RuntimeResolution(
            host_id=spec.host_id,
            display_name=spec.display_name,
            support_tier=spec.support_tier,
            runtime_root=runtime_root,
            source=f"env:{spec.home_env_var}",
            is_known_host=True,
        )

    return RuntimeResolution(
        host_id=spec.host_id,
        display_name=spec.display_name,
        support_tier=spec.support_tier,
        runtime_root=Path(spec.default_runtime_root).expanduser(),
        source=f"default:{spec.host_id}",
        is_known_host=True,
    )


def parse_runtime_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return parsed.astimezone()


def sanitize_text(value: str) -> str:
    sanitized = value
    for pattern in PATH_REDACTION_PATTERNS:
        sanitized = pattern.sub("[redacted-path]", sanitized)
    return sanitized


def sanitize_capture_record(record: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in record.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_text(value)
        elif isinstance(value, list):
            cleaned = []
            for item in value:
                if isinstance(item, str):
                    cleaned.append(sanitize_text(item))
                else:
                    cleaned.append(item)
            sanitized[key] = cleaned
        elif isinstance(value, dict):
            sanitized[key] = {
                nested_key: sanitize_text(nested_value)
                if isinstance(nested_value, str)
                else nested_value
                for nested_key, nested_value in value.items()
            }
        else:
            sanitized[key] = value
    return sanitized


def enrich_capture_record(record: dict[str, Any], resolution: RuntimeResolution) -> dict[str, Any]:
    enriched = sanitize_capture_record(record)
    enriched.setdefault("skill_name", SKILL_NAME)
    enriched.setdefault("host", resolution.host_id)
    enriched.setdefault("runtime_host", resolution.host_id)
    enriched.setdefault("runtime_host_display_name", resolution.display_name)
    enriched.setdefault("runtime_host_support_tier", resolution.support_tier)
    enriched.setdefault("runtime_root_source", resolution.source)
    return enriched


def default_manifest(runtime_root: Path, resolution: RuntimeResolution | None = None) -> dict[str, Any]:
    manifest = {
        "version": 1,
        "skill_name": SKILL_NAME,
        "created_at": datetime.now().astimezone().isoformat(),
        "runtime_root_contract": "local_first_non_repo_default",
        "public_repo_boundary": "raw_runtime_data_never_auto_published",
        "capture_privacy_rule": "redact_private_paths_and_private_project_context",
        "promotion_policy_file": "state/promotion-policy.json",
        "trigger_history_file": "state/trigger-history.jsonl",
    }
    if resolution is not None:
        manifest.update(
            {
                "runtime_host": resolution.host_id,
                "runtime_host_display_name": resolution.display_name,
                "runtime_host_support_tier": resolution.support_tier,
                "runtime_root_resolution_source": resolution.source,
            }
        )
    return manifest


def default_promotion_policy() -> dict[str, Any]:
    return {
        "version": 1,
        "review_queue_backlog_threshold": 10,
        "default_batch_size": 5,
        "promoted_working_set_ceiling": 20,
        "max_recent_capture_reads": 5,
        "max_promoted_note_reads": 3,
        "max_reference_reads": 2,
        "keep_raw_max_score": 1,
        "promote_min_score": 2,
        "repo_candidate_min_score": 3,
        "repo_candidate_gate_min": 2,
        "dedup_merge_same_slug": True,
        "archive_keywords": [
            "smoke-only",
            "demo only",
            "synthetic-only",
            "temporary cli sample",
        ],
        "scoring": {
            "repeat_signal": 1,
            "transfer_signal": 1,
            "specificity_signal": 1,
            "future_judgment_signal": 1,
        },
        "notes": "Runtime stays local. Repo candidates remain pending until explicit review.",
    }


def default_promotion_ledger() -> dict[str, Any]:
    return {
        "version": 1,
        "created_at": datetime.now().astimezone().isoformat(),
        "updated_at": None,
        "last_run_id": None,
        "runs": [],
        "note_stats": {},
        "repo_candidate_stats": {},
    }


def default_reuse_ledger() -> dict[str, Any]:
    return {
        "version": 1,
        "created_at": datetime.now().astimezone().isoformat(),
        "updated_at": None,
        "events": [],
        "note_hits": {},
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _merge_missing_defaults(existing: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    for key, value in defaults.items():
        if key not in merged:
            merged[key] = value
            continue
        if isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_missing_defaults(merged[key], value)
    return merged


def ensure_runtime_root(runtime_root: Path, resolution: RuntimeResolution | None = None) -> dict[str, Any]:
    runtime_root = runtime_root.expanduser()
    created: list[str] = []
    for subdir in RUNTIME_SUBDIRS:
        path = runtime_root / subdir
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))

    for rel_path, payload in INDEX_FILES.items():
        file_path = runtime_root / rel_path
        if not file_path.exists():
            write_json(file_path, payload)

    for rel_path, payload in STATE_FILES.items():
        file_path = runtime_root / rel_path
        if rel_path == "state/manifest.json":
            payload = default_manifest(runtime_root, resolution)
        elif rel_path == "state/promotion-policy.json":
            payload = default_promotion_policy()
        elif rel_path == "state/promotion-ledger.json":
            payload = default_promotion_ledger()
        elif rel_path == "state/reuse-ledger.json":
            payload = default_reuse_ledger()

        if not file_path.exists():
            write_json(file_path, payload)
            continue

        try:
            existing = load_json(file_path)
        except json.JSONDecodeError:
            continue
        if isinstance(existing, dict) and isinstance(payload, dict):
            merged = _merge_missing_defaults(existing, payload)
            if merged != existing:
                write_json(file_path, merged)

    trigger_history = runtime_root / "state" / "trigger-history.jsonl"
    if not trigger_history.exists():
        trigger_history.write_text("", encoding="utf-8")

    readme_path = runtime_root / "README.md"
    if not readme_path.exists():
        lines = [
            "# agent-doc Runtime",
            "",
            "This directory stores local runtime captures, light indexes, review queue, promoted notes, and repo candidates for agent-doc.",
            "",
            "- This runtime layer is local-first.",
            "- The repository working copy is not the default runtime root.",
            "- Raw runtime data must not be written back into the public repository automatically.",
        ]
        if resolution is not None:
            lines.extend(
                [
                    "",
                    f"- Host: `{resolution.display_name}`",
                    f"- Support tier: `{resolution.support_tier}`",
                    f"- Resolution source: `{resolution.source}`",
                ]
            )
        readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "runtime_root": str(runtime_root),
        "runtime_host": resolution.host_id if resolution else None,
        "runtime_root_source": resolution.source if resolution else None,
        "created": created,
    }


def validate_capture(record: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_CAPTURE_FIELDS if field not in record]
    if missing:
        raise ValueError(f"capture record missing required fields: {', '.join(missing)}")

    parse_runtime_timestamp(record["timestamp"])

    if record.get("skill_name") != SKILL_NAME:
        raise ValueError(f"skill_name must be '{SKILL_NAME}'")

    if not isinstance(record.get("artifacts_produced"), list):
        raise ValueError("artifacts_produced must be a list")
    if not isinstance(record.get("candidate_pattern_tags"), list):
        raise ValueError("candidate_pattern_tags must be a list")
    if not isinstance(record.get("candidate_failure_tags"), list):
        raise ValueError("candidate_failure_tags must be a list")

    for key in [
        "scene",
        "project_profile",
        "doc_type",
        "governance_problem",
        "objective",
        "what_worked",
        "what_failed",
        "local_fix_applied",
        "remaining_risk",
        "next_input",
    ]:
        value = record.get(key, "")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")

    for key in [
        "objective",
        "what_worked",
        "what_failed",
        "local_fix_applied",
        "remaining_risk",
        "next_input",
    ]:
        value = record.get(key, "")
        if value != sanitize_text(value):
            raise ValueError(f"{key} must not include private absolute paths")


def _update_index(index_path: Path, key: str, record: dict[str, Any]) -> None:
    if not key:
        return
    index = load_json(index_path)
    entry = index.setdefault(
        key,
        {
            "count": 0,
            "latest_timestamp": None,
            "latest_session_id": None,
        },
    )
    entry["count"] += 1
    entry["latest_timestamp"] = record["timestamp"]
    entry["latest_session_id"] = record["session_id"]
    write_json(index_path, index)


def append_capture(runtime_root: Path, record: dict[str, Any]) -> Path:
    runtime_root = runtime_root.expanduser()
    validate_capture(record)
    timestamp = parse_runtime_timestamp(record["timestamp"])
    capture_file = runtime_root / "captures" / f"{timestamp.date().isoformat()}.jsonl"
    with capture_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")

    _update_index(runtime_root / "index" / "by-scene.json", record["scene"], record)
    _update_index(runtime_root / "index" / "by-doc-type.json", record["doc_type"], record)
    for tag in record.get("candidate_failure_tags", []):
        _update_index(runtime_root / "index" / "by-failure-mode.json", tag, record)

    if record.get("promotion_hint") != "raw_only":
        queue_path = runtime_root / "inbox" / "review-queue.json"
        queue = load_json(queue_path)
        queue.setdefault("pending", []).append(
            {
                "capture_file": str(capture_file),
                "session_id": record["session_id"],
                "scene": record["scene"],
                "doc_type": record["doc_type"],
                "project_profile": record["project_profile"],
                "promotion_hint": record["promotion_hint"],
                "timestamp": record["timestamp"],
            }
        )
        write_json(queue_path, queue)

    return capture_file


def iter_capture_records(runtime_root: Path) -> list[dict[str, Any]]:
    runtime_root = runtime_root.expanduser()
    records: list[dict[str, Any]] = []
    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line in capture_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            records.append(json.loads(line))
    return records


def read_capture_record(capture_file: Path, session_id: str) -> dict[str, Any]:
    for line in capture_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("session_id") == session_id:
            return record
    raise ValueError(f"capture {session_id} not found in {capture_file}")


def read_recent_captures(
    runtime_root: Path,
    *,
    scene: str | None = None,
    doc_type: str | None = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    runtime_root = runtime_root.expanduser()
    records: list[dict[str, Any]] = []
    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl"), reverse=True):
        lines = capture_file.read_text(encoding="utf-8").splitlines()
        for line in reversed(lines):
            if not line.strip():
                continue
            record = json.loads(line)
            if scene and record.get("scene") != scene:
                continue
            if doc_type and record.get("doc_type") != doc_type:
                continue
            records.append(record)
            if len(records) >= limit:
                return records
    return records


def _extract_metadata_from_note(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            if metadata:
                break
            continue
        if ":" not in line:
            if metadata:
                break
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def read_promoted_field_notes(
    runtime_root: Path,
    *,
    scene: str | None = None,
    doc_type: str | None = None,
    limit: int = 3,
) -> list[dict[str, Any]]:
    runtime_root = runtime_root.expanduser()
    notes: list[dict[str, Any]] = []
    for note_path in sorted((runtime_root / "promoted" / "field-notes").glob("*.md"), reverse=True):
        text = note_path.read_text(encoding="utf-8")
        metadata = _extract_metadata_from_note(text)
        if scene and metadata.get("scene") != scene:
            continue
        if doc_type and metadata.get("doc_type") != doc_type:
            continue
        title = note_path.stem.replace("-", " ")
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        excerpt_lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.startswith("#") and ":" not in line[:40]
        ]
        notes.append(
            {
                "slug": note_path.stem,
                "path": str(note_path),
                "title": title,
                "scene": metadata.get("scene"),
                "doc_type": metadata.get("doc_type"),
                "excerpt": " ".join(excerpt_lines[:3])[:220],
            }
        )
        if len(notes) >= limit:
            break
    return notes


def record_promoted_note_reuse(
    runtime_root: Path,
    promoted_notes: list[dict[str, Any]],
    *,
    scene: str | None = None,
    doc_type: str | None = None,
    source: str = "read_runtime_context",
) -> dict[str, Any]:
    runtime_root = runtime_root.expanduser()
    if not promoted_notes:
        return {"recorded": 0, "events": []}

    reuse_ledger_path = runtime_root / "state" / "reuse-ledger.json"
    promotion_ledger_path = runtime_root / "state" / "promotion-ledger.json"
    reuse_ledger = load_json(reuse_ledger_path)
    promotion_ledger = load_json(promotion_ledger_path)
    note_stats = promotion_ledger.setdefault("note_stats", {})

    timestamp = datetime.now().astimezone().isoformat()
    events = []
    for note in promoted_notes:
        slug = note["slug"]
        event = {
            "timestamp": timestamp,
            "source": source,
            "scene": scene,
            "doc_type": doc_type,
            "note_slug": slug,
        }
        events.append(event)
        hit = reuse_ledger.setdefault("note_hits", {}).setdefault(
            slug,
            {"count": 0, "last_hit_at": None, "scenes": [], "doc_types": [], "sources": []},
        )
        hit["count"] += 1
        hit["last_hit_at"] = timestamp
        if scene and scene not in hit["scenes"]:
            hit["scenes"].append(scene)
        if doc_type and doc_type not in hit["doc_types"]:
            hit["doc_types"].append(doc_type)
        if source not in hit["sources"]:
            hit["sources"].append(source)

        stat = note_stats.setdefault(
            slug,
            {
                "reuse_count": 0,
                "last_action": None,
                "last_updated_at": timestamp,
                "source_session_ids": [],
                "repo_candidate_paths": [],
            },
        )
        stat["reuse_count"] = int(stat.get("reuse_count", 0)) + 1
        stat["last_action"] = "reused"
        stat["last_updated_at"] = timestamp

    reuse_ledger.setdefault("events", []).extend(events)
    reuse_ledger["updated_at"] = timestamp
    promotion_ledger["updated_at"] = timestamp
    write_json(reuse_ledger_path, reuse_ledger)
    write_json(promotion_ledger_path, promotion_ledger)
    return {"recorded": len(events), "events": events}


def validate_runtime_root(runtime_root: Path) -> list[str]:
    runtime_root = runtime_root.expanduser()
    errors: list[str] = []

    for subdir in RUNTIME_SUBDIRS:
        path = runtime_root / subdir
        if not path.exists() or not path.is_dir():
            errors.append(f"missing directory: {path}")

    required_files = [
        runtime_root / "index" / "by-scene.json",
        runtime_root / "index" / "by-doc-type.json",
        runtime_root / "index" / "by-failure-mode.json",
        runtime_root / "inbox" / "review-queue.json",
        runtime_root / "state" / "manifest.json",
        runtime_root / "state" / "promotion-policy.json",
        runtime_root / "state" / "promotion-ledger.json",
        runtime_root / "state" / "reuse-ledger.json",
        runtime_root / "state" / "trigger-history.jsonl",
    ]

    for path in required_files:
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid json in {path}: {exc}")

    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line_no, line in enumerate(capture_file.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                validate_capture(json.loads(line))
            except Exception as exc:  # noqa: BLE001
                errors.append(f"invalid capture in {capture_file}:{line_no}: {exc}")

    return errors
