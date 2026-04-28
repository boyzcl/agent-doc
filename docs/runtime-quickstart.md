# agent-doc Runtime Quickstart

## Purpose

这份文档给出 `agent-doc` 本地 runtime 演化层的最小真实宿主操作链路。

目标不是解释设计理念，而是让你能在一个已支持的宿主上实际完成：

1. 初始化 runtime root
2. 写入一条最小 capture
3. 读取最近经验
4. 触发一次本地 promotion
5. 查看 governance 与 repo candidate 状态

## Before You Start

默认 `Codex` runtime root：

- `~/.codex/skills/agent-doc/runtime/`

其他宿主仍处于实验态：

- `Claude Code`: `~/.claude/skills/agent-doc/runtime/`
- `OpenClaw`: `~/.openclaw/skills/agent-doc/runtime/`

如果你要在临时目录验证，始终优先显式传 `--root`。

## Sample Capture

仓库自带一个脱敏 sample：

- [examples/runtime-memory-cli-sample.json](/Users/boyzcl/Documents/A/Agent规范/agent-doc/examples/runtime-memory-cli-sample.json)

第一次使用前，至少替换：

- `timestamp`
- `session_id`

## Minimal Real-Host Flow

在 `agent-doc` 仓库根目录执行：

```bash
python3 scripts/init_runtime_memory.py --host codex
python3 scripts/validate_runtime_memory.py --host codex
python3 scripts/write_runtime_capture.py --host codex --record-file examples/runtime-memory-cli-sample.json
python3 scripts/read_runtime_context.py --host codex --scene runtime-host-validation --doc-type skill-readme --limit 3
python3 scripts/promotion_worker.py --host codex --limit 2 --trigger-source runtime_quickstart
python3 scripts/runtime_governance_report.py --host codex
python3 scripts/review_repo_candidates.py --host codex
```

## Temporary Root Flow

如果不想先写入默认宿主目录，可以先用临时 root：

```bash
TMP_ROOT="$(mktemp -d)"
python3 scripts/init_runtime_memory.py --host codex --root "$TMP_ROOT"
python3 scripts/validate_runtime_memory.py --host codex --root "$TMP_ROOT"
python3 scripts/write_runtime_capture.py --host codex --root "$TMP_ROOT" --record-file examples/runtime-memory-cli-sample.json
python3 scripts/promotion_worker.py --host codex --root "$TMP_ROOT" --limit 1 --trigger-source runtime_quickstart
python3 scripts/runtime_governance_report.py --host codex --root "$TMP_ROOT"
```

## Expected Artifacts

一轮最小链路结束后，通常会看到：

- `captures/YYYY-MM-DD.jsonl`
- `index/by-scene.json`
- `index/by-doc-type.json`
- `inbox/review-queue.json`
- `promoted/field-notes/*.md`
- `promoted/repo-candidates/*.md`
- `state/promotion-ledger.json`
- `state/reuse-ledger.json`

## Safe Usage Rules

- 不要把 runtime root 指到仓库工作副本里
- 不要把 raw capture jsonl 提交到公开仓库
- 不要在 capture 中写入私有绝对路径或私有业务长原文
- `repo candidate` 只是候选，不是自动发布

## Verification Shortcut

如果只想先确认脚本闭环可跑：

```bash
python3 scripts/smoke_test_runtime_memory.py
```

它会在临时目录里跑完初始化、capture、读取、promotion 和治理报告。
