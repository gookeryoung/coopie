# skill-12：项目类型选择与编码规范（归档自 iter-12/req-12）

## 需求

- 新增 copier 变量 `project_type`（library/cli/gui/web），默认 library
- 根据 project_type 配置对应依赖：
  - library/cli: 无额外依赖
  - gui: PySide2（环境标记 `python_version <= "3.10"`，因 PyPI wheel 仅支持 3.6-3.10）
  - web: fastapi + uvicorn[standard]
- 根据 project_type 生成入口模板文件：
  - cli: src/{package_name}/cli.py（与 use_cli 对齐）
  - gui: src/{package_name}/main.py（PySide2 QApplication 入口）
  - web: src/{package_name}/app.py（FastAPI app 实例）
- CLI（coopie new/init）增加 `--type` 选项传递 project_type
- 填充 rule-12-pyqt-standards.md（PySide2 编码规范）
- 模板内 rule-12 条件渲染（project_type=gui 时生成到生成项目）
- .copier-answers.yml 添加 `project_type: library`（coopie 自身 use_cli=true，避免 cli.py 模板冲突）
- README 同步更新 project_type 说明（项目根 + 模板）

## 关键决策与依据

1. **use_cli 与 project_type 的关系**：`use_cli`（bool）保持向后兼容，仅控制 `[project.scripts]` 行；`project_type=cli` 额外生成 cli.py 模板文件。两者关系为 `use_cli or project_type == "cli"` 控制 scripts。

2. **coopie 自身 project_type 设为 library**：coopie 已有自定义 cli.py（src/coopie/cli.py），若 project_type=cli 则 copier update 会生成模板版 cli.py 覆盖。设为 library + use_cli=true 避免冲突。

3. **cli.py 模板条件只用 `project_type == "cli"`**：初始设计为 `use_cli or project_type == "cli"`，发现会导致 coopie（use_cli=true）在 copier update 时生成模板 cli.py 覆盖自定义版本。改为仅 `project_type == "cli"`。

4. **PySide2 Python 版本限制**：PyPI 官方 wheel 5.15.2.1 仅支持 Python 3.6-3.10（无 3.11+ wheel）。依赖加环境标记 `; python_version <= "3.10"`，rule-12 文档说明建议 gui 项目 max_python_version 设为 3.10。

5. **rule-12 模板版 Jinja 化**：模板内 rule-12 用 `{{ package_name }}`、`{{ coverage_fail_under }}` 等变量替换硬编码值，仅 project_type=gui 时渲染到生成项目。

6. **条件文件名渲染**：copier 的 `_templates_suffix: ""` 使所有文件都参与 Jinja 渲染，文件名中的 `{% if condition %}filename{% endif %}` 控制条件生成。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `copier.yml` | 修改 | 新增 `project_type` 变量（4 选项，默认 library） |
| `template/pyproject.toml` | 修改 | 按 project_type 条件化 dependencies；scripts 条件改为 `use_cli or project_type == "cli"` |
| `template/src/.../cli.py` | 新建 | CLI 入口模板（argparse + --version），条件 `project_type == "cli"` |
| `template/src/.../main.py` | 新建 | PySide2 QApplication 入口，条件 `project_type == "gui"` |
| `template/src/.../app.py` | 新建 | FastAPI app 实例 + uvicorn runner，条件 `project_type == "web"` |
| `src/coopie/cli.py` | 修改 | new/init 子命令增加 `--type` 选项 |
| `tests/test_cli.py` | 修改 | 新增 8 个测试，42 tests 100% cov |
| `.trae/rules/rule-12-pyqt-standards.md` | 新建 | PySide2 编码规范 |
| `template/.trae/rules/rule-12-...` | 新建 | 模板版 rule-12（Jinja 变量渲染） |
| `.copier-answers.yml` | 修改 | 新增 `project_type: library` |
| `README.md` / `template/README.md` | 修改 | project_type 说明 |

## 验证结果

- ruff/pyrefly/pytest 全绿（42 passed, 100% coverage）
- copier update -A：`Updating to template version 0.3.0`，无冲突
- 4 种 project_type 渲染验证：library/cli/gui/web 均正确
- 版本 bump 0.2.4 → 0.3.0，tag v0.3.0 已推送

## 遗留事项

- PySide2 版本限制：PyPI wheel 仅支持 Python 3.6-3.10，gui 项目的 max_python_version 应设为 3.10。rule-12 已文档说明。
- iter-13 后续补充了 PySide6 支持（Python ≥ 3.11），解决了此限制。
