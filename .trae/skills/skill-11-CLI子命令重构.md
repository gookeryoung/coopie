# skill-11：CLI 子命令重构（归档自 iter-11）

> 归档时间：2026-07-11（iter-15 时按 rule-01 阈值触发归档）

## 概要

将 coopie CLI 从旧接口（`coopie <name>` + `coopie -U`）完全迁移到子命令模式（`new`/`init`/`update`/`test`），提升用户体验和命令可读性。

## 改动文件清单

| 文件 | 改动 |
|------|------|
| `src/coopie/cli.py` | 完全重写为子命令模式（new/init/update/test），使用 dispatch dict 消除不可达分支 |
| `tests/test_cli.py` | 完全重写，34 个测试覆盖所有子命令分支 |
| `README.md` | 用法段更新为子命令模式，CLI 选项表改为子命令表 |
| `docs/index.rst` | 用法段同步更新为子命令模式（RST 格式） |
| `pyproject.toml` / `src/coopie/__init__.py` | bump 0.2.3 → 0.2.4 |
| `.copier-answers.yml` | 迁移 `_commit: v0.2.2 → v0.2.3` |

## 关键决策与依据

1. **完全迁移**：移除旧接口（`coopie <name>` 和 `coopie -U`），只支持子命令模式。
2. **init 确认后生成**：非空目录时提示用户确认（y/N），默认取消。
3. **test 命令用 --pretend**：`copier update --pretend` 是 dry-run，不修改文件，适合"模拟检查冲突"。
4. **dispatch dict 替代 if/elif 链**：if/elif 链的最后一个 `elif` 产生不可达的隐式 else 分支（argparse 保证 command 是 4 个子命令之一），改用 `dict[str, Callable]` dispatch 消除此分支，覆盖率从 99% 恢复到 100%。
5. **init 的 project_name 派生**：从 `Path.cwd().name` 获取当前目录名作为 project_name，copier 自动派生 package_name。

## 命令设计

```
coopie new <project_name>     # 新建项目到子目录
coopie init                   # 在当前目录初始化（project_name 从目录名派生）
coopie update [-A] [-T]       # 更新已有项目模板
coopie test [-A] [-T]         # 模拟检查更新冲突（dry-run）
coopie -V / --version         # 显示版本号
```

- `-A` / `--skip-answered`：跳过所有问题（使用上次答案）
- `-T` / `--skip-tasks`：跳过所有任务

## 验证结果

- ruff/pyrefly：全绿，0 errors
- pytest：34 passed，覆盖率 100%
- copier update：无冲突（Keeping template version 0.2.2）

## 遗留事项

无。
