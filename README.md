# agent-doc

`agent-doc` 是一个中文优先、平台中立的文档治理 Skill，用来帮助人和 Agent 在真实项目里建立稳定的文档入口、权威边界和渐进式治理方式。

它首先是“文档治理层”，其次才是“文档写作层”。
它的重点不是把一篇文档写得更像样，而是让整个项目文档系统更容易被 Agent 和人正确读取、正确路由、正确维护。

它重点解决这些问题：
- 文档太多，但没人知道先看哪里
- 多份文档都像“正式规则”，Agent 容易信错
- 历史背景、实验记录、证据目录和当前规则混在一起
- 团队一上来就想全量重写文档，治理范围迅速失控

它不解决这些问题：
- 普通单篇文章润色
- 营销文案或法务文书写作
- 用文档替代 CI、脚本、权限或评审制度

## 本地 runtime 演化层

`agent-doc` 现在带有一套本地优先的 runtime 演化层，用来积累“这次文档治理到底哪里卡住、什么修法有效、下次应该先读什么”。

这层和公开仓库明确分开：

- runtime root 默认在宿主本地目录，不在仓库工作副本里
- raw runtime capture 不自动写回公开仓库
- 只有经过 gate 的 field note / repo candidate 才会停留在本地晋升层
- repo 公共层继续只保存协议、模板、脚本和说明

默认路径约定：

- `Codex`: `~/.codex/skills/agent-doc/runtime/`
- `Claude Code`: `~/.claude/skills/agent-doc/runtime/`
- `OpenClaw`: `~/.openclaw/skills/agent-doc/runtime/`

核心说明见：

- [docs/runtime-memory-spec.md](docs/runtime-memory-spec.md)
- [docs/runtime-promotion-policy.md](docs/runtime-promotion-policy.md)
- [docs/host-abstraction.md](docs/host-abstraction.md)
- [docs/runtime-quickstart.md](docs/runtime-quickstart.md)
- [references/experience-compounding-loop.md](references/experience-compounding-loop.md)

## 何时使用

当你需要让 Agent 协同处理项目文档，而问题已经不是“少写一篇文档”，而是“文档系统失去入口、边界或稳定性”时，使用这个 Skill。

它支持三种主要用法：
- 单篇文档创建：按文档类型写一篇 `README`、`runbook`、`convention`、`reference`、`ADR` 或 `RFC`
- 新项目从零建框架：从一开始就按最小入口层、authority 和模板体系搭建
- 既有项目 retrofit：先稳住入口和 authority，再渐进整理存量文档

典型场景：
- 仓库里同时有 `AGENTS.md`、`README.md`、`docs/`、handoff、archive、评测报告，但没人说得清谁是当前口径
- Agent 经常读到错误文档、错误完成定义，或者把历史结论当当前规则
- 你想先做一个 bounded pilot，而不是把整库文档一次性重做

## 直接接入

- `Codex`：仓库根目录本身就是一个可直接使用的 Skill 包。
- `Claude Code / OpenClaw`：保留本仓库结构不变，只需要把根入口说明映射到各自的入口文件或系统提示。见 [references/platform-adaptation.md](references/platform-adaptation.md)。

## 仓库内容

- [SKILL.md](SKILL.md)：Skill 主体
- [references/diagnosis-matrix.md](references/diagnosis-matrix.md)：问题诊断矩阵
- [references/bounded-pilot.md](references/bounded-pilot.md)：最小入口层和试点治理方法
- [references/document-types.md](references/document-types.md)：单篇文档按类型写法
- [references/project-profiles.md](references/project-profiles.md)：项目类型裁剪与模板选型
- [references/retrofit-existing-project.md](references/retrofit-existing-project.md)：已有项目渐进接入路径
- [references/automation-adoption.md](references/automation-adoption.md)：检查脚本接入方式
- [references/authority-map-schema.md](references/authority-map-schema.md)：authority map 半结构化字段规范
- [references/platform-adaptation.md](references/platform-adaptation.md)：多平台轻改造说明
- [references/experience-compounding-loop.md](references/experience-compounding-loop.md)：runtime 经验如何从 capture 进入 field note 和 repo candidate
- [scripts/check_docs.py](scripts/check_docs.py)：最小可运行检查脚本
- [scripts/audit_docs.py](scripts/audit_docs.py)：最小审计与报告脚本
- [scripts/init_runtime_memory.py](scripts/init_runtime_memory.py)：初始化本地 runtime 目录
- [scripts/validate_runtime_memory.py](scripts/validate_runtime_memory.py)：校验 runtime 结构与 capture schema
- [scripts/write_runtime_capture.py](scripts/write_runtime_capture.py)：写入一条本地 runtime capture
- [scripts/read_runtime_context.py](scripts/read_runtime_context.py)：按 scene / doc type 读取最近经验
- [scripts/promotion_worker.py](scripts/promotion_worker.py)：消费 review queue 并本地晋升 field note / repo candidate
- [scripts/runtime_governance_report.py](scripts/runtime_governance_report.py)：输出 runtime backlog / promote / reuse 指标
- [scripts/review_repo_candidates.py](scripts/review_repo_candidates.py)：查看或更新本地 repo candidate review 状态
- [scripts/smoke_test_runtime_memory.py](scripts/smoke_test_runtime_memory.py)：跑一轮最小端到端 smoke test
- [docs/runtime-quickstart.md](docs/runtime-quickstart.md)：真实宿主与临时 root 的最小操作链路
- [examples/runtime-memory-cli-sample.json](examples/runtime-memory-cli-sample.json)：runtime capture 示例输入
- [templates/](templates/)：可直接复制的模板
- [examples/minimal-project/](examples/minimal-project/)：匿名化最小示例
