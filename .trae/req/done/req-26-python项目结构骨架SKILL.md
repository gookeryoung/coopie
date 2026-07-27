# req-26：Python 项目结构骨架设计 SKILL

## 背景

coopie 当前 SKILL 目录覆盖具体技术领域（类设计/并发/文件 I/O/测试/CLI/日志/配置/子进程/性能/GUI/FastAPI），但缺少"项目骨架本身如何设计"的总纲性 SKILL。新项目初始化、目录结构设计、工具链配置拆分、包内部组织、CI/CD 骨架等决策散落在 rule-11 与各 SKILL 中，缺乏系统性参考。coopie 自身已实践了一套成熟的项目结构（src layout + 工具链独立文件 + 4 种 project_type 差异化 + bump-my-version + OIDC 发布），应提炼为 SKILL 供模板生成的项目参考。

## 需求

- [x] 创建 `python-project-structure` SKILL，覆盖以下主题：
  - [x] 项目布局：src layout vs flat layout 选择依据
  - [x] 完整目录骨架（src/tests/docs + 工具链配置 + Makefile + LICENSE + .gitignore）
  - [x] pyproject.toml 设计（PEP 621 元数据 + PEP 631 optional-dependencies + PEP 735 dependency-groups + PEP 517 hatchling 构建后端）
  - [x] 工具链配置拆分（ruff.toml/pytest.ini/.coveragerc/pyrefly.toml/.bumpversion.toml/uv.toml/.pre-commit-config.yaml）
  - [x] 包内部结构（`__init__.py`/`py.typed`/`__main__.py`/模块划分）
  - [x] 测试目录组织（tests/unit + tests/integration + conftest.py 层级）
  - [x] 文档目录组织（Sphinx conf.py + ReadTheDocs + index.rst）
  - [x] CI/CD 结构（GitHub Actions 4 jobs + release.yml OIDC）
  - [x] 项目类型差异（library/cli/gui/web）
  - [x] 版本管理（bump-my-version 配置与命令）
  - [x] 构建与发布（uv build + PyPI OIDC + GitHub Release）
  - [x] Makefile 快捷命令
  - [x] 常见陷阱（15 条）
- [x] 根目录与 template 同步两份 SKILL.md，template 版本用 `{% raw %}...{% endraw %}` 包裹避免 Jinja 误渲染 GitHub Actions `${{ }}` 与 `{{ version }}` 占位符
- [x] 更新 `rule-03-触发场景.md`（根 + 模板）在语言场景首位注册新 SKILL 触发条目
- [x] 验证：`copier copy` 渲染 library 类型，确认 SKILL.md 内容完整、Jinja 模式正确保留
