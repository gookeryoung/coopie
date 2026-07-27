# req-23：恢复 cli 工具

## 背景

iter-22 将 coopie 改为纯 copier 模板仓库，移除了 CLI 工具与 PyPI 发布。用户现需恢复 CLI 工具，提供两个命令封装 copier 调用，简化模板使用：

- `coopie init <dest>`：调用 `copier copy --trust` 创建新项目
- `coopie update [dest]`：调用 `copier recopy --trust` 更新已有项目

经确认的决策：
- 分发方式：PyPI 包（恢复 `[build-system]`/`[project.scripts]`/PyPI 发布流程）
- CLI 框架：Typer（类型注解驱动，与 rule-11 类型注解要求契合）
- 模板源：提供 `--url` 参数，默认 Gitee 国内源，支持 GitHub 源

## 需求

- [x] 恢复 `src/coopie/` 包结构（`__init__.py` + `py.typed`）
- [x] 实现 `src/coopie/cli.py`：Typer app + `init`/`update` 两个命令
- [x] `init` 命令：封装 `copier copy --trust`，支持 `--url`/`--vcs-ref`/`--defaults`
- [x] `update` 命令：封装 `copier recopy --trust`，默认当前目录，校验 `.copier-answers.yml`
- [x] 恢复 `tests/` 并编写 CLI 测试（13 个用例，覆盖率 100%）
- [x] 重构 `pyproject.toml`：恢复 build-system/scripts/hatch/pytest/coverage 配置
- [x] `requires-python` 从 `>=3.8` 升至 `>=3.9`（copier 9 最低要求）
- [x] 依赖 `copier>=9.0.0` + `jinja2-time>=0.2.0` + `typer>=0.12.0`
- [x] 更新 CI 工作流：新增 test job，lint job 扩展为全量检查
- [x] 更新 release.yml：恢复 PyPI 发布（OIDC trusted publishing）
- [x] 更新 Makefile：新增 `test`/`cov`/`build` 目标
- [x] 更新 README.md 与 docs/：新增 CLI 使用说明
- [x] bump-my-version 新增 `src/coopie/__init__.py` 版本同步
- [x] 重新生成 `uv.lock`
- [x] ruff check / ruff format --check / pyrefly / pytest --cov 全绿
- [x] 更新 `.trae/docs/iter-23-*.md` 迭代记录
