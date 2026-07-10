# skill-05：Makefile 快捷命令封装（iter-05 归档）

## 迭代目标

为项目根和模板各创建 Makefile，封装 build/clean/test/cov/lint/typecheck/check/doc/tox/bump 等常用操作，提供 `make help` 自助文档；支持别名（`b`/`c`）与条件渲染（`use_docs`/`use_tox`）。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `Makefile` | 新建 | 项目根 Makefile，固定 `coopie`/`95` |
| `template/Makefile` | 新建 | 模板 Makefile，Jinja 渲染 `package_name`/`coverage_fail_under`，`{% if use_docs %}`/`{% if use_tox %}` 条件渲染 `doc`/`tox` 目标 |
| `tests/test_cli.py` | 修改 | 新增 `test_main_update_skip_answered`/`test_main_update_skip_tasks` 覆盖 commit d5c2ea5 引入的 `--skip-answered`/`--skip-tasks` 参数 |
| `template/README.md` | 修改 | 新增"Make 快捷命令"段；文档构建与 tox 命令简化为 `make doc`/`make tox` |
| `README.md` | 修改 | 生成文件清单加入 `Makefile` 行 |
| `pyproject.toml` / `src/coopie/__init__.py` | bump | 0.1.11 → 0.1.12 |
| `.copier-answers.yml` | 迁移 | `_commit: v0.1.11 → v0.1.12` |
| `.trae/rules/rule-01-开发流程.md` | 同步 | 从模板同步"需求分析"段（迭代前确认需求、记录到 `.trae/req/`） |

## 关键决策与依据

1. **help 目标 awk 模式**：原 `/^[a-zA-Z_-]+:.*##/` 不匹配含空格的别名行（`build b:` 中 `build` 后是空格），改为 `/^[a-zA-Z].*:.*##/`（以字母开头，含 `:` 和 `##` 即可）。

2. **模板条件渲染**：`doc`/`tox` 目标用 `{% if use_docs %}`/`{% if use_tox %}` 包裹，`clean` 目标里 `docs/_build/` 路径也条件化，`.PHONY` 列表动态拼接。`_templates_suffix: ""` 使所有文件经 Jinja 渲染，Makefile recipe 的 TAB 缩进被保留。

3. **bump 目标用 `uvx`**：bump-my-version 在 Python 3.8 报 `dict |=` 不兼容，用 `uvx bump-my-version`（自带 3.9+ 环境）。`--tag` 触发自动打 tag。

4. **README 冲突处理**：coopie 项目的 README 是描述模板本身的自定义文档（特性/可配置选项/生成文件清单），与模板 README（面向生成项目：安装/快速上手）完全不同。每次 copier update 改模板 README 时都会整体冲突，需 `git checkout --ours README.md` 保留项目版本。这是结构性问题，无法通过字段驱动解决。

5. **`.python-version` 保持 3.8**：本地工具（uv/pyenv）自动将其改为系统最高版本（3.14），但项目声明支持 3.8+，用 3.14 跑测试可能漏掉 3.8 不兼容代码。恢复为 3.8。

## 验证结果

- `make help`：列出全部目标，含别名 `build b`/`clean c`。
- `make check`（lint + typecheck + cov）：ruff 全绿、pyrefly 0 errors、pytest 23 passed、覆盖率 100%。
- `make build`：生成 wheel + sdist。
- 干净 `uvx copier update -A`：`Keeping template version 0.1.12`，无冲突无错误。

## 提交历史

```
2b2a03a docs: 模板 README 文档构建命令统一为 make doc/make tox
12f598c chore: 迁移 _commit 至 v0.1.12 完成 Makefile 同步
5115914 chore: 同步 uv.lock
3f5fd7b chore: bump version 0.1.11 → 0.1.12  (tag: v0.1.12)
d8e40bd feat: 新增 Makefile 封装 build/test/cov/lint/bump 等快捷命令
```

## 遗留事项

1. **README 冲突**：每次 copier update 改模板 README 时都会整体冲突，需手动 `git checkout --ours README.md`。长期可考虑把模板 README 改名（如 `PROJECT_README.md`）或在 copier.yml 用 `_skip_if_exists` 配置，但会影响生成项目的默认 README。
2. **rule-01 需求分析**：从模板同步的"需求分析"段要求迭代前确认需求并记录到 `.trae/req/`。本次迭代在上下文恢复时承接，未单独创建 req 文档。后续迭代需遵守此规则。
