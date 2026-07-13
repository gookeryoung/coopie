coopie
======

.. |ci| image:: https://github.com/gookeryoung/coopie/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/gookeryoung/coopie/actions/workflows/ci.yml
   :alt: CI

.. |pypi| image:: https://img.shields.io/pypi/v/coopie
   :target: https://pypi.org/project/coopie/
   :alt: PyPI

.. |python| image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
   :target: https://www.python.org/
   :alt: Python

.. |license| image:: https://img.shields.io/badge/license-MIT-green.svg
   :alt: License

.. |coverage| image:: https://img.shields.io/badge/coverage-%E2%89%A595%25-brightgreen.svg
   :target: https://github.com/gookeryoung/coopie/actions/workflows/ci.yml
   :alt: Coverage

|ci| |pypi| |python| |license| |coverage|

基于 `copier <https://copier.readthedocs.io/>`_ 的通用 Python 项目模板，自身既是模板又是可运行的 CLI 工具。

.. toctree::
   :maxdepth: 2
   :caption: 目录

   api
   changelog

简介
====

基于 `pyflowx <https://github.com/gookeryoung/pyflowx>`_ 项目实践，生成开箱即用的 Python 项目骨架，包含 hatchling + uv + ruff + pyrefly + pytest + coverage 工具链。

安装
====

.. code-block:: bash

   pip install coopie

或使用 uv_:

.. code-block:: bash

   uv add coopie

.. _uv: https://docs.astral.sh/uv/

用法
====

coopie 既是模板又是 CLI 工具，封装了 ``copier copy/update``，自动从 git 配置读取作者信息。采用子命令模式。

创建新项目（在子目录中新建）::

   coopie new my-new-project

   # 或直接调用 copier
   uvx copier copy https://gitee.com/gooker_young/coopie.git my-new-project

默认模板源为 Gitee 镜像（``https://gitee.com/gooker_young/coopie.git``），国内访问稳定。
``new``/``init`` 支持 ``--template <url|path>`` 指定模板源（URL 或本地路径），也可通过环境变量
``COOPIE_TEMPLATE_REPO`` 覆盖默认值。需要走 GitHub 时::

   coopie new my-project --template https://github.com/gookeryoung/coopie
   # 或
   COOPIE_TEMPLATE_REPO=/path/to/local-coopie coopie new my-project

在当前目录初始化项目（project_name 从目录名派生）::

   cd existing-dir
   coopie init           # 非空目录会提示确认（y/N）

更新已有项目::

   cd my-new-project
   coopie update         # 等价于 copier update
   coopie update -A      # 跳过所有问题
   coopie update -T      # 跳过所有任务

模拟检查更新冲突（dry-run，不修改文件）::

   coopie test           # 等价于 copier update --pretend
   coopie test -A -T     # 跳过所有问题和任务

快速上手
========

.. code-block:: python

   import coopie

   print(coopie.__version__)

开发
====

.. code-block:: bash

   # 安装开发依赖
   uv sync --extra dev

   # 运行测试（含覆盖率，阈值 95%）
   uv run pytest -m "not slow" --cov=coopie --cov-fail-under=95

   # 类型检查
   uv run pyrefly check

   # 代码风格
   uv run ruff check src tests
   uv run ruff format --check src tests

Make 快捷命令
=============

项目提供 Makefile 封装常用操作，运行 ``make help`` 查看全部命令::

   make sync     # 安装开发依赖
   make check    # 全套门禁 (lint + typecheck + cov)
   make build    # 构建分发包
   make clean    # 清理构建产物
   make bump              # 版本号 bump (默认 patch，可指定 minor/major)
