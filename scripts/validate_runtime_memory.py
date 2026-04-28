#!/usr/bin/env python3

from __future__ import annotations

import argparse

from runtime_memory_lib import resolve_runtime_resolution, validate_runtime_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate agent-doc runtime memory structure.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    errors = validate_runtime_root(resolution.runtime_root)
    if errors:
        for error in errors:
            print(error)
        return 1

    print(
        "runtime memory is valid: "
        f"{resolution.runtime_root} "
        f"(host={resolution.host_id}, source={resolution.source}, tier={resolution.support_tier})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
