# skill-09：修复 GitHub Actions Node.js 20 弃用警告（归档自 iter-09）

> 归档时间：2026-07-11（iter-15 时按 rule-01 阈值触发归档）

## 概要

GitHub Actions 运行时报告 `astral-sh/setup-uv@v6` 使用已弃用的 Node.js 20。升级到官方推荐的 `@v8`（Node.js 24），实际用 `@v8.3.2` 完整版本号标签。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `.github/workflows/ci.yml` | 修改 | `setup-uv@v6 → @v8.3.2`（2 处） |
| `.github/workflows/release.yml` | 修改 | `setup-uv@v6 → @v8.3.2`（1 处） |
| `template/{% if use_cicd %}.github{% endif %}/workflows/ci.yml` | 修改 | 同步（2 处） |
| `template/{% if use_cicd %}.github{% endif %}/workflows/release.yml` | 修改 | 同步（1 处） |
| `pyproject.toml` / `src/coopie/__init__.py` | bump | 0.2.0 → 0.2.1 → 0.2.2（首次 @v8 标签错误，修正为 @v8.3.2） |
| `.copier-answers.yml` | 迁移 | `_commit: v0.1.14 → v0.2.1 → v0.2.2` |

## 关键决策与依据

1. **升级到 @v8 而非 @v7**：官方文档示例用 `@v8`（Node.js 24）。
2. **仅升级 setup-uv**：用户报告只有 `setup-uv@v6` 有 Node.js 20 警告，`actions/checkout@v5` 未被报告，不主动升级未出问题的 action。
3. **项目根与模板同步**：6 处 `setup-uv@v6` 全部替换。
4. **@v8 标签错误**：首次用 `@v8` 滚动标签，CI 报错 "unable to find version `v8`"——setup-uv 只有完整版本号标签（immutable），无 major 滚动标签。修正为 `@v8.3.2`。

## 验证结果

- `make check`：ruff/pyrefly/pytest 23 passed，覆盖率 100%
- `uvx copier update -A`（迁移 v0.1.14→v0.2.2）：无冲突
- 干净 `uvx copier update -A`：`Keeping template version 0.2.2`，工作树干净

## 遗留事项

- `actions/checkout@v5` 和 `actions/setup-python` 未被报告 Node.js 20 警告，暂不升级。
- `astral-sh/setup-uv` 无 major 滚动标签（v6/v8），只有完整版本号标签（v8.3.2）。后续升级需指定完整版本号。
- bump 时发现 `.readthedocs.yaml` 被本地工具自动改为 Python 3.13（应保持 3.8），`git checkout --` 恢复。
