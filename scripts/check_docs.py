#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def iter_markdown_files(root: Path, ignore_paths: list[str]):
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        if any(rel.startswith(prefix) for prefix in ignore_paths):
            continue
        yield path, rel


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(root: Path, config: dict, errors: list[str]):
    for rel in config.get("required_files", []):
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    for group in config.get("required_one_of", []):
        name = group.get("name", "unnamed-group")
        paths = group.get("paths", [])
        if not any((root / rel).exists() for rel in paths):
            errors.append(f"missing one of required file group '{name}': {', '.join(paths)}")


def check_metadata(rel: str, text: str, config: dict, errors: list[str]):
    head = "\n".join(text.splitlines()[:30])
    for rule in config.get("metadata_rules", []):
        if not re.search(rule["match"], rel):
            continue

        for field in rule.get("required_fields", []):
            if not re.search(rf"^{re.escape(field)}\s*[:：]\s*.+$", head, re.MULTILINE):
                errors.append(f"{rel}: missing metadata field '{field}'")

        for field, allowed in rule.get("allowed_values", {}).items():
            match = re.search(
                rf"^{re.escape(field)}\s*[:：]\s*(.+)$",
                head,
                re.MULTILINE,
            )
            if not match:
                continue
            value = match.group(1).strip()
            if value not in allowed:
                errors.append(
                    f"{rel}: invalid value '{value}' for '{field}', allowed: {', '.join(allowed)}"
                )


def check_sections(rel: str, text: str, config: dict, errors: list[str]):
    for rule in config.get("section_rules", []):
        if not re.search(rule["match"], rel):
            continue
        for section in rule.get("required_sections", []):
            if section not in text:
                errors.append(f"{rel}: missing required section '{section}'")


def check_line_limits(rel: str, text: str, config: dict, warnings: list[str]):
    line_count = len(text.splitlines())
    for rule in config.get("line_limits", []):
        if not re.search(rule["match"], rel):
            continue
        limit = int(rule["warn_if_over"])
        if line_count > limit:
            warnings.append(f"{rel}: {line_count} lines exceeds warning limit {limit}")
        break


def check_links(root: Path, rel: str, text: str, errors: list[str]):
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    current_dir = (root / rel).parent
    for target in links:
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = unquote(target.split("#", 1)[0])
        if not clean:
            continue
        resolved = (current_dir / clean).resolve()
        if not resolved.exists():
            errors.append(f"{rel}: broken relative link -> {clean}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check minimal documentation governance rules.")
    parser.add_argument("--root", required=True, help="Root directory to check")
    parser.add_argument("--config", required=True, help="JSON policy file")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    errors: list[str] = []
    warnings: list[str] = []

    check_required_files(root, config, errors)

    for path, rel in iter_markdown_files(root, config.get("ignore_paths", [])):
        text = read_text(path)
        check_metadata(rel, text, config, errors)
        check_sections(rel, text, config, errors)
        check_line_limits(rel, text, config, warnings)
        check_links(root, rel, text, errors)

    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s) and {len(warnings)} warning(s).")
        return 1

    print(f"PASSED with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
