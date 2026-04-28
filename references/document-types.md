# 文档类型写法总览

这个 Skill 不只治理文档系统，也支持按类型直接创建单篇项目文档。

## 使用顺序

1. 先判断这篇文档主要解决什么问题
2. 再判断它属于哪种文档类型
3. 再用对应模板
4. 最后确认它属于 `当前规则`、`历史背景` 或 `证据目录`

## 1. README

适用：
- 仓库总入口
- 模块入口

主要回答：
- 这是什么
- 怎么最快开始
- 下一层文档去哪里看

不应承担：
- 全部架构细节
- 全部 runbook
- 全部 API 参考

模板：
- [templates/README.template.md](../templates/README.template.md)

## 2. Tutorial / Onboarding

适用：
- 第一次跑通项目
- 第一次使用某项能力

主要回答：
- 适合谁
- 先决条件是什么
- 按什么顺序完成一次最小成功路径

不应承担：
- 大量原理解释
- 完整参考字典

模板：
- [templates/tutorial.template.md](../templates/tutorial.template.md)

## 3. Architecture

适用：
- 解释系统边界、模块职责、关键数据流

主要回答：
- 系统如何组织
- 哪些是硬边界

不应承担：
- 操作步骤
- API 字段字典

模板：
- [templates/architecture-overview.template.md](../templates/architecture-overview.template.md)

## 4. Convention

适用：
- 稳定约束、命名规则、测试约定、错误处理约定

主要回答：
- 什么必须、应该、可以
- 正反例是什么
- 如何检查

模板：
- [templates/convention.template.md](../templates/convention.template.md)

## 5. Runbook

适用：
- 部署、回滚、值班、固定顺序操作

主要回答：
- 什么情况下用
- 前置条件是什么
- 具体步骤、成功判定、回滚、升级路径是什么

模板：
- [templates/runbook.template.md](../templates/runbook.template.md)

## 6. Troubleshooting

适用：
- 故障排查、常见症状定位

主要回答：
- 症状是什么
- 常见原因有哪些
- 排查顺序、证据入口和升级条件是什么

模板：
- [templates/troubleshooting.template.md](../templates/troubleshooting.template.md)

## 7. Reference / API

适用：
- 接口、字段、配置项、错误码、schema、事实性证据目录

主要回答：
- 精确字段、类型、默认值、限制、示例是什么

边界：
- 事实和证据可以放这里
- 决策结论不要和事实字典混成一个入口

模板：
- [templates/reference-api.template.md](../templates/reference-api.template.md)

## 8. ADR

适用：
- 记录已做出的重要决策

主要回答：
- 为什么这样选
- 替代方案是什么
- 影响范围是什么

注意：
- ADR 是角色，不必强行把历史决策文档全重命名成 `ADR-*`

模板：
- [templates/adr.template.md](../templates/adr.template.md)

## 9. RFC / Design Doc

适用：
- 重大变更前的方案比较和评审材料

主要回答：
- 问题定义是什么
- 候选方案有哪些
- 推荐方案与权衡是什么

模板：
- [templates/rfc-design.template.md](../templates/rfc-design.template.md)

## 10. 归类判断口诀

- 要“最快知道怎么开始”用 `README`
- 要“第一次按步骤成功”用 `tutorial`
- 要“理解系统怎么组织”用 `architecture`
- 要“长期稳定约束”用 `convention`
- 要“按步骤正确执行”用 `runbook`
- 要“按症状排查问题”用 `troubleshooting`
- 要“查事实和字段”用 `reference`
- 要“记为什么这样定”用 `ADR`
- 要“先比较方案再决定”用 `RFC / design doc`
