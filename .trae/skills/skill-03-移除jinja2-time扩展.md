# iter-03 移除 jinja2-time 扩展

## 迭代目标

消除 `copier update` 的 `jinja_extensions` 不安全警告与 `jinja2_time` 模块缺失错误，改用 copier 内置 `now()` 函数获取版权年份，使 `coopie -U`（即 `uvx copier update`）无需 `--trust` 与 `--with jinja2-time` 即可正常工作。

## 根因分析

`copier.yml` 声明了 `_jinja_extensions: ["jinja2_time.TimeExtension"]`，模板内 LICENSE 与 docs/conf.py 用 `{% now 'utc', '%Y' %}` 取当前年份。copier 视 `_jinja_extensions` 为潜在不安全特性，要求 `--trust`；而 `jinja2_time` 并非 copier 默认依赖，用户未单独安装时报 `No module named 'jinja2_time'`。

copier 向 Jinja 上下文注入了内置 `now` 函数（调用返回当前 `datetime`），`{{ now().year }}` 可完全替代 `jinja2_time.TimeExtension` 的 `{% now 'utc', '%Y' %}`，且不触发 unsafe 警告、无需额外依赖。

## 过渡迁移问题

移除 `_jinja_extensions` 后，coopie 项目自身 `.copier-answers.yml` 的 `_commit` 仍为 v0.1.9（base 模板含 jinja2-time）。`copier update` 渲染 base@v0.1.9 时仍需 jinja2-time，干净命令必然失败——这正是用户报错的根因。

解决方案：发 v0.1.10（jinja2-time-free 发布点），用一次性 `uvx --with jinja2-time copier update --trust -A` 把 coopie 迁移到 v0.1.10，此后干净命令可用。迁移时三方合并无冲突：base@v0.1.9 与 theirs@v0.1.10 渲染 LICENSE/conf.py 的年份同为 2026，ours 保持已渲染值。

## 改动文件清单

- `copier.yml`：移除 `_jinja_extensions` 配置块。
- `template/{% if license != 'None' %}LICENSE{% endif %}`：2 处 `{% now 'utc', '%Y' %}` → `{{ now().year }}`。
- `template/{% if use_docs %}docs{% endif %}/conf.py`：1 处 `{% now 'utc', '%Y' %}` → `{{ now().year }}`。
- `src/coopie/cli.py`：update 命令改为 `["uvx", "copier", "update"]`（移除 `--with jinja2-time` 与 `--trust`）；copy 命令同步清理。
- `tests/test_cli.py`：`test_main_update` 断言匹配新命令。
- `README.md`：移除 jinja2-time/--trust 相关文档。
- `pyproject.toml`（根）：版本 bump 至 0.1.10。
- `src/coopie/__init__.py`：`__version__` → "0.1.10"。
- `.copier-answers.yml`：`_commit` 由 v0.1.9 迁移至 v0.1.10。

## 关键决策与依据

1. **改用 copier 内置 `now()`**：`now()` 是 copier 注入 Jinja 上下文的内置函数，不依赖 `_jinja_extensions`，不触发 unsafe 警告，无需额外安装包。相比 `jinja2_time.TimeExtension` 更安全、依赖更少。
2. **发 v0.1.10 作为迁移发布点**：coopie 的 `_commit` 是 v0.1.9（含 jinja2-time），必须有一个不含 jinja2-time 的发布点作为迁移目标。v0.1.10 tag 指向 jinja2-time-free 的提交，`copier update` 从远程 GitHub `_src_path` 拉取，须先推送 tag。
3. **一次性迁移命令带 jinja2-time**：迁移时 base@v0.1.9 模板仍含 `_jinja_extensions` 与 `{% now %}`，渲染 base 需要 jinja2-time。用 `uvx --with jinja2-time copier update --trust -A` 一次性完成，迁移后 `_commit` 变为 v0.1.10，后续干净命令渲染 base@v0.1.10 不再需要 jinja2-time。
4. **迁移无冲突的依据**：LICENSE 与 conf.py 的年份字段在 base@v0.1.9（`{% now %}` 渲染）与 theirs@v0.1.10（`now().year` 渲染）同为 "2026"，ours 保持已渲染值，三方一致；版本号字段 base==theirs（同为 `initial_version` 渲染值），ours 为 bump 后值，copier 保留 ours。

## 验证结果

- `ruff check` / `ruff format --check` / `pyrefly check`：全绿。
- `pytest -m "not slow" --cov`：21 passed，覆盖率 100%。
- 一次性迁移 `uvx --with jinja2-time copier update --trust -A`：无冲突，仅 `.copier-answers.yml` 变更（`_commit` v0.1.9→v0.1.10 + copier YAML 引号归一化）。
- 干净命令 `uvx copier update -A`（无 jinja2-time 无 --trust）：exit 0，"Keeping template version 0.1.10"，无 unsafe 警告、无模块缺失错误。

## 遗留事项

- copier 对 `now()` 发出 `FutureWarning`：`now` 将在未来版本移除，建议改用 `{{ '%Y' | strftime }}`。当前仍可用，待 copier 正式移除 `now()` 时再迁移。
- `copier update` 的 YAML 引号归一化（`initial_version: '0.1.8'` → `0.1.8`）每次更新产生 1 行差异，属 copier 行为，非缺陷。
