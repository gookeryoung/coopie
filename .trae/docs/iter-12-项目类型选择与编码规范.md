# iter-12：项目类型选择与编码规范

## 迭代目标

在 copier 模板中新增 `project_type` 变量（library/cli/gui/web），根据类型配置对应依赖与入口模板文件，并制定 PySide2 编码规范（rule-12-pyqt-standards.md）。

## 需求确认

按 rule-01 需求分析规则，创建 `.trae/req/req-12-项目类型选择与编码规范.md` 并通过 AskUserQuestion 与用户确认：

- 支持全部 4 种项目类型：library（纯库）、cli（命令行工具）、gui（PySide2 桌面应用）、web（FastAPI 服务）
- GUI 使用 PySide2（非 PySide6，用户明确选择）
- 编码规范产出：仅 rule-12 一份 PySide2 最佳实践
- 验收标准：标准门禁（ruff + pyrefly + pytest 95% + copier update 无冲突）

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `copier.yml` | 修改 | 新增 `project_type` 变量（4 选项，默认 library） |
| `template/pyproject.toml` | 修改 | 按 project_type 条件化 dependencies（gui: PySide2 + 环境标记、web: fastapi+uvicorn）；scripts 条件改为 `use_cli or project_type == "cli"` |
| `template/src/{{ package_name }}/{% if project_type == "cli" %}cli.py{% endif %}` | 新建 | CLI 入口模板（argparse + --version） |
| `template/src/{{ package_name }}/{% if project_type == "gui" %}main.py{% endif %}` | 新建 | PySide2 QApplication 入口（main() 标记 `# pragma: no cover`） |
| `template/src/{{ package_name }}/{% if project_type == "web" %}app.py{% endif %}` | 新建 | FastAPI app 实例 + uvicorn runner |
| `src/coopie/cli.py` | 修改 | new/init 子命令增加 `--type` 选项；_run_new/_run_init 传递 `--data project_type=<type>` |
| `tests/test_cli.py` | 修改 | 新增 8 个测试（--type 选项验证），42 tests 100% cov |
| `.trae/rules/rule-12-pyqt-standards.md` | 新建 | PySide2 编码规范（工具链/兼容性/信号槽/布局/资源/线程/QSS/测试/打包/i18n/性能） |
| `template/.trae/rules/{% if project_type == "gui" %}rule-12-pyqt-standards.md{% endif %}` | 新建 | 模板版 rule-12（Jinja 变量渲染） |
| `.copier-answers.yml` | 修改 | 新增 `project_type: library`（coopie 自身 use_cli=true，避免 cli.py 模板冲突） |
| `README.md` | 修改 | 可配置选项表新增 use_cli 和 project_type 行 |
| `template/README.md` | 修改 | 特性段按 project_type 条件渲染 |
| `.trae/req/req-12-项目类型选择与编码规范.md` | 新建 | 需求分析文档 |
| `pyproject.toml` / `src/coopie/__init__.py` | bump | 0.2.4 → 0.3.0 |
| `.copier-answers.yml` | 迁移 | `_commit: v0.2.3 → v0.3.0` |

## 关键决策与依据

1. **use_cli 与 project_type 的关系**：`use_cli`（bool）保持向后兼容，仅控制 `[project.scripts]` 行；`project_type=cli` 额外生成 cli.py 模板文件。两者关系为 `use_cli or project_type == "cli"` 控制 scripts。

2. **coopie 自身 project_type 设为 library**：coopie 已有自定义 cli.py（src/coopie/cli.py），若 project_type=cli 则 copier update 会生成模板版 cli.py 覆盖。设为 library + use_cli=true 避免冲突。

3. **cli.py 模板条件只用 `project_type == "cli"`**：初始设计为 `use_cli or project_type == "cli"`，发现会导致 coopie（use_cli=true）在 copier update 时生成模板 cli.py 覆盖自定义版本。改为仅 `project_type == "cli"`。

4. **PySide2 Python 版本限制**：PyPI 官方 wheel 5.15.2.1 仅支持 Python 3.6-3.10（无 3.11+ wheel）。依赖加环境标记 `; python_version <= "3.10"`，rule-12 文档说明建议 gui 项目 max_python_version 设为 3.10。

5. **rule-12 模板版 Jinja 化**：模板内 rule-12 用 `{{ package_name }}`、`{{ coverage_fail_under }}` 等变量替换硬编码值，仅 project_type=gui 时渲染到生成项目。

6. **条件文件名渲染**：copier 的 `_templates_suffix: ""` 使所有文件都参与 Jinja 渲染，文件名中的 `{% if condition %}filename{% endif %}` 控制条件生成。

## 验证结果

- `ruff check`：All checks passed!
- `ruff format --check`：5 files already formatted
- `pyrefly check`：0 errors
- `pytest`：42 passed, 100% coverage（≥ 95%）
- copier update -A：`Updating to template version 0.3.0`，无冲突
- 4 种 project_type 渲染验证（rsync 副本 + copier copy --defaults）：library/cli/gui/web 均正确

## 提交历史

```
8b62704 chore: 迁移 _commit v0.2.3 → v0.3.0（copier update 无冲突）
0c81e6b style: 修正 rule-12 格式（双空行分隔）
4175a99 chore: 同步 uv.lock 至 0.3.0
ce09fe3 chore: 更新版本 0.2.4 → 0.3.0  (tag: v0.3.0)
233973b feat: 新增 project_type 项目类型选择与 PySide2 编码规范
```

## 遗留事项

1. **PySide2 版本限制**：PyPI wheel 仅支持 Python 3.6-3.10，gui 项目的 max_python_version 应设为 3.10。rule-12 已文档说明。
2. **rule-01 归档**：iter-06 已归档到 skill-06（docs 超过 5 份触发清理）。
