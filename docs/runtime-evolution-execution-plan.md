# agent-doc Runtime Evolution Execution Plan

## Purpose

这份文档是给下一次新对话直接接手执行用的 handoff。

目标不是继续讨论“要不要做”，而是基于当前 `agent-doc` 仓库状态，落地一套参考 `ai-native-loop` 演化机制的本地持续进化层，让 `agent-doc` 具备：

- 本地默认留痕
- 低成本读取最近相关经验
- 受 gate 约束的经验晋升
- 不污染公开仓库主干的持续优化能力

## Current Repository State

当前仓库根目录：
- `/Users/boyzcl/Documents/A/Agent规范/agent-doc`

当前已经存在的公开层资产：
- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `templates/`
- `scripts/check_docs.py`
- `scripts/audit_docs.py`
- `examples/minimal-project/`

当前仓库已经具备：
- 文档治理主干
- 单篇文档类型支持
- greenfield / brownfield 支持
- authority map 半结构化 schema
- 最小 `check` 与最小 `audit`

当前还没有的，是“本地 runtime 演化层”。

## Strategic Judgment

`agent-doc` 不应把所有经验直接写回公开仓库。

正确方向是参考 `ai-native-loop`，建立两层经验系统：

1. `Runtime Layer`
   - 本地宿主目录
   - 默认 capture、review、promotion、archive、reuse
2. `Repository Layer`
   - 当前公开仓库
   - 只接收经过 gate 的稳定资产

## Design Principles

### 1. Runtime and Repo Must Be Split

本地积累与公开表达必须分层。

### 2. Default Capture Must Be Lightweight

默认不是写长复盘，而是写最小结构化记录。

### 3. Promotion Must Follow a Ladder

默认流转梯子：
1. `raw capture`
2. `reviewed note`
3. `promoted field note`
4. `repo candidate`

### 4. Repo Candidate Is Not Auto-Publish

`repo candidate` 只表示“值得考虑反哺仓库”，不等于自动修改公开资产。

### 5. Capacity Governance Must Exist

不能只积累，不治理 working set、archive、dedup、reuse。

## Target Architecture For agent-doc

建议给 `agent-doc` 建四层：

1. `协议层`
   - 文档治理主干
   - entrypoint / authority / history-evidence / scope
   - single-doc / greenfield / brownfield
2. `宿主层`
   - runtime root 解析
   - host support tier
3. `适配层`
   - `agents/openai.yaml`
   - 后续其他宿主 metadata
4. `验证层`
   - runtime smoke tests
   - runtime structure validation
   - retrieval / promotion / governance validation

## Runtime Root Rules

默认 runtime root 不应放在仓库工作副本里。

建议路径：
- `Codex`: `~/.codex/skills/agent-doc/runtime/`
- `Claude Code`: `~/.claude/skills/agent-doc/runtime/`
- `OpenClaw`: `~/.openclaw/skills/agent-doc/runtime/`

建议解析顺序：
1. 显式 `--root`
2. `AGENT_DOC_RUNTIME_ROOT`
3. host 专属 runtime env
4. host home env
5. host 默认路径约定

## Proposed Runtime Layout

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

## Proposed Capture Schema

最小字段建议：
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

约束：
- 不记录本地绝对路径
- 不记录可还原私有业务背景的大段原文

## Default Experience Loop

建议默认循环：
1. `read`
2. `capture`
3. `triage`
4. `compress`
5. `validate`
6. `promote`

## Promotion Policy For agent-doc

### Promotion Ladder

1. `raw capture`
2. `reviewed note`
3. `promoted field note`
4. `repo candidate`

### Repo Candidate Gate

至少满足下列 4 条中的 2 条，才允许进入 `repo candidate`：
- 7 到 14 天内重复出现
- 出现在两个不同项目语境里
- 已能稳定抽象成 `pattern / failure mode / template refinement / audit rule`
- 会显著改变下一次文档治理判断

额外硬门槛：
- 可匿名化
- 可脱离原项目理解

否则一律停留在 runtime 层。

### Dedup Rule

默认顺序：
1. merge
2. update
3. new

### Archive Rule

满足任一条件即可 archive：
- 被更强版本覆盖
- 长期未命中 reuse
- 只是单项目一次性细节
- 无法匿名化

### Capacity Rule

首版建议：
- `pending backlog threshold >= 10`
- `promoted working set ceiling = 20`
- `repo candidates` 可撤回
- `reuse ledger` 回写 promotion ledger

## Task Scope For The Next Conversation

下一次对话的任务不是“讨论这套方案”，而是**实际把它落进当前仓库**。

至少要完成：

### A. 文档层

新增或更新以下文档：
- `docs/runtime-memory-spec.md`
- `docs/runtime-promotion-policy.md`
- `docs/host-abstraction.md`
- `references/experience-compounding-loop.md`

### B. Runtime Script Layer

新增最小脚本骨架：
- `scripts/init_runtime_memory.py`
- `scripts/validate_runtime_memory.py`
- `scripts/write_runtime_capture.py`
- `scripts/read_runtime_context.py`
- `scripts/promotion_worker.py`
- `scripts/runtime_governance_report.py`
- `scripts/review_repo_candidates.py`
- `scripts/smoke_test_runtime_memory.py`

### C. Skill Integration

更新：
- `SKILL.md`
- `README.md`
- `agents/openai.yaml`

要求它们明确：
- `agent-doc` 有本地 runtime 演化层
- 公开仓库与本地 runtime 分层
- 默认 capture / read / promote 的边界

### D. Validation

至少完成：
- runtime 初始化 smoke test
- runtime 结构校验
- 一次最小 capture 写入与读取
- 一次最小 promotion / governance report 演示

## Constraints

- 不要把 runtime 设计成重型知识库
- 不要把仓库工作副本当默认 runtime root
- 不要把 repo candidate 自动写回公开 references / templates
- 不要把单次经验直接升级成公开规范
- 不要引入项目私有路径或私有业务上下文
- `SKILL.md` 仍要保持简洁，细节放到 `docs/` 和 `references/`

## Definition Of Done

只有当以下条件同时满足时，任务才算完成：

1. `agent-doc` 已具备本地 runtime 演化层文档说明
2. runtime 最小脚本可以运行
3. 可以初始化 runtime 目录
4. 可以写入一条 capture
5. 可以读取相关 capture
6. 可以生成最小治理报告
7. 公开仓库边界仍然干净，没有把 runtime raw data 混入公开层
8. 最终回复清楚说明：
   - 创建或修改了哪些文件
   - 如何初始化和验证 runtime
   - 当前能力边界和未完成项

## Final Output Requirement For The Next Conversation

下一次执行完成后，最终回复至少要包含：

1. 已创建 / 修改文件清单
2. runtime 机制最终结构
3. 运行过的验证命令与结果摘要
4. 当前还未完成或仍属实验状态的部分
5. 对这套自进化机制是否“足够可用”的判断
