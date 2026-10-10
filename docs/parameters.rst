模板参数
========

本节列出 ``copier.yml`` 中定义的全部参数。参数分为询问参数（copier 交互式收集）与派生参数（``when: false``，自动计算不询问）。

项目基本信息
------------

``project_name``
   类型：str，默认：``my-project``

   项目名称，可含连字符，用于 README/文档标题与 git 仓库名。

``package_name``
   类型：str，默认：由 ``project_name`` 派生（小写+下划线）

   Python 包名，必须是合法导入标识符。

``description``
   类型：str，默认：``A Python project.``

   项目简短描述（一句话），用于 pyproject.toml 与 README。

``author_name``
   类型：str，默认：空

   作者名称，用于 pyproject.toml 与 LICENSE。

``author_email``
   类型：str，默认：空

   作者邮箱，用于 pyproject.toml。

Python 版本配置
----------------

``min_python_version``
   类型：str，默认：``3.8``，可选：3.8 ~ 3.14

   最低支持的 Python 版本，决定 ``requires-python``、ruff ``target-version``、tox envlist 起始版本、CI 矩阵下界。

``max_python_version``
   类型：str，默认：``3.14``，可选：3.8 ~ 3.14

   最高支持的 Python 版本，决定 classifiers 列表、tox envlist 结束版本、CI 矩阵上界。

派生变量（不询问）
------------------

以下变量由 ``min_python_version`` / ``max_python_version`` 自动计算：

- ``target_py``：ruff ``target-version`` 值，如 ``py38``。
- ``supported_py_versions``：JSON 数组，classifiers 用。
- ``tox_envlist``：tox envlist 字符串，如 ``py38, py39, py310``。
- ``ci_test_versions``：JSON 数组，CI 矩阵测试版本（首尾两个）。

许可证
------

``license``
   类型：str，默认：``MIT``，可选：MIT / Apache-2.0 / GPL-3.0 / None

   许可证类型。选 ``None`` 时不生成 LICENSE 文件，pyproject.toml 不含 license 字段。

功能开关
--------

``use_docs``
   类型：bool，默认：true

   是否包含 Sphinx 文档配置（conf.py、index.rst、ReadTheDocs 配置）。

``use_docker``
   类型：bool，默认：false

   是否包含 Dockerfile 与 .dockerignore。

``use_cicd``
   类型：bool，默认：true

   是否包含 GitHub Actions CI/CD 配置（ci.yml + release.yml）。

``use_tox``
   类型：bool，默认：true

   是否包含 tox 多版本测试配置。

``project_type``
   类型：str，默认：library，可选：library / cli / gui / web

   项目类型，决定入口模板与依赖：

   - ``library``：纯库，无入口脚本。
   - ``cli``：生成 ``cli.py``，启用 ``[project.scripts]``。
   - ``gui``：PySide2（≤3.10）/ PySide6（≥3.11），分发 GUI 设计规范。
   - ``web``：FastAPI + uvicorn，分发 FastAPI SKILL。

``use_domestic_mirrors``
   类型：bool，默认：true

   是否预置国内镜像源（uv 华为云源、apt 华为云源）。

``coverage_fail_under``
   类型：int，默认：95

   覆盖率阈值（百分比），用于 pytest --cov-fail-under 与 CI 校验。

模板配置（高级）
----------------

以下字段在 ``copier.yml`` 末尾，通常无需修改：

- ``_subdirectory: template``：模板内容位于 ``template/`` 子目录。
- ``_answers_file: .copier-answers.yml``：答案记录文件路径。
- ``_templates_suffix: ""``：渲染所有文件（copier v9 默认仅渲染 ``.jinja`` 后缀）。
- ``_copy_without_render``：不渲染的文件列表（二进制/空标记文件）。
