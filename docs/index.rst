coopie
======

基于 copier_ 的通用 Python 项目模板，通过 ``coopie`` CLI 或 ``copier copy`` 一键生成开箱即用的工程骨架。

.. _copier: https://copier.readthedocs.io/

.. toctree::
   :maxdepth: 2
   :caption: 目录

   usage
   parameters
   api
   changelog

简介
====

coopie 是一个 copier 模板仓库，用于生成符合现代 Python 工程实践的项目骨架。提供 ``coopie`` CLI 封装 ``copier copy/recopy`` 命令，简化模板调用。模板内置：

- **构建工具链**：hatchling + uv + ruff + pyrefly + pytest + coverage
- **Python 版本**：3.8 ~ 3.14（可配置最低/最高版本）
- **代码质量**：pre-commit 钩子 + ruff lint/format，可配置覆盖率阈值
- **CI/CD**：GitHub Actions（lint + typecheck + 多版本测试 + 自动发布到 PyPI）
- **文档**：Sphinx + ReadTheDocs（中文 zh_CN）
- **多版本测试**：tox + tox-uv
- **项目类型**：library / cli / gui（PySide2/PySide6）/ web（FastAPI）
- **项目结构**：src layout + py.typed 类型标记
- **开发规则**：内嵌 ``.trae/rules/`` 与 ``.trae/skills/`` 规则体系，配套 SKILL 文档

安装
====

coopie CLI 封装 copier 调用，安装后自动包含 copier 依赖：

.. code-block:: bash

   # 免安装调用（uvx 自动下载 coopie 与 copier）
   uvx coopie init my-project

   # 或 pip 安装后使用
   pip install coopie
   coopie init my-project

快速上手
========

使用 ``coopie init`` 从模板创建新项目：

.. code-block:: bash

   # 默认使用 Gitee 国内源
   coopie init my-project

   # 使用 GitHub 源
   coopie init my-project --url https://github.com/gookeryoung/coopie.git

   # 指定模板版本
   coopie init my-project --vcs-ref v0.8.0

   # 使用默认参数跳过交互（CI/脚本化场景）
   coopie init my-project --defaults

执行后会交互式询问项目名称、包名、Python 版本范围、项目类型（library/cli/gui/web）等参数，并在目标目录生成完整工程骨架。详细使用说明见 :doc:`usage`，模板参数说明见 :doc:`parameters`。

更新已有项目
============

当模板版本升级后，在已生成的项目目录中执行：

.. code-block:: bash

   # 使用 coopie CLI（推荐）
   coopie update

   # 或使用 copier 原生命令
   uvx copier update --trust --with jinja2-time

``coopie update`` 调用 ``copier recopy``，基于 ``.copier-answers.yml`` 中记录的答案重新渲染模板。

开发
====

本仓库自身即 copier 模板，开发与验证流程：

.. code-block:: bash

   # 安装开发依赖（lint + test + docs 工具链）
   uv sync --extra dev

   # 校验代码
   uv run ruff check
   uv run ruff format --check

   # 类型检查
   uv run pyrefly check

   # 运行测试
   uv run pytest

   # 本地构建文档
   make doc

   # 渲染验证（生成到 .preview/ 检查输出）
   make render
