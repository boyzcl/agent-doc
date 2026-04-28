# Bounded Pilot 指南

首轮治理的目标不是“文档系统做全”，而是建立一个能稳定协作的最小闭环。

## 1. 先选试点边界

优先选下面三种之一：
- 一个高频流程，例如发布、部署、交接
- 一个文档密度高但范围清楚的子系统
- 一组最小入口文档，例如 `AGENTS.md`、`README.md`、`docs/index.md`、authority map

不要首轮就覆盖：
- 历史归档目录
- 实验报告目录
- 自动生成目录
- 多年存量文档全集

## 2. 建立最小入口层

首轮最小落地通常只需要：

1. 根级 Agent 控制文档
2. 根级 `README.md`
3. `docs/index.md`
4. `docs/authority-map.md`
5. 一份当前规则文档
6. 一份与当前规则相配套的操作文档或 runbook

如果资源更紧，只先完成前五项。

## 3. 分清三类资产

### 当前规则

回答：
- 现在按什么做
- 什么算完成
- 冲突时先信谁

典型位置：
- `docs/conventions/`
- `docs/runbooks/`
- 根级 Agent 入口文档

### 历史背景

回答：
- 为什么会演化到当前方案
- 哪些旧方案已经被替代

典型位置：
- `docs/history/`
- `docs/archive/`
- `docs/adr/`

### 证据目录

回答：
- 这个判断基于哪些评测、观察、日志或实验

典型位置：
- `docs/reference/evidence-*`
- `reports/`
- `artifacts/`

规则：
- 证据目录默认 `Source of Truth: no`
- 历史背景默认不参与当前入口竞争

## 4. 先加轻量检查

首轮检查只建议覆盖：
- 根入口文件存在性
- authority map 存在性
- 入口链接有效性
- 当前规则文档 metadata
- runbook 的核心结构

暂不覆盖：
- 历史目录统一 metadata
- 证据目录全量 lint
- 语义重复自动检测

## 5. 记录摩擦

每次 pilot 期间出现摩擦，都至少记录：
- 症状
- 阶段
- 涉及文档或模板
- 本地修正是否有效
- 是否值得升级为共享规范问题

模板见 [templates/friction-record.template.md](../templates/friction-record.template.md)。

## 6. 判断本地问题还是共享问题

优先判断为 `项目本地问题` 的情况：
- 只有一个项目出现
- 路径、命名、owner 特别定制
- 团队没有按最小入口层落地

优先判断为 `共享规范问题` 的情况：
- 两个及以上上下文反复出现
- 本地修正仍无法稳定缓解
- 问题直接击中入口、authority 或最小模板本身

## 7. 试点完成定义

可以把 pilot 判定为完成，当且仅当：
- 新成员或 Agent 知道先看哪里
- authority map 能回答主要主题谁说了算
- 当前规则、历史背景、证据目录不再混放
- 最小检查脚本能跑
- 至少记录过一轮摩擦
