# 既有项目渐进接入指南

当项目已经存在大量文档时，不要全量重写。按下面顺序 retrofit。

## 1. 盘点当前入口

先列出：
- 根入口文档
- 文档索引
- 局部入口
- handoff / archive / reports

目标：
- 找出哪些文件实际上在竞争“总入口”

## 2. 画 authority map

不要先改内容，先回答：
- 每个高价值主题当前谁说了算
- 哪些只是辅助说明
- 哪些是历史背景
- 哪些是证据目录

## 3. 标记 current / history / evidence

把高价值存量文档至少分成三类：
- `current`
- `history`
- `evidence`

不要求首轮就移动文件，但至少要在入口或 authority map 里声明边界。

## 4. 先治理新增和高价值文档

首轮只规范：
- 新增文档
- 高频被访问文档
- 高风险操作文档
- 当前主规则文档

不要首轮治理：
- 低频 archive
- 大量历史 handoff
- 自动生成证据目录

## 5. 补最小入口层

至少补齐：
- 根入口文档
- `README`
- `docs/index.md` 或等价入口集
- `docs/authority-map.md`

## 6. 接入轻量检查

先检查：
- 根入口存在性
- 索引存在性
- authority map 存在性
- 当前规则文档 metadata
- 关键链接

## 7. 记录摩擦

每次 retrofit 摩擦都记录：
- 是入口问题还是 authority 问题
- 是历史 / 证据混淆还是范围失控
- 是项目本地问题还是共享规范问题

## 8. 完成定义

当下列条件同时满足时，可以认为首轮 retrofit 完成：
- 新成员和 Agent 知道先看哪里
- authority map 已覆盖主要主题
- current / history / evidence 不再混成一个入口
- 新增文档有稳定模板和检查路径
