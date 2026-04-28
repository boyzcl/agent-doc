Title: Minimal Project Authority Map
Type: authority-map
Layer: standard
Mode: reference
Scope: repo
Status: active
Owner: docs-owner
Source of Truth: yes
Related Files: AGENTS.md ; README.md ; docs/conventions/release-policy.md ; docs/runbooks/release-smoke.md

# Minimal Project Authority Map

## Purpose

这份文档用于声明当前发布主题谁说了算，哪些材料只是历史背景或证据目录。

## Navigation Register

| Entry | Role | Default Use | Notes |
| --- | --- | --- | --- |
| `AGENTS.md` | Agent 控制入口 | yes | 改动前优先读取 |
| `README.md` | 项目总入口 | yes | 首次进入项目先看这里 |
| `docs/index.md` | 文档索引 | yes | 负责 current / history / evidence 分层 |

## Topic Register

| Topic | Canonical Doc | Doc Role | Scope | Status | History Docs | Evidence Docs | Conflict Rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Release Rules` | `docs/conventions/release-policy.md` | `current-rule` | `repo` | `active` | `docs/history/release-evolution.md` | `docs/reference/evidence-catalog.md` | `runbook` 负责执行步骤，但不能取代 `canonical doc` |
| `Release Smoke` | `docs/runbooks/release-smoke.md` | `runbook` | `repo` | `active` | `docs/history/release-evolution.md` | `docs/reference/evidence-catalog.md` | 操作步骤冲突时以 `Release Rules` 的主文档约束为准 |

## Conflict Rules
1. 最近作用域的入口文档优先
2. `Canonical Doc` 优先于辅助文档
3. `History Docs` 与 `Evidence Docs` 默认不参与当前规则竞争

## Evidence Boundaries
- evidence_dirs: `docs/reference/`
- evidence_usage: 支持判断、链接实验或观察记录
- evidence_is_not_default_rule_source: yes

## Review Notes
- 如果未来新增第二套发布流程，先扩写 authority map，再补文档
