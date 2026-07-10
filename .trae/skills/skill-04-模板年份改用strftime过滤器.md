# iter-04 模板年份改用 strftime 过滤器

## 迭代目标

解决 iter-03 遗留的 copier `FutureWarning`：`now()` 函数将在未来版本移除，模板改用 `{{ '%Y' | strftime }}` 获取版权年份，使模板不依赖已弃用的 `now()`。

## 根因分析

iter-03 将 `jinja2_time.TimeExtension` 的 `{% now 'utc', '%Y' %}` 替换为 copier 内置 `{{ now().year }}`，消除了 unsafe 警告。但 copier 随后对 `now()` 发出 `FutureWarning`，提示将在未来版本移除，建议改用 `{{ '%Y-%m-%d %H:%M:%S' | strftime }}`。

`strftime` 是 copier 提供的 Jinja 过滤器，接收 strftime 格式字符串，返回格式化的当前时间字符串。`{{ '%Y' | strftime }}` 返回当前年份（如 "2026"），与 `now().year` 等价。

补充发现：`FutureWarning` 由 copier 的 `_user_data.py` 在向 Jinja 上下文注入 `now` 函数时发出，与模板是否调用 `now()` 无关。即模板改用 `strftime` 后，copier 在渲染模板时仍会发出该警告（因其仍注入 `now` 供向后兼容）。但模板本身已不依赖 `now()`，当 copier 正式移除 `now()` 时模板不受影响。

## 改动文件清单

- `template/{% if license != 'None' %}LICENSE{% endif %}`：2 处 `{{ now().year }}` → `{{ '%Y' | strftime }}`。
- `template/{% if use_docs %}docs{% endif %}/conf.py`：1 处 `{{ now().year }}` → `{{ '%Y' | strftime }}`。
- `pyproject.toml`（根）：版本 bump 至 0.1.11。
- `src/coopie/__init__.py`：`__version__` → "0.1.11"。
- `.copier-answers.yml`：`_commit` 由 v0.1.10 迁移至 v0.1.11。

## 关键决策与依据

1. **改用 `strftime` 过滤器**：`{{ '%Y' | strftime }}` 是 copier 官方推荐的 `now()` 替代方案，返回当前年份字符串，与 `now().year` 渲染结果一致。模板不再依赖已弃用的 `now()`，未来 copier 移除 `now()` 时无需再迁移。
2. **非 git 副本验证**：用 `rsync --exclude='.git'` 创建副本，`copier copy` 验证 `strftime` 渲染为 "2026" 且无 FutureWarning（模板层面），确认过滤器可用后再改正式模板。
3. **迁移无冲突**：base@v0.1.10 与 theirs@v0.1.11 渲染 LICENSE/conf.py 的年份同为 "2026"，ours 保持已渲染值，三方一致，无冲突。

## 验证结果

- 非 git 副本 `copier copy`：`strftime` 正确渲染年份 "2026"，模板层面无 FutureWarning。
- `ruff check` / `ruff format --check` / `pyrefly check`：全绿。
- `pytest -m "not slow" --cov`：21 passed，覆盖率 100%。
- 一次性迁移 `uvx copier update -A`（v0.1.10→v0.1.11）：无冲突，仅 `.copier-answers.yml` 的 `_commit` 变更。
- 干净命令 `uvx copier update -A`（v0.1.11 base）：exit 0，"Keeping template version 0.1.11"。

## 遗留事项

- copier 渲染模板时仍发出 `now()` 的 `FutureWarning`（来自 `_user_data.py` 注入 `now` 函数，与模板用法无关）。这是 copier 运行时行为，模板层面无法消除；待 copier 正式移除 `now()` 后警告自然消失。模板已不依赖 `now()`，移除后不受影响。
