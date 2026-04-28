# agent-doc Experience Compounding Loop

## Purpose

这份参考说明 `agent-doc` 的经验如何在 runtime 层持续复利，而不是每次都只留在一次性对话里。

## Loop

默认闭环：

1. `read`
2. `capture`
3. `triage`
4. `compress`
5. `validate`
6. `promote`

## Read

进入新任务时，不默认扫完整 runtime。

优先读取：

- 最近相似 `scene`
- 最近相似 `doc_type`
- 少量已晋升的 field notes

读取预算应小而稳，避免把 runtime 变成新的噪音源。

## Capture

默认 capture 不是长篇复盘，而是最小结构化记录。

至少写清：

- 这次治理问题是什么
- 哪个文档类型或场景出现摩擦
- 什么做法有效
- 什么做法失败
- 还有什么风险没解决
- 下一轮应该带着什么输入继续

## Triage

不是所有 capture 都值得晋升。

先判断：

- 是一次性细节，还是重复问题
- 是局部修补，还是能迁移的方法
- 会不会改变下次的文档治理判断

## Compress

压缩的目标不是“更短”，而是“更可复用”。

首选把个案压成：

- 可复用的 pattern
- 可命名的 failure mode
- 可复现的 next input

## Validate

进入下一层前先检查：

- 是否匿名化
- 是否还带着私有绝对路径
- 是否能脱离原项目语境阅读
- 是否仍然只是 raw 运行数据

如果答案不安全，就停留在 runtime 层。

## Promote

默认梯子：

1. `raw capture`
2. `reviewed note`
3. `promoted field note`
4. `repo candidate`

注意：

- `repo candidate` 不是自动发布
- repo 层只接收稳定表达，不接 raw capture

## Reuse

当 promoted field note 在后续任务里再次被读取时：

- reuse event 写入 `reuse-ledger`
- promoted note 的复用计数增加
- 后续 repo candidate gate 可以参考真实复用信号

## Governance

这套机制只有 capture 没有治理会失控。

因此最小治理也要同时存在：

- review queue
- archive
- dedup / merge
- promotion ledger
- reuse ledger
- trigger history

## Practical Meaning For agent-doc

对 `agent-doc` 来说，经验复利最有价值的不是“写了更多笔记”，而是：

- 下次更快判断先修入口还是先修 authority
- 更快识别 `current / history / evidence` 混淆
- 更快判断某个修补应停留在 runtime 层还是值得升级成共享规范
