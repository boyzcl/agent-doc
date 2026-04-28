Title: [Project Authority Map]
Type: authority-map
Layer: standard
Mode: reference
Scope: [repo or subsystem]
Status: active
Owner: [team or role]
Source of Truth: yes
Related Files: [key docs and directories]

# [Project] Authority Map

## Purpose
[说明哪些文档负责当前规则，哪些只负责背景或证据。]

## Navigation Register

| Entry | Role | Default Use | Notes |
| --- | --- | --- | --- |
| `[root agent doc]` | Agent 控制入口 | yes | [说明] |
| `README.md` | 项目总入口 | yes | [说明] |
| `docs/index.md` | 文档索引 | yes | [说明] |

## Topic Register

| Topic | Canonical Doc | Doc Role | Scope | Status | History Docs | Evidence Docs | Conflict Rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `[Topic A]` | `[path]` | `current-rule` | `[scope]` | `active` | `[path or none]` | `[path or none]` | `[rule]` |
| `[Topic B]` | `[path]` | `runbook` | `[scope]` | `active` | `[path or none]` | `[path or none]` | `[rule]` |

## Conflict Rules
1. 最近作用域的根入口或局部入口文档
2. `Canonical Doc` 优先于辅助文档
3. 当前 runbook 或操作性文档不能取代主题主文档
4. 历史背景和证据目录默认不参与当前规则竞争

## Evidence Boundaries
- evidence_dirs:
- evidence_usage:
- evidence_is_not_default_rule_source: yes

## Review Notes
- [待补边界]
