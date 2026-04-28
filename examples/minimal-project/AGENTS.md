# AGENTS.md

## Project Map
- `docs/`: 当前规则、操作文档、历史背景和证据目录

## Read First
- 进入项目先读 `README.md`
- 无法判断文档主次时先读 `docs/authority-map.md`
- 执行发布相关动作前先读 `docs/runbooks/release-smoke.md`

## Commands
- Install: `not applicable`
- Format: `not applicable`
- Lint: `not applicable`
- Typecheck: `not applicable`
- Tests: `not applicable`
- Docs check: `python3 ../../scripts/check_docs.py --root . --config ../../templates/docs-policy.example.json`
- Docs audit: `python3 ../../scripts/audit_docs.py --root .`

## Rules
- 当前发布规则以 `docs/conventions/release-policy.md` 为准
- 历史背景只能从 `docs/history/` 进入，不参与当前入口竞争
- 证据目录只能支持判断，不能替代当前规则文档

## Completion Rules
- 改发布规则时，同步更新 `docs/authority-map.md`
- 改 docs-only 内容时，至少运行一次 docs check

## Escalate Before Changing
- 想把历史目录重新纳入当前规则入口
- 想给整个仓库增加更强的文档治理规则

## External Docs
- `docs/index.md`
- `docs/authority-map.md`
- `docs/conventions/release-policy.md`
- `docs/runbooks/release-smoke.md`
