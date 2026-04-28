# Root Agent Doc

把这份模板复制到你的根入口文件，并按平台重命名，例如：
- `AGENTS.md`
- `CLAUDE.md`
- 其他 Agent 平台的根入口说明文件

## Project Map
- `[path]`: [一句话职责]
- `[path]`: [一句话职责]
- `docs/`: [文档入口、规则和历史资料]

## Read First
- 进入项目先读 `README.md`
- 做复杂文档治理前先读 `docs/index.md`
- 无法判断谁说了算时先读 `docs/authority-map.md`

## Commands
- Install: `[install command or not applicable]`
- Format: `[format command or not applicable]`
- Lint: `[lint command or not applicable]`
- Typecheck: `[typecheck command or not applicable]`
- Tests: `[test command or not applicable]`
- Docs check: `[docs check command]`
- Docs audit: `[docs audit command]`

## Rules
- 不要把历史目录或证据目录当当前规则入口
- 行为变更必须同步更新对应的当前规则文档
- 不要在没有 authority map 的情况下并行维护多份正式规则

## Completion Rules
- 改当前规则：更新 authority map、相关入口和必要验证
- 改 docs-only 内容：运行文档检查并手动确认入口仍清晰

## Escalate Before Changing
- 公共 API / schema / migration
- 安全敏感配置
- 会改写历史目录边界的整理动作
- 会引入全仓强校验的治理动作

## External Docs
- `docs/index.md`
- `docs/authority-map.md`
- `[high-value convention or runbook]`
