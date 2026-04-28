#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from runtime_memory_lib import append_capture, ensure_runtime_root, enrich_capture_record, resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Append one agent-doc runtime capture record.")
    parser.add_argument("--record-file", required=True, help="Path to a JSON file containing one capture record.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    parser.add_argument(
        "--run-promotion",
        action="store_true",
        help="After writing the capture, run one bounded local promotion cycle.",
    )
    parser.add_argument("--promotion-limit", type=int, default=1, help="Max pending items to process.")
    args = parser.parse_args()

    record_path = Path(args.record_file).expanduser()
    record = json.loads(record_path.read_text(encoding="utf-8"))
    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    ensure_runtime_root(resolution.runtime_root, resolution)
    capture = enrich_capture_record(record, resolution)
    capture_path = append_capture(resolution.runtime_root, capture)

    if args.run_promotion:
        command = [
            sys.executable,
            str(Path(__file__).with_name("promotion_worker.py")),
            "--root",
            str(resolution.runtime_root),
            "--limit",
            str(args.promotion_limit),
            "--trigger-source",
            "write_runtime_capture",
        ]
        if args.host:
            command.extend(["--host", args.host])
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.stdout.strip():
            print(completed.stdout.strip(), file=sys.stderr)
        if completed.stderr.strip():
            print(completed.stderr.strip(), file=sys.stderr)
        if completed.returncode != 0:
            return completed.returncode

    print(capture_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
