# agent-doc Host Abstraction

## Purpose

这份文档说明 `agent-doc` 如何把 runtime 演化层和具体宿主解耦。

## Four Layers

`agent-doc` 当前分成四层：

1. `协议层`
   - `SKILL.md`
   - `references/`
   - `templates/`
   - 文档治理规则本体
2. `宿主层`
   - runtime root 解析
   - host support tier
   - helper script 入口
3. `适配层`
   - `agents/openai.yaml`
   - 后续其他宿主 metadata
4. `验证层`
   - runtime 初始化
   - 结构校验
   - capture/read/promote/review 最小验证链路

## Why Runtime Must Stay Outside The Repo

如果把 runtime root 直接放进仓库工作副本，会出现三个问题：

1. 原始经验和公开资产混在一起
2. 容易把私有路径、私有上下文误提交进 repo
3. runtime 高频写入会污染正常版本控制

因此默认策略是：

- repo 只保存协议、模板、脚本和说明
- runtime 只保存本地运行痕迹与本地晋升资产

## Resolution Contract

宿主解析顺序统一为：

1. `--root`
2. `AGENT_DOC_RUNTIME_ROOT`
3. `AGENT_DOC_<HOST>_RUNTIME_ROOT`
4. host home env
5. host 默认路径约定

这样做的目的：

- 同一套脚本可复用于不同宿主
- repo 不需要硬编码某个个人目录
- 可以在测试里把 runtime root 指向临时目录

## Support Tier Contract

- `reference_ready`
  - 路径约定明确
  - helper scripts 已落地
  - smoke test 可跑
- `experimental`
  - 合同已定义
  - 脚本入口可用
  - 仍需更多真实宿主验证

当前不是所有宿主都同等成熟，仓库说明必须如实标记，不把实验态说成已完全验证。

## Public Layer Safe Output

适配层和文档层只允许暴露：

- 路径约定
- 变量名
- 目录结构
- 脚本命令
- gate 规则

不允许默认暴露：

- 某次 capture 的原始 JSON 行
- 本地绝对路径
- 私有项目原文
- 私有业务诊断细节

## Minimal Adapter Surface

当前适配层只要求宿主 metadata 能说明三件事：

1. `agent-doc` 有本地 runtime 演化层
2. runtime root 默认不在仓库工作副本里
3. raw capture 不会自动写回公开层

这让宿主可以先接入最小 contract，再逐步扩展更深的自动化。
