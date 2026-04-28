Title: Release Smoke Check
Type: runbook
Layer: operation
Mode: how-to
Scope: repo
Status: active
Owner: release-owner
Source of Truth: no
Related Files: docs/conventions/release-policy.md

# Release Smoke Check

## Prerequisites

- 已确认当前规则仍以 `docs/conventions/release-policy.md` 为准

## Steps

1. 读取当前发布规则
2. 执行 smoke 检查
3. 记录异常或风险

## Verify

- 检查已完成并留有结果记录

## Rollback

- 如果 smoke 失败，停止发布并回到当前稳定版本
