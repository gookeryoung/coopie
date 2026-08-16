更新日志
=========

v0.9.1（未发布）
----------------

- 移除模板未使用的 ``jinja2-time`` 依赖，同步清理 Makefile/CI/文档中的 ``--with jinja2-time`` 引用
- 模板不再分发 ``.trae/`` 规则与技能文档，删除 README/docs 中与实际不符的宣传
- 移除仓库自身的 ``tox.ini``（CI 与 Makefile 均无调用入口，自举答案 ``use_tox`` 置为 false）
- Python 版本要求表述统一为 3.8+（``requires-python>=3.8`` 实际未变，修正 README/docs 徽章与前置要求）
- 模板 ``.vscode/settings.json`` 清理 Python 项目无效的 eslint 保存动作
- 修正 v0.9.0 条目：``requires-python`` 实际未升至 3.9，移除该错误声明

v0.9.0
------

- **breaking**: 恢复 ``coopie`` CLI 工具（``src/coopie/cli.py``），反转 iter-22 的纯模板仓库决策
- **breaking**: 恢复 PyPI 发布流程（``release.yml`` 使用 OIDC trusted publishing）
- 新增 ``coopie init`` 命令，封装 ``copier copy --trust``，默认 Gitee 源，支持 ``--url``/``--vcs-ref``/``--defaults``
- 新增 ``coopie update`` 命令，封装 ``copier recopy --trust``，默认当前目录
- 依赖 ``copier>=9.0.0`` + ``jinja2-time>=0.2.0`` + ``typer>=0.12.0``
- 恢复 ``[build-system]``/``[project.scripts]``/``[tool.hatch.build]``/``[tool.pytest]``/``[tool.coverage]`` 配置
- CI 新增 test job（pytest + coverage）；lint job 扩展为全量检查（src/ + tests/ + docs/）
- Makefile 新增 ``test``/``cov``/``build`` 目标
- bump-my-version 新增 ``src/coopie/__init__.py`` 版本同步

v0.8.0
------

- **breaking**: 移除 ``coopie`` CLI 工具（``src/coopie/``），回归 copier 原生使用方式
- **breaking**: 移除 PyPI 发布流程（``release.yml`` 不再 ``uv publish``）
- 删除 ``src/coopie/``、``tests/``、``tox.ini``
- 重写 README 与 docs 为 copier 模板使用说明
- pyproject.toml 移除 ``[project.scripts]``、``[tool.hatch.build]``、``[tool.coverage]``、``[tool.pytest]``
- copier.yml 移除冗余的 ``use_cli`` 字段（由 ``project_type == 'cli'`` 推导）

v0.7.12
-------

- 修复 Windows 文件名兼容（Jinja 条件文件名双引号改单引号）
- CLI 默认模板源切换为 Gitee（国内访问稳定）
- Makefile ``push`` 改为遍历 ``git remote`` 不硬编码远程名
- 新增 GUI 设计规范（rule-12-gui-pyside-standards.md）

v0.1.0
------

- 项目初始化
