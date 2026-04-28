# Authority Map 字段规范

为了让 authority map 更适合 Agent 读取、人工维护和脚本审计，推荐使用半结构化表格，而不是全自由叙述。

## 1. 最小结构

一份 authority map 建议包含：

1. metadata 头部
2. `## Navigation Register`
3. `## Topic Register`
4. `## Conflict Rules`
5. `## Evidence Boundaries`
6. `## Review Notes`

## 2. Navigation Register

用来声明入口角色和主次关系。

推荐列：

| Entry | Role | Default Use | Notes |
| --- | --- | --- | --- |
| `README.md` | 项目总入口 | yes | 面向人和 Agent 的第一站 |

字段含义：
- `Entry`: 入口文件或入口集
- `Role`: 它承担什么角色
- `Default Use`: 是否默认从这里进入
- `Notes`: 例外或边界说明

## 3. Topic Register

这是 authority map 的核心表。

推荐列：

| Topic | Canonical Doc | Doc Role | Scope | Status | History Docs | Evidence Docs | Conflict Rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 发布规则 | `docs/conventions/release-policy.md` | current-rule | repo | active | `docs/history/release-evolution.md` | `docs/reference/evidence-catalog.md` | `runbook` 不能取代 `canonical doc` |

字段含义：
- `Topic`: 主题名
- `Canonical Doc`: 当前主文档
- `Doc Role`: 建议值如 `current-rule`、`runbook`、`design-authority`、`reference-authority`
- `Scope`: 作用域
- `Status`: 当前状态
- `History Docs`: 历史背景入口
- `Evidence Docs`: 证据目录入口
- `Conflict Rule`: 冲突时如何判定

## 4. Conflict Rules

这里写全局优先级，不复制主题内容。

推荐至少写：
1. 最近作用域的入口文档优先
2. `Canonical Doc` 优先于辅助文档
3. `History Docs` 与 `Evidence Docs` 默认不参与当前规则竞争

## 5. Evidence Boundaries

推荐最少字段：
- `evidence_dirs`
- `evidence_usage`
- `evidence_is_not_default_rule_source`

## 6. 设计原则

- 优先用表，不优先写长段解释
- 一行只表达一个主题 authority
- `History Docs` 和 `Evidence Docs` 不留空时，说明该主题已有明确降级入口
- 如果一个主题没有历史或证据入口，可写 `none`
