#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    scripts_dir = repo_root / "scripts"

    with tempfile.TemporaryDirectory(prefix="agent-doc-runtime-") as temp_dir:
        runtime_root = Path(temp_dir)

        steps = [
            [
                sys.executable,
                str(scripts_dir / "init_runtime_memory.py"),
                "--host",
                "claude-code",
                "--root",
                str(runtime_root),
            ]
        ]
        for command in steps:
            completed = run(command)
            if completed.returncode != 0:
                sys.stderr.write(completed.stdout)
                sys.stderr.write(completed.stderr)
                return completed.returncode

        record_path = runtime_root / "sample-capture.json"
        record_path.write_text(
            json.dumps(
                {
                    "timestamp": datetime.now().astimezone().isoformat(),
                    "session_id": "smoke-test-session",
                    "host": "claude-code",
                    "skill_name": "agent-doc",
                    "scene": "brownfield-retrofit",
                    "project_profile": "existing-product-docs",
                    "doc_type": "authority-map",
                    "governance_problem": "multiple entry docs compete for current guidance",
                    "objective": "verify runtime capture, promotion, and retrieval",
                    "artifacts_produced": ["authority-map.md", "docs/index.md"],
                    "what_worked": "repairing the entry layer before content expansion reduced routing ambiguity",
                    "what_failed": "reading history notes as current rules kept causing drift",
                    "local_fix_applied": "split current rules, history context, and evidence references",
                    "remaining_risk": "repo candidate still needs explicit human review before public drafting",
                    "next_input": "reuse this note when another brownfield authority-map repair request appears",
                    "candidate_pattern_tags": ["entry-layer", "authority-map"],
                    "candidate_failure_tags": ["history-evidence-confusion"],
                    "promotion_hint": "review_for_repo_candidate",
                },
                ensure_ascii=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        commands = [
            [
                sys.executable,
                str(scripts_dir / "write_runtime_capture.py"),
                "--host",
                "claude-code",
                "--root",
                str(runtime_root),
                "--record-file",
                str(record_path),
            ],
            [
                sys.executable,
                str(scripts_dir / "validate_runtime_memory.py"),
                "--host",
                "claude-code",
                "--root",
                str(runtime_root),
            ],
            [
                sys.executable,
                str(scripts_dir / "read_runtime_context.py"),
                "--host",
                "claude-code",
                "--root",
                str(runtime_root),
                "--scene",
                "brownfield-retrofit",
                "--doc-type",
                "authority-map",
                "--limit",
                "1",
            ],
            [
                sys.executable,
                str(scripts_dir / "promotion_worker.py"),
                "--host",
                "claude-code",
                "--root",
                str(runtime_root),
                "--limit",
                "1",
                "--trigger-source",
                "smoke_test_runtime_memory",
            ],
            [
                sys.executable,
                str(scripts_dir / "runtime_governance_report.py"),
                "--host",
                "claude-code",
                "--root",
                str(runtime_root),
                "--json",
            ],
        ]

        outputs: list[str] = []
        for command in commands:
            completed = run(command)
            outputs.append(completed.stdout.strip())
            if completed.returncode != 0:
                sys.stderr.write(completed.stdout)
                sys.stderr.write(completed.stderr)
                return completed.returncode

        read_payload = json.loads(outputs[2])
        if not read_payload or read_payload[0]["session_id"] != "smoke-test-session":
            print("failed to retrieve the just-written runtime capture")
            return 1

        governance = json.loads(outputs[4])
        if governance["field_note_count"] < 1:
            print("promotion worker did not produce a field note during smoke test")
            return 1

        print(f"smoke test passed: {runtime_root} (host=claude-code)")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
