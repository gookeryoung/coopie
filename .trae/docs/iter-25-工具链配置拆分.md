# iter-25：工具链配置拆分到独立文件

## 需求清单

- [x] 将 `template/pyproject.toml` 中 ruff/pytest/coverage/pyrefly/bumpversion/uv 配置拆到 6 个独立文件
- [x] `template/pyproject.toml` 仅保留项目元数据 + build-system + hatch + dependency-groups
- [x] `copier.yml` 添加 `_skip_if_exists` 列表
- [x] 同步更新 rule-11、python-testing SKILL、rule-01、Dockerfile、CI render job
- [x] 验证：ruff/pyrefly/pytest 全绿 + 渲染测试 6 个独立文件内容正确

## 迭代目标

解决 `copier update` 覆盖项目自身配置（版本号、Python 版本、README 等）的问题。方案：将工具链配置从 `pyproject.toml` 拆到 6 个独立文件（ruff.toml/pytest.ini/.coveragerc/pyrefly.toml/.bumpversion.toml/uv.toml），并在 `copier.yml` 用 `_skip_if_exists` 标记 `pyproject.toml` 等项目自身配置文件。这样 `copier update` 时：工具链文件随模板更新，项目元数据文件被跳过保留用户修改。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `template/ruff.toml` | 新建 | ruff 配置（顶层键，`target-version = "{{ target_py }}"`） |
| `template/pytest.ini` | 新建 | pytest 配置（`[pytest]` 段，markers + testpaths） |
| `template/.coveragerc` | 新建 | coverage 配置（`source = {{ package_name }}`、`fail_under = {{ coverage_fail_under }}`） |
| `template/pyrefly.toml` | 新建 | pyrefly 配置（`python-version = "{{ min_python_version }}"`） |
| `template/.bumpversion.toml` | 新建 | bump-my-version 配置（保留 `[tool.bumpversion]` 前缀，`current_version = "0.1.0"`，同步 pyproject.toml 与 `src/{{ package_name }}/__init__.py`） |
| `template/uv.toml` | 新建 | uv 配置（`required-version`，可选国内镜像源 `[[index]]`） |
| `template/pyproject.toml` | 修改 | 移除 `[tool.uv]`/`[tool.coverage.*]`/`[tool.pytest.ini_options]`/`[tool.ruff*]`/`[tool.pyrefly]`/`[tool.bumpversion*]`，仅保留 `[project]`/`[project.optional-dependencies]`/`[project.scripts]`/`[build-system]`/`[tool.hatch.*]`/`[dependency-groups]` |
| `copier.yml` | 修改 | `_message_before_copy` 描述新结构；新增 `_skip_if_exists`（pyproject.toml/.python-version/README.md/LICENSE/src/*/__init__.py） |
| `template/.trae/rules/rule-11-python-standards.md` | 修改 | 工具链章节标题改为"独立配置文件"，表格新增"配置文件"列 |
| `template/.trae/rules/rule-01-开发流程.md` | 修改 | 暂停条件第 2 条"修改 pre-commit/pyproject.toml 工具链配置"改为"修改 pre-commit/工具链配置文件（ruff.toml/pytest.ini/.coveragerc/pyrefly.toml/.bumpversion.toml/uv.toml）" |
| `.trae/rules/rule-01-开发流程.md` | 修改 | 根目录 rule-01 同步上述暂停条件变更（与 template/ 保持一致） |
| `template/.trae/skills/python-testing/SKILL.md` | 修改 | 标记注册示例改 `pytest.ini`；测试配置章节改用 `pytest.ini` + `.coveragerc`；覆盖率配置示例改 `.coveragerc` |
| `template/{% if use_docker %}Dockerfile{% endif %}` | 修改 | `COPY pyproject.toml` → `COPY pyproject.toml uv.toml`（uv sync 读取 uv.toml） |
| `.github/workflows/ci.yml` | 修改 | render job 新增 6 个独立文件的 `test -f` 验证 |
| `.trae/req/req-25-工具链配置拆分.md` | 新建 | 需求记录 |
| `.trae/docs/iter-25-工具链配置拆分.md` | 新建 | 本迭代记录 |

## 关键决策与依据

### 1. 拆分工具链到独立文件而非 `_skip_if_exists` 跳过整个 pyproject.toml

- **依据**：用户反馈"`copier update` 把现有项目的版本信息全搞乱了"。若直接对 `pyproject.toml` 加 `_skip_if_exists`，模板对 `[build-system]`/`[tool.hatch]` 等结构的演进也无法传递给用户项目。拆分后，`pyproject.toml` 只剩项目元数据（版本号、作者、依赖），可安全跳过；工具链配置独立成文件，随模板更新
- **实现**：6 个独立文件分别承载 ruff/pytest/coverage/pyrefly/bumpversion/uv 配置，`pyproject.toml` 仅保留项目元数据与构建配置

### 2. `.bumpversion.toml` 保留 `[tool.bumpversion]` 前缀

- **依据**：bump-my-version 官方文档明确要求 `.bumpversion.toml` 必须使用 `[tool.bumpversion]` 前缀（与其他工具的独立文件无 `tool.` 前缀不同）。测试验证：去掉前缀后 bump-my-version 无法识别配置
- **实现**：`.bumpversion.toml` 保留 `[tool.bumpversion]` 与 `[[tool.bumpversion.files]]` 前缀

### 3. `uv.toml` 而非 `[tool.uv]` 保留在 pyproject.toml

- **依据**：uv 官方文档说明 `uv.toml` 存在时覆盖 `pyproject.toml [tool.uv]`。将 uv 配置放 `uv.toml` 后，`pyproject.toml` 不再含 `[tool.uv]`，避免 `copier update` 时 uv 配置段参与三方合并
- **实现**：`uv.toml` 含 `required-version` 与可选国内镜像源 `[[index]]`

### 4. `_skip_if_exists` 列表内容

- **依据**：这些文件承载项目自身配置（版本号、Python 版本、README 标题、许可证、包初始化），应由用户独立管理，`copier update` 不应覆盖
- **实现**：`pyproject.toml`、`.python-version`、`README.md`、`LICENSE`、`src/*/__init__.py`。首次 `copier copy` 正常生成，`copier update` 时若已存在则跳过

### 5. `_skip_if_exists` 对首次 copy 与 update 的差异行为

- **依据**：copier 文档说明 `_skip_if_exists` 只在文件已存在时跳过，首次 copy 时文件不存在所以正常生成
- **实现**：用户首次 `coopie init` 正常得到所有文件；后续 `copier update` 时这些文件被跳过，工具链文件正常更新

## 代码实现情况

### 6 个独立配置文件

```toml
# ruff.toml
extend-exclude = ["template"]
line-length    = 120
target-version = "{{ target_py }}"

[lint]
ignore = ["E501", "PLC0415", "PLR0915", "PLR2004", "RUF001", "RUF002", "RUF003", "RUF012", "SIM108"]
select = ["ARG", "B", "C4", "E", "F", "I", "PL", "PTH", "RUF", "SIM", "UP", "W"]

[lint.per-file-ignores]
"**/tests/**" = ["ARG001", "ARG002"]
```

```ini
# pytest.ini
[pytest]
asyncio_default_fixture_loop_scope = function
markers = slow: marks tests as slow (deselect with '-m "not slow"')
testpaths = tests
```

```ini
# .coveragerc
[run]
branch = true
concurrency = thread
omit = tests/*
source = {{ package_name }}

[report]
fail_under = {{ coverage_fail_under }}
exclude_lines =
    if TYPE_CHECKING:
    if __name__ == .__main__.:
    pragma: no cover
    raise NotImplementedError
show_missing = true
```

```toml
# pyrefly.toml
preset           = "strict"
project-excludes = [".venv/**", "template/**"]
project-includes = ["**/*.ipynb", "**/*.py*"]
python-version   = "{{ min_python_version }}"
search-path      = ["."]
```

```toml
# .bumpversion.toml（保留 [tool.bumpversion] 前缀）
[tool.bumpversion]
current_version = "0.1.0"
commit = true
exclude = ["template/*"]
message = "chore: 更新版本 {current_version} → {new_version}"
tag = true
tag_name = "v{new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
regex = true
search = '(version\s+=\s+)"{current_version}"'
replace = '\1"{new_version}"'

[[tool.bumpversion.files]]
filename = "src/{{ package_name }}/__init__.py"
search = '__version__ = "{current_version}"'
replace = '__version__ = "{new_version}"'
```

```toml
# uv.toml
required-version = ">=0.5.0"
{% if use_domestic_mirrors %}[[index]]
default = true
url     = "https://mirrors.aliyun.com/pypi/simple/"

{% endif %}
```

### copier.yml `_skip_if_exists`

```yaml
_skip_if_exists:
  - "pyproject.toml"
  - ".python-version"
  - "README.md"
  - "LICENSE"
  - "src/*/__init__.py"
```

### template/pyproject.toml 精简后

仅含 `[project]`（含 `version = "0.1.0"`）、`[project.optional-dependencies]`、`[project.scripts]`（cli）、`[build-system]`、`[tool.hatch.build.targets.wheel]`、`[dependency-groups]`。

## 整合优化情况

- rule-11 工具链章节表格新增"配置文件"列，与拆分后的文件结构一致
- python-testing SKILL 示例从 `pyproject.toml [tool.pytest.ini_options]` 改为 `pytest.ini`，覆盖率示例从 `pyproject.toml [tool.coverage]` 改为 `.coveragerc`，与新结构一致
- rule-01 暂停条件第 2 条"修改 pre-commit/pyproject.toml 工具链配置"改为"修改 pre-commit/工具链配置文件（ruff.toml/pytest.ini/.coveragerc/pyrefly.toml/.bumpversion.toml/uv.toml）"，与拆分后文件一致
- Dockerfile `COPY` 命令加入 `uv.toml`，确保容器内 `uv sync` 能读取 uv 配置
- CI render job 新增 6 个 `test -f` 验证，确保渲染产物包含所有独立配置文件

## 测试验证结果

```
uv run ruff check           → All checks passed!
uv run ruff format --check  → 4 files already formatted
uv run pyrefly check        → 0 errors
uv run pytest --cov         → 13 passed, coverage 100.00%
```

渲染测试（`uvx copier copy --trust --defaults --vcs-ref HEAD . .preview/test-split`）：

| 文件 | 渲染结果 |
|------|---------|
| `ruff.toml` | `target-version = "py38"`，lint 规则完整 |
| `pytest.ini` | `[pytest]` 段，markers + testpaths |
| `.coveragerc` | `source = my_project`，`fail_under = 95` |
| `pyrefly.toml` | `python-version = "3.8"`，`project-excludes` 含 template/** |
| `.bumpversion.toml` | `current_version = "0.1.0"`，`filename = "src/my_project/__init__.py"` |
| `uv.toml` | `required-version = ">=0.5.0"`，国内镜像 `[[index]]` 段 |
| `pyproject.toml` | 仅项目元数据 + build-system + hatch + dependency-groups，`version = "0.1.0"`，无任何 `[tool.*]` 工具链配置 |

## 遗留事项

- coopie 自身 `pyproject.toml`（仓库根，非模板）仍用 `[tool.*]` 内联配置，未拆分到独立文件。coopie 自身不是用 `copier update` 管理的（它是模板仓库本身），无 update 覆盖风险，按"不过度工程化"原则保持现状

## 下一轮计划

无。本次迭代已完整覆盖"工具链配置拆分到独立文件"的所有需求，全套门禁全绿，渲染测试 6 个独立文件内容正确。等待用户反馈或新需求。
