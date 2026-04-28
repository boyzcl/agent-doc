# agent-doc Runtime Promotion Policy

## Purpose

这份文档定义 `agent-doc` 的本地经验如何从默认留痕进入更高层系统资产。

## Promotion Ladder

默认四级流转：

1. `raw capture`
   - 只保留在 `runtime/captures/`
2. `reviewed note`
   - 进入 `runtime/inbox/review-queue.json`
3. `promoted field note`
   - 升级到 `runtime/promoted/field-notes/`
4. `repo candidate`
   - 升级到 `runtime/promoted/repo-candidates/`
   - 仍然只是候选，不等于自动修改公开仓库

## Review Policy

默认先看 runtime 价值，再看 repo 价值。

第一版 worker 的最小判断信号：

- `repeat_signal`
- `transfer_signal`
- `specificity_signal`
- `future_judgment_signal`
- `multi_project_signal`

分数不足时：

- 保留 raw 或进入 archive

分数达到 `promote_min_score` 时：

- 创建或更新本地 field note

## Repo Candidate Gate

只有满足下列 4 条中的至少 2 条，才允许进入 `repo candidate`：

- 重复出现
- 跨项目语境出现
- 已能抽象成 pattern 或 failure mode
- 会显著改变下一次文档治理判断

额外硬边界：

- 能匿名化
- 能脱离原项目理解
- 不包含 raw capture jsonl

## Dedup Rule

默认顺序：

1. merge
2. update
3. new

首版实现采用保守策略：

- 先按 `doc_type + scene` 生成稳定 slug
- 如果同 slug 的 field note 已存在，则优先 merge/update
- repo candidate 也走稳定 slug，避免同一经验反复散落成多个候选

## Archive Rule

满足任一条件即可 archive：

- promotion score 太低
- 命中 `smoke-only`、`demo only`、`synthetic-only`、`temporary cli sample` 等明确低价值关键词
- 被更高质量 field note 覆盖

archive 仍保留在本地 runtime 层，不回写公开仓库。

## Capacity Governance

首版默认阈值：

- `review_queue_backlog_threshold >= 10`
- `promoted_working_set_ceiling = 20`
- `default_batch_size = 5`

当前脚本层已实现：

- review queue pending / reviewed 分流
- promotion ledger run 记录
- reuse ledger 命中回写
- trigger history 留痕

当前尚未实现：

- 真正的 working set 自动裁剪
- 更细的相似度 dedup
- 候选撤回 reconcile

## Runtime / Repo Boundary

runtime 层负责：

- 默认 capture
- 最近经验读取
- review queue
- field note / repo candidate 的本地沉淀

repo 层负责：

- 公共表达
- 模板、README、Skill contract、metadata
- 可验证、可分享、可版本化的稳定资产

一句话：

> runtime 负责让经验先留下来，repo 负责让经验经过 gate 后再公开表达。

## Review Workflow

repo candidate 默认只有三种状态：

- `pending`
- `accepted`
- `rejected`

`scripts/review_repo_candidates.py` 只更新本地候选状态，不直接生成 repo patch。
