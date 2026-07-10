# {{ project_name }}

> {{ description }}

{% if use_cicd %}[![CI]({{ "https://github.com/" ~ author_name ~ "/" ~ project_name ~ "/actions/workflows/ci.yml/badge.svg" }})]({{ "https://github.com/" ~ author_name ~ "/" ~ project_name ~ "/actions/workflows/ci.yml" }})
{% endif %}![Python](https://img.shields.io/badge/python-{{ min_python_version }}%2B-blue.svg)
{% if license != "None" %}![License](https://img.shields.io/badge/license-{{ license }}-green.svg)
{% endif %}![Coverage](https://img.shields.io/badge/coverage-%E2%89%A5{{ coverage_fail_under }}%25-brightgreen.svg)

## 安装

```bash
pip install {{ package_name }}
```

或使用 [uv](https://docs.astral.sh/uv/)：

```bash
uv add {{ package_name }}
```

## 快速上手

```python
import {{ package_name }}

print({{ package_name }}.__version__)
```

## 开发

```bash
# 安装开发依赖
uv sync --extra dev

# 运行测试（含覆盖率，阈值 {{ coverage_fail_under }}%）
uv run pytest -m "not slow" --cov={{ package_name }} --cov-fail-under={{ coverage_fail_under }}

# 类型检查
uv run pyrefly check .

# 代码风格
uv run ruff check src tests
uv run ruff format --check src tests
```

### Make 快捷命令

项目提供 Makefile 封装常用操作，运行 `make help` 查看全部命令：

```bash
make sync     # 安装开发依赖
make check    # 全套门禁 (lint + typecheck + cov)
make build    # 构建分发包
make clean    # 清理构建产物
make bump PART=patch  # 版本号 bump
```

{% if use_docs %}
## 文档

文档由 Sphinx 构建，托管在 ReadTheDocs：

```bash
# 本地构建文档
make doc
```
{% endif %}
{% if use_tox %}
## 多版本测试

使用 tox 在多个 Python 版本（{{ tox_envlist }}）下运行测试：

```bash
make tox
```
{% endif %}
## 许可证

{% if license == "MIT" %}MIT{% elif license == "Apache-2.0" %}Apache-2.0{% elif license == "GPL-3.0" %}GPL-3.0{% else %}未指定{% endif %}
