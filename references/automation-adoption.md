# 文档检查接入指南

`agent-doc` 的检查脚本是辅助治理，不是治理本身。

## 推荐接入顺序

1. 先手工本地运行
2. 再放进本地开发脚本或 pre-commit
3. 再接入 CI
4. 最后再考虑 nightly report

## 最小命令

```bash
python3 scripts/check_docs.py --root . --config templates/docs-policy.example.json
```

## 初始阶段建议启用

- 根入口存在性
- 文档索引存在性
- authority map 存在性
- metadata 完整性
- 关键链接有效性

## 稳定后再启用

- 结构完整性
- 行数预算
- 更细的类型规则

## 高文档密度项目建议

如果项目里有大量评测、观测、回放、实验结果或归档材料：
- 首轮先在 `ignore_paths` 排除这些目录
- 只治理当前入口和当前规则文档
- 等 authority map 稳定后再决定是否逐步纳入
