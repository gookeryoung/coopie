# coopie

> 基于 [copier](https://copier.readthedocs.io/) 的通用 Python 项目模板，一键生成开箱即用的工程骨架。

[![CI](https://github.com/gookeryoung/coopie/actions/workflows/ci.yml/badge.svg)](https://github.com/gookeryoung/coopie/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/coopie)](https://pypi.org/project/coopie/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A595%25-brightgreen.svg)](https://github.com/gookeryoung/coopie/actions/workflows/ci.yml)

## 快速开始

```bash
# 新建项目到子目录
coopie new my-project

# 或在当前目录初始化（项目名从目录名派生）
cd existing-dir && coopie init
```

coopie 自动从 git 配置读取作者信息，生成包含构建工具链（uv + ruff + pyrefly + pytest）、CI/CD、文档与测试的完整项目。也可直接用 `uvx copier copy https://gitee.com/gooker_young/coopie.git <目标>` 调用 copier。

### 更新已有项目

模板更新后，在已生成的项目目录中运行：

```bash
coopie update         # 增量合并模板更新
coopie update -A      # 跳过问题（使用上次答案）
coopie test           # dry-run 检查是否产生冲突
```

## CLI 命令

| 命令 | 说明 |
|------|------|
| `coopie new <name>` | 新建项目（建立子目录） |
| `coopie init` | 在当前目录初始化（非空目录提示确认） |
| `coopie update [-A] [-T]` | 更新已生成项目模板 |
| `coopie test [-A] [-T]` | 模拟检查更新冲突（dry-run） |
| `coopie -V` | 显示版本号 |

默认模板源为 Gitee 镜像（`https://gitee.com/gooker_young/coopie.git`），国内访问稳定。`new`/`init` 支持 `--template <url|path>` 指定模板源（URL 或本地路径），也可通过环境变量 `COOPIE_TEMPLATE_REPO` 覆盖默认值。需要走 GitHub 时：

```bash
coopie new my-project --template https://github.com/gookeryoung/coopie
# 或
COOPIE_TEMPLATE_REPO=/path/to/local-coopie coopie new my-project
```

## 可配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `project_name` | str | `my-project` | 项目名称 |
| `package_name` | str | 自动派生 | Python 包名 |
| `description` | str | - | 项目简短描述 |
| `author_name` | str | git 配置 | 作者名称 |
| `author_email` | str | git 配置 | 作者邮箱 |
| `min_python_version` | str | `3.8` | 最低 Python 版本 |
| `max_python_version` | str | `3.14` | 最高 Python 版本 |
| `license` | str | `MIT` | 许可证（MIT/Apache-2.0/GPL-3.0/None） |
| `project_type` | str | `library` | 项目类型（library/cli/gui/web；gui 按 Python 版本区分 PySide2≤3.10 / PySide6≥3.11） |
| `use_docs` | bool | `true` | Sphinx 文档 |
| `use_docker` | bool | `false` | Dockerfile |
| `use_cicd` | bool | `true` | GitHub Actions CI/CD |
| `use_tox` | bool | `true` | tox 多版本测试 |
| `use_cli` | bool | `false` | CLI 入口（project_type=cli 时自动启用） |
| `use_domestic_mirrors` | bool | `true` | 国内镜像源 |
| `coverage_fail_under` | int | `95` | 覆盖率阈值 |

## 生成后

```bash
cd my-project
uv sync --extra dev      # 安装依赖
uv run pytest            # 运行测试
make check               # 全套门禁（lint + typecheck + cov）
```

生成的项目自带 Makefile，运行 `make help` 查看全部命令（sync/build/clean/test/cov/lint/bump 等）。

## 许可证

MIT
