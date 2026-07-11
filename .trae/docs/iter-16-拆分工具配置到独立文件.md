# iter-16：拆分工具配置到独立文件

## 迭代目标

解决 `copier update` 时 pyproject.toml 行级三方合并不理解 TOML 语义、覆盖用户定制内容的问题。将工具配置从 pyproject.toml 拆分到独立文件，pyproject.toml 加入 `_skip_if_exists` 使 copier 不再覆盖。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `template/pyproject.toml` | 修改 | 移除 [tool.ruff/pyrefly/coverage/pytest] 四个工具配置段 |
| `template/ruff.toml` | 新建 | Ruff 独立配置（TOML，Jinja 渲染 target_py） |
| `template/pyrefly.toml` | 新建 | Pyrefly 独立配置（TOML，Jinja 渲染 min_python_version） |
| `template/.coveragerc` | 新建 | Coverage 独立配置（INI，Jinja 渲染 package_name/coverage_fail_under） |
| `template/pytest.ini` | 新建 | Pytest 独立配置（INI，无 Jinja 变量） |
| `copier.yml` | 修改 | 新增 `_skip_if_exists: [pyproject.toml]` |
| `pyproject.toml`（项目根） | 修改 | 移除四个工具配置段，保留 [project]/[build-system]/[tool.uv]/[tool.hatch]/[dependency-groups]/[tool.bumpversion] |
| `ruff.toml`（项目根） | 新建 | 渲染后的 Ruff 配置（target-version = "py38"） |
| `pyrefly.toml`（项目根） | 新建 | 渲染后的 Pyrefly 配置（python-version = "3.8"） |
| `.coveragerc`（项目根） | 新建 | 渲染后的 Coverage 配置（source = coopie, fail_under = 95） |
| `pytest.ini`（项目根） | 新建 | Pytest 配置（无 Jinja 变量） |

## 关键决策与依据

### 1. 方案选择：拆分配置文件 + _skip_if_exists

copier 无原生 TOML 语义合并能力（社区 issue #1738 仍在请求），行级 diff3 合并将工具配置变更与项目元数据变更混在 pyproject.toml 一个文件中，冲突难以理解和解决。

方案 A 将工具配置拆到独立文件（ruff.toml/pyrefly.toml/.coveragerc/pytest.ini），pyproject.toml 加入 `_skip_if_exists` 使 copier update 完全跳过该文件。这样：
- pyproject.toml 首次 `copier copy` 时创建，后续 update 不再覆盖
- 工具配置独立文件可正常更新（用户不定制则自动同步模板改进）
- 用户定制的项目元数据（依赖、版本号等）受到保护

### 2. 工具配置文件格式

| 工具 | 格式 | 前缀变化 | Jinja 变量 |
|------|------|---------|-----------|
| ruff | ruff.toml | [tool.ruff] → 顶层, [tool.ruff.lint] → [lint] | target_py |
| pyrefly | pyrefly.toml | [tool.pyrefly] → 顶层 | min_python_version |
| coverage | .coveragerc | [tool.coverage.run] → [run], [tool.coverage.report] → [report] | package_name, coverage_fail_under |
| pytest | pytest.ini | [tool.pytest.ini_options] → [pytest] | 无 |

工具配置优先级：独立文件 > pyproject.toml 中的 [tool.xxx]，首个命中即用、不合并。

### 3. 保留在 pyproject.toml 的段

以下段保留在 pyproject.toml 中（`_skip_if_exists` 后不被 copier 覆盖）：
- [project] + [project.optional-dependencies] + [project.scripts] — 项目元数据
- [build-system] — 构建配置
- [tool.uv] + [[tool.uv.index]] — uv 配置
- [tool.hatch.build.targets.wheel] — 打包配置
- [dependency-groups] — 依赖分组
- [tool.bumpversion] — 版本管理（current_version 由 bump-my-version 自动维护）

### 4. _skip_if_exists 行为验证

- `copier copy`（首次）：pyproject.toml 正常创建
- `copier update`：pyproject.toml 已存在 → 跳过，用户定制内容完整保留
- 工具配置独立文件不在 `_skip_if_exists` 中 → 正常参与 copier update 三方合并

## 验证结果

- 非 git 副本 `copier copy` 渲染验证：四个独立配置文件正确生成，Jinja 变量正确替换 ✓
- `make check` 全绿：ruff/pyrefly/pytest 均正确读取独立配置文件 ✓
  - pyrefly: `INFO Checking project configured at /home/zhou/coopie/pyrefly.toml`
  - pytest: `configfile: pytest.ini`
  - ruff: `All checks passed!`（自动发现 ruff.toml）
  - coverage: 100%（正确读取 .coveragerc）
- 42 个测试通过，覆盖率 100%
- `copier update -A` 迁移 _commit v0.4.0 → v0.4.4：无冲突，pyproject.toml 被跳过 ✓
- 版本 bump 0.4.3 → 0.4.4，tag v0.4.4 已推送

## 遗留事项

无。后续如需在模板中新增工具配置段，直接添加到对应的独立配置文件即可，pyproject.toml 不会再产生合并冲突。
