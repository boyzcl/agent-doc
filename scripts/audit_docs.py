#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


ENTRY_CANDIDATES = [
    "AGENTS.md",
    "CLAUDE.md",
    "ROOT_AGENT.md",
    "README.md",
    "docs/index.md",
    "docs/README.md",
]

HISTORY_HINTS = ("history", "archive", "legacy")
EVIDENCE_HINTS = ("evidence", "report", "reports", "artifact", "artifacts", "reference")
BOUNDARY_WORDS = ("历史", "证据", "archive", "history", "evidence", "current")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def existing_entries(root: Path) -> list[str]:
    return [rel for rel in ENTRY_CANDIDATES if (root / rel).exists()]


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def authority_map_path(root: Path) -> Path:
    return root / "docs" / "authority-map.md"


def audit_entrypoint_competition(root: Path, findings: list[dict]):
    entries = existing_entries(root)
    if len(entries) >= 4:
        findings.append(
            {
                "severity": "warning",
                "category": "entrypoint-competition",
                "summary": "发现多个根入口候选，项目可能存在入口竞争。",
                "details": f"发现的入口候选: {', '.join(entries)}",
            }
        )

    if len(entries) > 1 and not authority_map_path(root).exists():
        findings.append(
            {
                "severity": "error",
                "category": "authority-missing",
                "summary": "项目存在多个入口候选，但缺少 authority map。",
                "details": f"发现的入口候选: {', '.join(entries)}",
            }
        )


def audit_authority_map(root: Path, findings: list[dict]):
    path = authority_map_path(root)
    if not path.exists():
        return

    text = read_text(path)
    required_sections = [
        "## Navigation Register",
        "## Topic Register",
        "## Conflict Rules",
        "## Evidence Boundaries",
    ]
    missing = [section for section in required_sections if section not in text]
    if missing:
        findings.append(
            {
                "severity": "error",
                "category": "authority-structure",
                "summary": "authority map 结构不完整。",
                "details": f"缺失区块: {', '.join(missing)}",
            }
        )

    topic_header = "| Topic | Canonical Doc | Doc Role | Scope | Status | History Docs | Evidence Docs | Conflict Rule |"
    if topic_header not in text:
        findings.append(
            {
                "severity": "error",
                "category": "authority-structure",
                "summary": "authority map 缺少标准化 Topic Register 表头。",
                "details": "建议使用半结构化表格字段，而不是自由叙述。",
            }
        )

    if not re.search(
        r"^-\s*evidence_is_not_default_rule_source:\s*yes\s*$",
        text,
        re.MULTILINE,
    ):
        findings.append(
            {
                "severity": "warning",
                "category": "evidence-boundary",
                "summary": "authority map 没有明确声明 evidence 默认不是规则来源。",
                "details": "建议在 Evidence Boundaries 中显式写出 evidence_is_not_default_rule_source: yes。",
            }
        )

    suspicious_rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8 or cells[0] in {"Topic", "---"}:
            continue
        canonical_doc = cells[1].lower()
        if any(hint in canonical_doc for hint in EVIDENCE_HINTS):
            suspicious_rows.append(line)
    if suspicious_rows:
        findings.append(
            {
                "severity": "warning",
                "category": "history-evidence-confusion",
                "summary": "authority map 中存在疑似把证据目录当 canonical doc 的行。",
                "details": "\n".join(suspicious_rows[:3]),
            }
        )


def audit_history_evidence_confusion(root: Path, findings: list[dict]):
    suspicious_links = []
    for rel in existing_entries(root):
        path = root / rel
        text = read_text(path)
        has_boundary_words = any(word in text.lower() for word in BOUNDARY_WORDS)
        for link in markdown_links(text):
            clean = link.split("#", 1)[0]
            lowered = clean.lower()
            if any(hint in lowered for hint in HISTORY_HINTS + EVIDENCE_HINTS):
                if not has_boundary_words:
                    suspicious_links.append(f"{rel} -> {clean}")

    if suspicious_links:
        findings.append(
            {
                "severity": "warning",
                "category": "history-evidence-confusion",
                "summary": "入口文档直接链接到历史或证据目录，但没有显式边界说明。",
                "details": "\n".join(suspicious_links[:8]),
            }
        )

    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix().lower()
        if not any(hint in rel for hint in HISTORY_HINTS + EVIDENCE_HINTS):
            continue
        text = read_text(path)
        if re.search(r"^Source of Truth\s*[:：]\s*yes\s*$", text, re.MULTILINE):
            findings.append(
                {
                    "severity": "warning",
                    "category": "history-evidence-confusion",
                    "summary": "历史或证据类文档被标记为 Source of Truth: yes。",
                    "details": path.relative_to(root).as_posix(),
                }
            )


def render_report(root: Path, findings: list[dict]) -> str:
    status = "pass" if not findings else "needs-attention"
    lines = [
        "# agent-doc audit report",
        "",
        f"- root: `{root}`",
        f"- status: `{status}`",
        f"- findings: `{len(findings)}`",
        "",
    ]
    if not findings:
        lines.extend(
            [
                "## Summary",
                "",
                "未发现明显的入口竞争、authority 缺失或 history/evidence 混淆信号。",
            ]
        )
        return "\n".join(lines) + "\n"

    lines.extend(["## Findings", ""])
    for index, finding in enumerate(findings, start=1):
        lines.append(f"{index}. [{finding['severity']}] {finding['category']} - {finding['summary']}")
        lines.append(f"   {finding['details']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a project for documentation governance gaps.")
    parser.add_argument("--root", required=True, help="Project root to audit")
    parser.add_argument("--output", help="Optional markdown report output path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings: list[dict] = []

    audit_entrypoint_competition(root, findings)
    audit_authority_map(root, findings)
    audit_history_evidence_confusion(root, findings)

    report = render_report(root, findings)
    sys.stdout.write(report)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")

    return 1 if any(item["severity"] == "error" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
