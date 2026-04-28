# agent-doc Runtime Memory Spec

## Purpose

这份文档定义 `agent-doc` 的本地 runtime 演化层。

目标不是把公开仓库变成经验垃圾桶，而是给每次文档治理任务一个默认的本地留痕宿主，让下一次相似任务可以低成本读取最近经验，并在 gate 下逐步晋升。

## Boundary

`agent-doc` 的经验系统分两层：

1. `runtime layer`
   - 本地宿主目录
   - 默认 capture、read、review、promote、archive、reuse
2. `repository layer`
   - 当前公开仓库
   - 只接收经过 gate 的稳定表达

硬边界：

- 不把 raw runtime 数据直接写回公开层
- 不把仓库工作副本当默认 runtime root
- 不在公开层暴露私有绝对路径
- 不在 runtime capture 中保留可还原私有业务上下文的大段原文

## Runtime Root Resolution

解析顺序：

1. 显式 `--root`
2. `AGENT_DOC_RUNTIME_ROOT`
3. host 专属 runtime env
4. host home env
5. host 默认路径约定

当前路径约定：

- `Codex`: `~/.codex/skills/agent-doc/runtime/`
- `Claude Code`: `~/.claude/skills/agent-doc/runtime/`
- `OpenClaw`: `~/.openclaw/skills/agent-doc/runtime/`

仓库工作副本不是默认 runtime root。

## Host Support Tier

- `Codex`: `reference_ready`
- `Claude Code`: `experimental`
- `OpenClaw`: `experimental`

含义：

- `reference_ready` 表示仓库已提供明确路径约定与最小 helper scripts
- `experimental` 表示结构和 contract 已定义，但仍需更多宿主实测

## Directory Layout

```text
runtime/
  captures/
    YYYY-MM-DD.jsonl
  index/
    by-scene.json
    by-doc-type.json
    by-failure-mode.json
  inbox/
    review-queue.json
  promoted/
    field-notes/
    repo-candidates/
    archive/
  state/
    manifest.json
    promotion-policy.json
    promotion-ledger.json
    reuse-ledger.json
    trigger-history.jsonl
```

## Capture Schema

最小字段：

- `timestamp`
- `session_id`
- `host`
- `skill_name`
- `scene`
- `project_profile`
- `doc_type`
- `governance_problem`
- `objective`
- `artifacts_produced`
- `what_worked`
- `what_failed`
- `local_fix_applied`
- `remaining_risk`
- `next_input`
- `candidate_pattern_tags`
- `candidate_failure_tags`
- `promotion_hint`

实现约束：

- 写入前会做最小路径脱敏
- `skill_name` 固定为 `agent-doc`
- `artifacts_produced`、`candidate_pattern_tags`、`candidate_failure_tags` 必须是列表

## Default Loop

默认工作流：

1. `read`
2. `capture`
3. `triage`
4. `compress`
5. `validate`
6. `promote`

其中：

- `read` 默认只读少量最近相关 capture 与少量 promoted notes
- `capture` 默认写最小结构化记录，而不是长复盘
- `promote` 只写入 runtime/promoted，不自动发布 repo 公共资产

## Read Budget

默认预算：

- 最近 5 条 raw captures
- 最多 3 条 promoted field notes
- 最多 2 条更高层 references

当前首版脚本实现了：

- 按 `scene` 读取最近 capture
- 按 `doc_type` 进一步过滤
- 读取命中的 promoted field notes
- 可选写入 reuse ledger

## Validation Contract

最小验证链路：

1. `scripts/init_runtime_memory.py`
2. `scripts/validate_runtime_memory.py`
3. `scripts/write_runtime_capture.py`
4. `scripts/read_runtime_context.py`
5. `scripts/promotion_worker.py`
6. `scripts/runtime_governance_report.py`
7. `scripts/review_repo_candidates.py`
8. `scripts/smoke_test_runtime_memory.py`

`smoke_test_runtime_memory.py` 会在临时 runtime root 里跑一次：

- 初始化
- 写 capture
- 校验结构
- 读取 capture
- 消费一次 review queue
- 输出治理指标

## Non-Goals

- 不做复杂语义检索
- 不自动把 repo candidate 改写成公开资产
- 不把公开仓库历史资产批量导回 runtime
- 不把调度日志提升成默认 repo 内容
