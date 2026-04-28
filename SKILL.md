---
name: agent-doc
description: >
  Use this skill when an agent needs to establish, audit, repair, or govern a project's documentation system for human and AI collaboration: document entrypoints, authority or source-of-truth boundaries, current rules vs history vs evidence separation, bounded pilot adoption, retrofit paths for existing projects, document-type templates, and lightweight docs checks. This is a documentation governance skill, not a general writing helper. Use it when docs are messy, duplicated, hard to route, or when agents keep reading the wrong files. Do not use it for ordinary one-off writing or polishing a single document.
---

# Agent DOC

## Mission

- 把 `agent-doc` 明确当成“文档治理 Skill”，而不是普通写文档助手。
- 让项目文档先变得可路由、可判断、可维护，再追求齐全。
- 让 Agent 先知道“先看哪里、谁说了算、什么算完成”，而不是先生成更多文档。
- 用最小入口层和 bounded pilot 建立秩序，避免一上来全量治理。

## Public Positioning

`agent-doc` 的主目标不是帮用户把一篇文档写漂亮，而是帮项目建立一个可被 Agent 和人稳定协同使用的文档系统。

它优先解决：
- 入口竞争
- authority 缺失
- `current / history / evidence` 混淆
- brownfield 项目的渐进治理
- 文档类型与项目类型的稳定落位

如果只是普通内容写作，应优先使用项目现有模板或更窄的写作 Skill。

## Runtime Evolution Layer

`agent-doc` 现在带有一个本地 runtime 演化层，用来沉淀文档治理过程中的最近经验，而不是把所有摩擦都直接写回公开仓库。

默认原则：

- runtime 和 repo 必须分层
- runtime root 默认不在仓库工作副本里
- raw runtime capture 不自动发布到公开层
- capture 里不应保留私有绝对路径或可还原私有业务上下文的大段原文

默认 runtime root 解析顺序：

1. 显式 `--root`
2. `AGENT_DOC_RUNTIME_ROOT`
3. host 专属 runtime env
4. host home env
5. host 默认路径约定

当前路径约定：

- `Codex`: `~/.codex/skills/agent-doc/runtime/`
- `Claude Code`: `~/.claude/skills/agent-doc/runtime/`
- `OpenClaw`: `~/.openclaw/skills/agent-doc/runtime/`

运行时目录角色：

- `captures/`: 每次任务后的最小结构化留痕
- `index/`: 按 scene / doc type / failure mode 的轻索引
- `inbox/`: review queue
- `promoted/field-notes/`: 经过本地晋升的 field note
- `promoted/repo-candidates/`: 通过 gate 的 repo candidate
- `promoted/archive/`: 被覆盖或低价值的旧经验
- `state/`: manifest、policy、ledger、trigger history

## Use This Skill When

- 你要新建一篇项目文档，并希望它按正确文档类型落位和成文。
- 项目已经有多个文档入口，但没有明确当前入口。
- 同一主题有多份文档，Agent 很难判断 `authority` 或 `source of truth`。
- 历史背景、实验记录、handoff、archive、当前规则混在一起。
- 团队准备引入 AI / Agent 协同写文档，需要先定义边界和最小治理方式。
- 你需要为一个项目建立或修复：
  - 根入口文档
  - 文档索引
  - authority map
  - 当前规则 / 历史背景 / 证据目录分层
  - 最小可运行文档检查

## Do Not Use This Skill When

- 用户只是要写一篇普通说明文、日报、周报或博客。
- 任务只是润色、校对、翻译单篇文档。
- 问题主要在产品需求、架构实现或代码质量，而不是文档协同边界。
- 你已经有稳定入口和 authority，只需要补一份局部文档。

## Supported Use Modes

### 1. Single-document creation

适用：
- 新写一篇 `README`
- 补一篇 `runbook`
- 把某条稳定约束沉淀成 `convention`
- 写 `reference`、`ADR`、`RFC`、`architecture`、`troubleshooting`

动作：
- 先判断文档类型
- 再用对应模板
- 再检查它应该属于 `当前规则`、`历史背景` 还是 `证据目录`

文档类型说明见 [references/document-types.md](references/document-types.md)。

### 2. Greenfield project setup

适用：
- 新项目从零搭文档框架
- 希望一开始就有根入口、索引、authority 和最小检查

动作：
- 先按项目类型裁剪
- 再复制最小模板集
- 最后接入轻量检查

项目裁剪说明见 [references/project-profiles.md](references/project-profiles.md)。

### 3. Brownfield retrofit

适用：
- 已有项目中途接入
- 需要让新增文档和高价值存量文档先规范起来

动作：
- 先盘点入口
- 再做 authority map
- 再区分 current / history / evidence
- 先治理新增文档和高价值文档，不全量重写

已有项目接入步骤见 [references/retrofit-existing-project.md](references/retrofit-existing-project.md)。

## First Diagnosis

先判断问题属于哪一类，再决定动作。需要细则时读取 [references/diagnosis-matrix.md](references/diagnosis-matrix.md)。

### 1. 入口问题

症状：
- 新成员或 Agent 不知道先看哪里
- `README.md`、`AGENTS.md`、`docs/`、handoff 各自都像总入口
- 入口页主要在讲历史，而不是当前协作路线

第一动作：
- 先修入口层，不先重写下游文档

### 2. Authority 问题

症状：
- 同一规则在多个文档里都有一版
- 大家默认“日期更新的那个更对”
- runbook、FAQ、实验结论被误当正式规则

第一动作：
- 先做 authority map，不先扩写内容

### 3. 历史 / 证据混淆问题

症状：
- archive、评测记录、实验报告被当成当前规则入口
- 设计演化背景和当前执行规则写在同一文档
- Agent 会把“为什么如此”误读成“现在必须这样做”

第一动作：
- 先拆出当前规则、历史背景、证据目录三层

### 4. 范围失控问题

症状：
- 想一次性把所有文档重写完
- 模板、规范、目录和脚本同时扩张
- 还没跑 pilot，就想做全量 CI 治理

第一动作：
- 先定义 pilot 边界和不治理范围

## Default Workflow

### 1. Find the minimal entry layer

优先建立或修复以下最小层，而不是先补齐所有文档：

1. 一个根级 Agent 控制文档
2. 一个项目总入口
3. 一个文档索引或分散式导航声明
4. 一份 authority map
5. 一到两份当前高价值规则文档

如果项目不是代码仓库，也保持同样角色分工，只把文件名换成该环境的常用入口名。
如果当前任务只是“新建单篇文档”，可以跳过入口层重建，直接按对应文档类型模板创建，但仍要确认它应归属的文档层级。

### 2. Separate roles before editing content

先把文档分成三类：

- `当前规则`：回答“现在按什么做”
- `历史背景`：回答“为什么会演化到这里”
- `证据目录`：回答“有哪些实验、观察、数据或报告支持某个判断”

不要把历史目录或证据目录当默认规则入口。

### 3. Build an authority map

authority map 至少要回答：

- 这个主题的主文档是哪份
- 哪些文档只是辅助解释
- 哪些只能作为历史背景
- 哪些属于证据资产
- 冲突时先信谁

推荐使用半结构化表格而不是自由叙述。字段规范见 [references/authority-map-schema.md](references/authority-map-schema.md)。

### 4. Choose a bounded pilot

一次只治理：
- 一个子系统，或
- 一个高频流程，或
- 一组最小入口文档

不要把整个仓库同时纳入重写、重命名、归档和强校验。需要步骤时读取 [references/bounded-pilot.md](references/bounded-pilot.md)。
如果是 brownfield 项目，再同时读取 [references/retrofit-existing-project.md](references/retrofit-existing-project.md)。

### 5. Add only lightweight checks first

优先自动检查：
- 根入口文件是否存在
- 文档索引是否存在
- authority map 是否存在
- 关键文档 metadata 是否完整
- 入口链接是否失效

不要第一轮就做：
- 全量历史文档治理
- 复杂语义冲突检测
- 大规模自动修复

如果需要脚本，优先复用 [scripts/check_docs.py](scripts/check_docs.py) 和 [templates/docs-policy.example.json](templates/docs-policy.example.json)。
需要接入顺序时读取 [references/automation-adoption.md](references/automation-adoption.md)。
如果要先做诊断审计，再决定怎么治理，运行 [scripts/audit_docs.py](scripts/audit_docs.py)。

### 6. Record friction and keep the standard small

每次摩擦都先记录：
- 症状
- 发生阶段
- 影响
- 本地修正是否有效
- 是否真的是共享规范问题

不要因为一个项目的一次不适配，就立刻扩写共享 Skill。

如果当前环境允许写本地文件，且这次任务已经明显进入文档治理层，优先做三件事：

1. 读取少量最近相关 runtime 经验
2. 在结束时写一条最小 runtime capture
3. 仅在满足 gate 时把经验晋升到本地 field note 或 repo candidate

如果当前环境不允许写本地 runtime，必须明确说明未完成 runtime capture，不要声称经验已经进入系统。

## Minimum Entry Layer

一个可用的最小入口层通常包含：

1. 根级 Agent 文档：负责路由、命令、禁区、完成定义
2. 根级 `README.md`：负责项目总入口和文档导航
3. `docs/index.md`：负责文档分层和跳转
4. `docs/authority-map.md`：负责声明主文档、历史背景和证据边界
5. 一份高价值当前规则文档：例如 convention 或 runbook

模板见：
- [templates/README.template.md](templates/README.template.md)
- [templates/root-agent-doc.template.md](templates/root-agent-doc.template.md)
- [templates/docs-index.template.md](templates/docs-index.template.md)
- [templates/authority-map.template.md](templates/authority-map.template.md)
- [templates/architecture-overview.template.md](templates/architecture-overview.template.md)
- [templates/convention.template.md](templates/convention.template.md)
- [templates/runbook.template.md](templates/runbook.template.md)
- [templates/troubleshooting.template.md](templates/troubleshooting.template.md)
- [templates/reference-api.template.md](templates/reference-api.template.md)
- [templates/adr.template.md](templates/adr.template.md)
- [templates/rfc-design.template.md](templates/rfc-design.template.md)
- [templates/tutorial.template.md](templates/tutorial.template.md)
- [templates/friction-record.template.md](templates/friction-record.template.md)

## Shared Decision Rules

- `当前规则` 应该短、稳定、可执行。
- `历史背景` 应该解释演化，不争夺当前口径。
- `证据目录` 应该支持判断，不直接下达规则。
- `AGENTS.md`、`CLAUDE.md` 或其他根入口文档应做路由，不做百科。
- 新日期不自动等于更权威；文档角色和 `Source of Truth` 更重要。
- 如果项目还没有 authority map，不要并行扩写多份主题文档。
- 不同项目应先裁剪模板集，不要复制整包后长期不维护。
- 特殊项目类型应先选项目画像，再决定是否需要额外的 tutorial、ADR、reference 或调试文档。

## Anti-Patterns To Avoid

### 继续抽象扩张

不要在没有真实摩擦证据前，一直新增“更上层”的规范词汇。

### 过度治理

不要为了“看起来完整”而要求所有目录都立刻满足同一标准。

### 全量重写历史文档

不要把 archive、handoff、实验报告整批改成当前规范文档。先声明边界，再决定是否局部整理。

### 把证据目录当规则入口

观测结果、实验报告、截图、评测数据可以支撑判断，但默认不应取代当前规则文档。

## Platform Notes

- `Codex` 可直接使用本 Skill。
- `Claude Code / OpenClaw` 需要把根入口说明映射到各自入口文件，但保留同样的文档角色分工。
- 适配步骤见 [references/platform-adaptation.md](references/platform-adaptation.md)。

## References

- 诊断四类问题时读取 [references/diagnosis-matrix.md](references/diagnosis-matrix.md)
- 建立最小入口层和 pilot 时读取 [references/bounded-pilot.md](references/bounded-pilot.md)
- 按单篇文档类型写作时读取 [references/document-types.md](references/document-types.md)
- 按项目类型裁剪和选模板时读取 [references/project-profiles.md](references/project-profiles.md)
- 为已有项目渐进接入时读取 [references/retrofit-existing-project.md](references/retrofit-existing-project.md)
- 接入 pre-commit、CI 或 nightly 检查时读取 [references/automation-adoption.md](references/automation-adoption.md)
- authority map 字段规范见 [references/authority-map-schema.md](references/authority-map-schema.md)
- 适配其他 Agent 平台时读取 [references/platform-adaptation.md](references/platform-adaptation.md)
- 做触发自测时读取 [references/validation-cases.md](references/validation-cases.md)
- runtime root、capture schema 与读写边界见 [docs/runtime-memory-spec.md](docs/runtime-memory-spec.md)
- runtime 晋升策略见 [docs/runtime-promotion-policy.md](docs/runtime-promotion-policy.md)
- 宿主分层与 support tier 见 [docs/host-abstraction.md](docs/host-abstraction.md)
- 经验复利闭环见 [references/experience-compounding-loop.md](references/experience-compounding-loop.md)
