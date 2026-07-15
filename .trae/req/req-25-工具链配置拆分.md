# req-25：工具链配置拆分到独立文件

## 背景

`copier update` 时，coopie 模板与用户项目对 `pyproject.toml` 的三方合并容易把项目自身配置（版本号、Python 版本、README 标题等）覆盖回模板默认值。根因是 `pyproject.toml` 既承载项目元数据（版本号、作者、依赖），又承载工具链配置（ruff/pytest/coverage/pyrefly/bumpversion/uv）。工具链配置随模板演进需更新，而项目元数据应由用户独立管理，二者混在一个文件导致 `copier update` 无法精确跳过项目元数据段。

## 需求

- [x] 将 `template/pyproject.toml` 中的 ruff/pytest/coverage/pyrefly/bumpversion/uv 配置拆到独立文件
  - [x] `ruff.toml`（顶层键，无 `[tool.ruff]` 前缀）
  - [x] `pytest.ini`（INI 格式，`[pytest]` 段）
  - [x] `.coveragerc`（INI 格式，`[run]`/`[report]` 段，无 `tool.` 前缀）
  - [x] `pyrefly.toml`（顶层键）
  - [x] `.bumpversion.toml`（保留 `[tool.bumpversion]` 前缀，bump-my-version 强制要求）
  - [x] `uv.toml`（顶层键；uv.toml 存在时覆盖 pyproject.toml `[tool.uv]`）
- [x] `template/pyproject.toml` 仅保留项目元数据 + build-system + hatch + dependency-groups
- [x] `copier.yml` 添加 `_skip_if_exists` 列表，update 时跳过项目自身配置文件
  - `pyproject.toml`、`.python-version`、`README.md`、`LICENSE`、`src/*/__init__.py`
- [x] 同步更新 rule-11（工具链章节指向独立文件）、python-testing SKILL（示例改用 pytest.ini/.coveragerc）、rule-01（暂停条件提及工具链配置文件）、Dockerfile（COPY uv.toml）、CI render job（验证 6 个新文件）
- [x] 验证：ruff/pyrefly/pytest 全绿 + 渲染测试 6 个独立文件内容正确
