使用指南
========

前置要求
--------

- Python ≥ 3.8
- uv_ ≥ 0.5（推荐）

.. _uv: https://docs.astral.sh/uv/

使用 coopie CLI（推荐）
-----------------------

coopie 提供 ``coopie`` CLI 封装 copier 命令，安装后自动包含 copier 依赖：

.. code-block:: bash

   # 免安装调用（uvx 自动下载 coopie 与 copier）
   uvx coopie init my-project

   # 或 pip 安装后使用
   pip install coopie
   coopie init my-project

``coopie init`` 默认使用 Gitee 国内源，可用 ``--url`` 切换：

.. code-block:: bash

   # 使用 GitHub 源
   coopie init my-project --url https://github.com/gookeryoung/coopie.git

   # 指定模板版本
   coopie init my-project --vcs-ref v0.8.0

   # 使用默认参数跳过交互（CI/脚本化场景）
   coopie init my-project --defaults

使用 copier 原生命令（备选）
-----------------------------

.. _copier: https://copier.readthedocs.io/

在希望生成项目的父目录中执行：

.. code-block:: bash

   # 国内用户推荐 Gitee 源（访问稳定）
   uvx copier copy --trust https://gitee.com/gooker_young/coopie.git my-project

   # 国外用户可使用 GitHub 源
   uvx copier copy --trust https://github.com/gookeryoung/coopie.git my-project

执行后 copier 会交互式询问项目名称、包名、Python 版本范围、项目类型（library/cli/gui/web）等参数，并在 ``my-project/`` 目录生成完整工程骨架。

常用选项：

- ``--trust``：信任模板仓库以执行渲染。
- ``--defaults``：使用所有参数的默认值，跳过交互（适用于 CI/脚本化场景）。
- ``--vcs-ref v0.8.0``：指定模板版本（默认使用最新 tag）。
- ``--data project_name=foo``：在命令行预设参数值。

生成后的下一步
--------------

进入生成目录并初始化开发环境：

.. code-block:: bash

   cd my-project
   uv sync --extra dev
   git init && git add -A && git commit -m "feat: 初始化项目"

更新已有项目
------------

当模板版本升级后，在已生成的项目目录中执行：

.. code-block:: bash

   # 使用 coopie CLI（推荐）
   coopie update

   # 或使用 copier 原生命令
   uvx copier update --trust

``coopie update`` 调用 ``copier recopy``，基于 ``.copier-answers.yml`` 中记录的答案重新渲染模板。copier 原生 ``update`` 命令则比对当前模板版本与记录版本，交互式应用差异更新。

项目类型说明
------------

模板支持四种项目类型，通过 ``project_type`` 参数选择：

- ``library``：纯库项目，无入口脚本，src layout + py.typed。
- ``cli``：命令行工具，生成 ``cli.py`` 与 ``[project.scripts]`` 入口，基于 argparse。
- ``gui``：PySide2/PySide6 桌面应用，按 Python 版本自动选择（≤3.10 用 PySide2，≥3.11 用 PySide6），随模板分发 GUI 设计规范与代码模板。
- ``web``：FastAPI + uvicorn 服务，随模板分发 FastAPI SKILL 文档。

模板开发
--------

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

   # 渲染验证（生成到临时目录检查输出）
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-lib
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-cli --data project_type=cli
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-gui --data project_type=gui
   uvx copier copy --trust --defaults --vcs-ref HEAD . /tmp/preview-web --data project_type=web
