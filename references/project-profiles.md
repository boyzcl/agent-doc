# 项目类型裁剪与模板选型

不是每个项目都需要完整文档套件。先按项目画像裁剪，再复制最小模板集。

## 1. 极小型项目

特征：
- 单人或双人维护
- 无复杂部署链路

最小模板集：
- [templates/root-agent-doc.template.md](../templates/root-agent-doc.template.md)
- [templates/README.template.md](../templates/README.template.md)

可选：
- [templates/docs-index.template.md](../templates/docs-index.template.md)
- [templates/runbook.template.md](../templates/runbook.template.md)

## 2. 常规工程项目

特征：
- 多模块
- 有 CI、测试和部署

最小模板集：
- 根入口模板
- `README`
- `docs-index`
- `architecture`
- `convention`
- `runbook`

可选：
- `troubleshooting`
- `ADR`

## 3. Monorepo

特征：
- 多包、多服务、多子系统

最小模板集：
- 根入口模板
- `README`
- `docs-index`
- `authority-map`
- `architecture`
- 至少一份局部 `convention` 或 `runbook`

特别建议：
- 根入口保持短
- 更多复杂度下沉到局部入口或局部文档

## 4. SDK / Library

最小模板集：
- 根入口模板
- `README`
- `reference-api`
- `ADR`

可选：
- `tutorial`
- `architecture`
- `rfc-design`

## 5. 服务端 / 基础设施

最小模板集：
- 根入口模板
- `README`
- `docs-index`
- `architecture`
- `runbook`
- `troubleshooting`

## 6. 数据 / ML / AI 项目

最小模板集：
- 根入口模板
- `README`
- `docs-index`
- `architecture`
- `runbook`
- `reference-api`

可选：
- `convention`
- `ADR`
- `rfc-design`

特别注意：
- 实验记录和生产规范边界要分开
- 证据目录默认不是规则入口

## 7. 高文档密度 / 复杂存量项目

最小模板集：
- 根入口模板
- `README`
- `authority-map`
- 必要时再补 `docs-index`
- 一份当前上位规则或当前阶段主文档

特别建议：
- 先修入口，不先重命名历史文件
- 先声明 current / history / evidence 边界

## 8. 强监管或高风险项目

最小模板集：
- 常规工程项目模板
- `ADR`
- `rfc-design`

可选：
- `troubleshooting`
- 审批型 runbook

## 9. 选择原则

- 先满足控制层和导航层
- 再补高风险、高频流程
- 不要复制所有模板
- 复制后必须删减占位区块
- 特殊项目先看画像，再决定是否增加教程、调试或 ADR
