# skill-07：bump 目标默认 patch（归档自 iter-07）

> 归档时间：2026-07-11（iter-15 时按 rule-01 阈值触发归档）

## 概要

改进 Makefile bump 目标用法：`make bump` 默认 patch，`make bump minor`/`make bump major` 支持位置参数指定级别。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `Makefile` | 修改 | bump 目标改用 `MAKECMDGOALS` 提取位置参数，默认 patch；新增 `patch`/`minor`/`major` 占位目标；补充 `push` 目标 |
| `template/Makefile` | 修改 | 同步 bump 目标改进 |
| `pyproject.toml` / `src/coopie/__init__.py` | bump | 0.1.13 → 0.1.14 |
| `.copier-answers.yml` | 迁移 | `_commit: v0.1.13 → v0.1.14` |

## 关键决策与依据

1. **`MAKECMDGOALS` 提取位置参数**：`make bump minor` 时 `MAKECMDGOALS` 为 `bump minor`，用 `filter-out bump` 提取 `minor`。`$(if $(BUMP_PART),$(firstword $(BUMP_PART)),patch)` 实现"有参数用参数，无参数默认 patch"。
2. **占位目标**：`make bump minor` 同时触发 `bump` 和 `minor` 两个目标。定义 `patch minor major:` 空操作目标（`@:`），避免 Make 报"No rule to make target"。无 `##` 注释不出现在 `make help`。
3. **push 目标同步**：项目根 Makefile 补充 `push` 目标（`git push && git push --tags`）与模板一致。

## 验证结果

- `make -n bump`/`make -n bump minor`/`make -n bump major`：命令正确
- `make help`：bump 显示"版本号 bump (默认 patch，用法: make bump [minor|major])"，patch/minor/major 不显示
- `make check`：ruff/pyrefly/pytest 23 passed，覆盖率 100%
- `uvx copier update -A`：`Keeping template version 0.1.14`，无冲突

## 遗留事项

`template/.python-version` 仍被本地工具自动改为 3.14，每次 copier update 后需 `git checkout --` 恢复为 3.8。
