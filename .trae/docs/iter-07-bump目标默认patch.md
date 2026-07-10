# iter-07：bump 目标默认 patch

## 迭代目标

改进 Makefile bump 目标用法：`make bump` 默认 patch，`make bump minor`/`make bump major` 支持位置参数指定级别。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `Makefile` | 修改 | bump 目标改用 `MAKECMDGOALS` 提取位置参数，默认 patch；新增 `patch`/`minor`/`major` 占位目标；补充 `push` 目标与模板一致 |
| `template/Makefile` | 修改 | 同步 bump 目标改进（模板已有 push 目标） |
| `.trae/req/req-07-bump目标默认patch.md` | 新建 | 需求分析文档 |
| `pyproject.toml` / `src/coopie/__init__.py` | bump | 0.1.13 → 0.1.14 |
| `.copier-answers.yml` | 迁移 | `_commit: v0.1.13 → v0.1.14` |

## 关键决策与依据

1. **`MAKECMDGOALS` 提取位置参数**：`make bump minor` 时 `MAKECMDGOALS` 为 `bump minor`，用 `filter-out bump` 提取 `minor`。`$(if $(BUMP_PART),$(firstword $(BUMP_PART)),patch)` 实现"有参数用参数，无参数默认 patch"。

2. **占位目标**：`make bump minor` 会同时触发 `bump` 和 `minor` 两个目标。定义 `patch minor major:` 空操作目标（`@:`），避免 Make 报"No rule to make target"。这些目标无 `##` 注释，不出现在 `make help`。

3. **push 目标同步**：模板 Makefile 已有 `push` 目标（commit 54cd93c，用户手动添加），项目根 Makefile 补充相同目标保持一致，避免 copier update 时不一致。

## 验证结果

- `make -n bump`：`uvx bump-my-version bump patch --tag`（默认 patch）
- `make -n bump minor`：`uvx bump-my-version bump minor --tag` + `:`（minor 占位空操作）
- `make -n bump major`：`uvx bump-my-version bump major --tag` + `:`（major 占位空操作）
- `make help`：bump 显示"版本号 bump (默认 patch，用法: make bump [minor|major])"，push 显示"推送代码到远程仓库"，patch/minor/major 不显示
- `make bump` 实际执行：成功 bump 0.1.13 → 0.1.14（默认 patch 验证通过）
- `make check`：ruff/pyrefly/pytest 23 passed，覆盖率 100%
- 干净 `uvx copier update -A`：`Keeping template version 0.1.14`，无冲突（Makefile push 目标有空白冲突，已解决）

## 提交历史

```
b8f33dd chore: 迁移 _commit 至 v0.1.14 完成 bump 目标改进同步
3ce90d6 chore: bump version 0.1.13 → 0.1.14  (tag: v0.1.14)
b032ccf feat: Makefile bump 目标默认 patch，支持位置参数
54cd93c build(template): add push target to Makefile  (用户手动提交)
```

## 遗留事项

无新增遗留事项。`template/.python-version` 仍被本地工具自动改为 3.14，每次 copier update 后需 `git checkout --` 恢复为 3.8。
