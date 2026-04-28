# 平台适配说明

`agent-doc` 的核心是文档角色分工、authority 边界和渐进治理方法，不依赖某一个 Agent 平台的专有能力。

## Codex

这是默认直连平台：
- 仓库根目录就是 Skill 包
- 直接使用 `SKILL.md` 和 `agents/openai.yaml`
- `references/`、`templates/`、`scripts/`、`examples/` 维持原样即可

## Claude Code

最小改造步骤：

1. 保留本仓库目录结构不变
2. 把 `SKILL.md` 中的触发边界、诊断流程、最小入口层和反模式，映射到 `Claude Code` 使用的入口说明文件
3. 把示例里的根入口文档名按需替换成该平台常用文件名
4. 保持 `references/`、`templates/`、`scripts/check_docs.py` 不变

建议只改“入口承载方式”，不要改核心方法：
- 入口问题先修入口层
- authority 问题先画 authority map
- 历史 / 证据问题先做边界分层
- 范围失控时先退回 bounded pilot

## OpenClaw

最小改造步骤：

1. 保留本仓库目录结构不变
2. 把 `SKILL.md` 的主流程映射到 OpenClaw 的常驻说明入口
3. 继续使用同一套 `references/`、`templates/` 和 `scripts/check_docs.py`
4. 如果 OpenClaw 的默认入口文件名不同，只替换入口文件名，不替换方法角色

## 适配时不要改动的核心

这些内容跨平台应保持不变：
- 文档最小入口层的角色分工
- authority map 的存在与用途
- 当前规则 / 历史背景 / 证据目录的三分法
- bounded pilot 先于全量治理
- 摩擦先本地归因，再决定是否升级共享规范

## 适配时可以改动的外壳

这些内容可以按平台轻改：
- 根入口文件名
- 入口说明语气和示例命令
- 是否保留 `agents/openai.yaml`
- 是否把 `SKILL.md` 拆成平台本地说明加共享 references
