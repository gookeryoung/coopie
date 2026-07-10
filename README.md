# pytemplate

> 基于 [copier](https://copier.readthedocs.io/) 的通用 Python 项目模板。

基于 [pyflowx](https://github.com/gookeryoung/pyflowx) 项目实践，生成开箱即用的 Python 项目骨架。

## 特性

- **构建工具链**：hatchling + uv + ruff + pyrefly + pytest + coverage
- **多版本支持**：Python 3.8 ~ 3.14（可配置范围）
- **CI/CD**：GitHub Actions（lint + typecheck + 多版本测试 + 自动发布）
- **容器化**：Dockerfile（含国内镜像源配置）
- **文档**：Sphinx + ReadTheDocs（中文 zh_CN）
- **代码质量**：pre-commit 钩子 + ruff lint/format
- **多版本测试**：tox + tox-uv
- **开发规则**：.trae 规则集（自驱动开发 + Python 规范 + 提交规范）
- **项目结构**：src layout + py.typed 标记
- **模板更新**：支持 `copier update` 增量合并

## 用法

### 创建新项目

模板使用 `jinja2-time` 扩展获取当前年份，需随 copier 一起安装。

```bash
# 方式一：uvx（推荐，无需预装）
uvx --with jinja2-time copier copy --trust f:\Dev\pytemplate my-new-project

# 方式二：pip
pip install copier jinja2-time
copier copy --trust f:\Dev\pytemplate my-new-project

# 从 git 仓库创建（推送到远程后）
uvx --with jinja2-time copier copy --trust https://github.com/yourname/pytemplate.git my-new-project
```

> `--trust` 是必需的，因为模板使用了 `jinja_extensions` 功能（用于 `{% now %}` 动态获取版权年份）。

### 更新已有项目

当模板更新后，可在已生成的项目目录中运行：

```bash
cd my-new-project
uvx --with jinja2-time copier update --trust
```

Copier 会读取 `.copier-answers.yml` 中的上一次答案，对比模板差异，增量合并更新。

## 可配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `project_name` | str | `my-project` | 项目名称 |
| `package_name` | str | 自动派生 | Python 包名（导入标识符） |
| `description` | str | - | 项目简短描述 |
| `author_name` | str | - | 作者名称 |
| `author_email` | str | - | 作者邮箱 |
| `min_python_version` | str | `3.8` | 最低 Python 版本 |
| `max_python_version` | str | `3.14` | 最高 Python 版本 |
| `license` | str | `MIT` | 许可证（MIT/Apache-2.0/GPL-3.0/None） |
| `use_docs` | bool | `true` | Sphinx 文档配置 |
| `use_docker` | bool | `true` | Dockerfile |
| `use_cicd` | bool | `true` | GitHub Actions CI/CD |
| `use_tox` | bool | `true` | tox 多版本测试 |
| `use_domestic_mirrors` | bool | `true` | 国内镜像源 |
| `coverage_fail_under` | int | `95` | 覆盖率阈值 |
| `pypi_token_secret` | str | `PYPI_TOKEN` | PyPI token Secret 名 |

## 生成文件清单

```
my-project/
├── .copier-answers.yml          # Copier 答案（用于 copier update）
├── .dockerignore                # Docker 忽略文件（use_docker）
├── .gitignore                   # Git 忽略文件
├── .pre-commit-config.yaml      # pre-commit 钩子配置
├── .python-version              # Python 版本（uv/pyenv 用）
├── .readthedocs.yaml            # ReadTheDocs 配置（use_docs）
├── .trae/                       # Trae 开发规则
│   ├── .ignore
│   └── rules/
│       ├── self-driven.md       # 自驱动开发规则
│       ├── dev-workflow.md      # 开发流程约束
│       ├── git-commit-message.md # 提交信息规范
│       └── python-standards.md  # Python 开发规范
├── .vscode/settings.json        # VS Code 配置
├── Dockerfile                   # CI/容器化用（use_docker）
├── LICENSE                      # 许可证文件
├── README.md                    # 项目 README
├── docs/                        # Sphinx 文档（use_docs）
│   ├── _static/.gitkeep
│   ├── api.rst
│   ├── changelog.rst
│   ├── conf.py
│   └── index.rst
├── pyproject.toml               # 项目配置（构建/依赖/工具链）
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── py.typed             # PEP 561 类型标记
├── tests/
│   ├── __init__.py
│   └── test_my_package.py       # 冒烟测试
└── tox.ini                      # 多版本测试配置（use_tox）
```

## 生成后步骤

```bash
cd my-project
uv sync --extra dev          # 安装开发依赖
uv run pytest                # 运行测试
git init                     # 初始化 git 仓库
git add -A
git commit -m "feat: 初始化项目"
```

## 设计依据

本模板提炼自 pyflowx 项目的工程实践：

- **src layout**：避免导入歧义，与 pyflowx 一致
- **hatchling 构建后端**：快速、现代、PEP 621 兼容
- **uv 依赖管理**：比 pip 快 10-100x，支持 lockfile
- **ruff**：集成 lint + format，替代 flake8 + isort + black
- **pyrefly**：Meta 开源的快速类型检查器
- **.trae 规则**：AI 辅助开发的行为约束（自驱动 + 代码规范）
- **国内镜像源**：pip/uv 清华源、apt 阿里云、Docker 道云

## 许可证

MIT
