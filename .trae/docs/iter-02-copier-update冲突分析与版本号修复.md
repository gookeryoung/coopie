# iter-02 copier update 冲突分析与版本号修复

## 迭代目标

定位并解决 `coopie -U`（即 `copier update`）作用于项目自身时出现 git 冲突合并提示的问题；顺带修复版本 bump 漏改 `[project] version` 与 bumpversion `search` 无法匹配对齐行的缺陷。

## 根因分析

`copier update` 执行三方合并：base=模板@`_commit` 渲染、theirs=模板@HEAD 渲染、ours=工作树。三方对同一处均不同时产生冲突。

项目 `.copier-answers.yml` 的 `_commit` 停留在 `v0.1.5`，而 HEAD 模板已新增 `initial_version`、`use_cli` 两个变量。于是版本号相关字段在三方各不相同：

- `[tool.bumpversion] current_version`：base=v0.1.5 硬编码 "0.1.5"、theirs=HEAD 渲染 "0.1.8"、ours=bump 后 "0.1.9" → 冲突
- `src/coopie/__init__.py __version__`：同上三方不同 → 冲突

端到端对照实验确认根因：
- Test A（基线 `_commit: v0.1.5`）：`copier update` 产生 UU 冲突（pyproject.toml、__init__.py）。
- Test B（基线 `_commit: v0.1.9`）：`copier update` 无冲突，仅 `.copier-answers.yml` 常规更新。

## 改动文件清单

- `copier.yml`：新增 `initial_version`（默认 "0.1.0"，创建后不再变）与 `use_cli`（默认 false）两个变量，使版本号由模板变量驱动而非硬编码。
- `template/pyproject.toml`：`version`/`current_version` 改用 `{{ initial_version }}`；`[project.scripts]` 由 `{% if use_cli %}` 条件渲染；Jinja 条件标签内联化以消除残留空行；bumpversion `search` 改正则 + 反向引用。
- `.copier-answers.yml`：`_commit` 由 `v0.1.5` 更新至 `v0.1.9`，补 `use_cli: true`。
- `pyproject.toml`（根）：`[project] version` 同步至 "0.1.9"；bumpversion `search` 改正则。
- `src/coopie/__init__.py`：`__version__` → "0.1.9"。
- `uv.lock`：uv 重新锁定（依赖项补环境 marker）。

## 关键决策与依据

1. **新增 `initial_version` 变量**：模板硬编码版本号导致 base/theirs 永远等于"该模板发布时的版本"，与 ours（用户 bump 后的版本）冲突。改为变量后，copier 渲染始终用 `.copier-answers.yml` 中固化的 `initial_version`，base==theirs，copier 保留 ours。
2. **`_commit` 升级到 v0.1.9**：v0.1.5 模板不含新变量，copier 视其为"新问题"且 base 缺失对应渲染。升到含新变量的 v0.1.9 后 base 与 theirs 同源，冲突消失。
3. **bumpversion `search` 改正则**：原 `search = 'version = "{current_version}"'`（单空格）匹配不上对齐后的 `version         = "0.1.9"`（多空格），导致 bump 时漏改 `[project] version`。改为 `regex = true` + `search = '(version\s+=\s+)"{current_version}"'` + `replace = '\1"{new_version}"'`，反向引用保留对齐缩进；`\b` 语义保证不误匹配 `current_version`。
4. **v0.1.9 tag 移至修复提交**：原 tag 指向的 bump 提交 `[project] version` 仍为 "0.1.8"（漏改），tag 尚未推到远程，本地移动使其指向版本一致的提交，避免发布带缺陷的快照。

## 验证结果

- `ruff check` / `ruff format --check` / `pyrefly check`：全绿。
- `pytest -m "not slow" --cov`：21 passed，覆盖率 100%（未下降）。
- `bump-my-version bump --dry-run`（根项目 + 渲染产物）：正则匹配到对齐版本行，三处版本号（`[project] version`、`current_version`、`__version__`）均正确 bump，对齐格式保留。
- 真实项目 `copier update --trust -A`：无冲突、无冲突标记，仅 `.copier-answers.yml` 一处 copier 的 YAML 引号归一化（验证副产品，已回退）。

## 遗留事项

- `copier update` 会把 `initial_version: '0.1.8'` 归一化为不带引号的 `0.1.8`（YAML 仍解析为字符串），属 copier 行为，每次更新都会产生该 1 行差异；非缺陷，按需接受或提交。
- bump-my-version 在 Python 3.8 报 `dict |=` 不兼容（3.9+ 语法），项目 `uv run` 锁定 3.8 故未装该工具；3.9+ 环境可用 `uvx bump-my-version` 正常工作。
