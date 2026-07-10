# iter-01 模板修复与 CLI 完善

## 迭代目标

修复 coopier 模板渲染的结构性缺陷与版本泄漏，补全 .gitignore 安全缺口，完善 CLI（返回注解/常量/--version）。

## 改动文件清单

- `template/pyproject.toml`：重构 `[build-system]`/`[tool.uv]`/`[[tool.uv.index]]` 结构，使前两者无条件保留、仅镜像表受 `use_domestic_mirrors` 控制；初始版本 `0.1.5`→`0.1.0`。
- `template/src/{{ package_name }}/__init__.py`：`__version__` `0.1.5`→`0.1.0`。
- `template/.gitignore`、`.gitignore`（根）：补 `.env`/`.env.*`、`htmlcov/`、`coverage.xml`、`.tox/`、`.ruff_cache/`、`.pyrefly_cache/`、`.mypy_cache/`、`.uv-cache/`。
- `.copier-answers.yml`：移除 `copier.yml` 未定义的死配置 `pypi_token_secret`。
- `src/coopie/cli.py`：`main()` 补 `-> None` 返回注解；提取 `_TEMPLATE_REPO` 模块常量；新增 `-V/--version`。
- `tests/test_cli.py`：新增 `--version` 长/短选项测试。
- `pyproject.toml`（根）：uv sync 自动规范化的一处空行。

## 关键决策与依据

1. **模板 pyproject 结构重构**：原模板把 `build-backend`/`requires`/`required-version` 包进 `{% if use_domestic_mirrors %}`，导致 `false` 取值下 `[build-system]` 失去构建后端、`default`/`url` 成为 `[build-system]` 孤儿键且仍引用国内镜像。依据：`use_domestic_mirrors` 应只控制镜像源表，不波及构建元数据。
2. **模板版本回退 0.1.0**：模板硬编码了 coopie 自身的 `0.1.5`，新生项目应从 `0.1.0` 起；`conf.py` 的 ImportError 回退值已是 `0.1.0`，印证此意图。
3. **`--version` 用 `action="version"`**：argparse 内建行为，自动打印并 `exit(0)`，无需手写校验逻辑，且先于互斥/缺参校验生效。
4. **测试用 `cli.__version__` 而非裸 `__version__` 导入**：ruff F821 无法解析从 `__init__.py` 导入的变量名，改用模块属性访问规避。

## 验证结果

- `ruff check` / `ruff format --check` / `pyrefly check`：全绿。
- `pytest -m "not slow" --cov`：21 passed，覆盖率 100%（基线 100%，未下降）。
- 模板渲染校验：用 copier 对 `use_domestic_mirrors` 两种取值渲染（非 git 副本，避免 copier 读 HEAD），`tomllib` 解析两份产物均合法：true 含镜像表、false 不含孤儿键与镜像引用。

## 遗留事项

- `copier copy` 从 git 仓库源读取 HEAD 而非工作树，模板本地改动需提交后才在 `copier copy <repo>` 流程生效；本次用非 git 副本完成验证。提交后流程自然一致。
- 模板根 Dockerfile 的基础镜像（`docker.m.daocloud.io`）未条件化，属设计选择（注释提示可替换），非缺陷。
