# iter-16 需求：拆分工具配置到独立文件

## 需求来源

`coopie update` 时 copier 对 `pyproject.toml` 做行级三方合并，不支持 TOML 语义级合并。用户对 `pyproject.toml` 的定制内容（新增依赖、工具配置）容易被模板更新覆盖或产生难以理解的冲突。

## 方案

方案 A（用户授权）：将工具配置从 `pyproject.toml` 拆到独立文件，`pyproject.toml` 加入 `_skip_if_exists`，copier 生成后不再覆盖。

## 需求清单

- [x] 1. 从 template/pyproject.toml 移除 [tool.ruff]、[tool.ruff.lint]、[tool.ruff.lint.per-file-ignores]
- [x] 2. 从 template/pyproject.toml 移除 [tool.pyrefly]
- [x] 3. 从 template/pyproject.toml 移除 [tool.coverage.run]、[tool.coverage.report]
- [x] 4. 从 template/pyproject.toml 移除 [tool.pytest.ini_options]
- [x] 5. 创建 template/ruff.toml（TOML 格式，Jinja 渲染 target-version）
- [x] 6. 创建 template/pyrefly.toml（TOML 格式，Jinja 渲染 python-version）
- [x] 7. 创建 template/.coveragerc（INI 格式，Jinja 渲染 source/fail_under）
- [x] 8. 创建 template/pytest.ini（INI 格式，无 Jinja 变量）
- [x] 9. copier.yml 添加 _skip_if_exists: [pyproject.toml]
- [x] 10. 同步变更到项目根（创建独立配置文件，从 pyproject.toml 移除对应段）
- [x] 11. make check 全绿（ruff/pyrefly/pytest/coverage 能正确读取独立配置）
- [x] 12. bump 版本 + copier update 迁移 _commit
- [x] 13. 创建 iter-16 文档

## 保留在 pyproject.toml 的段（_skip_if_exists 后不再覆盖）

- [project] + [project.optional-dependencies] + [project.scripts]
- [build-system]
- [tool.uv] + [[tool.uv.index]]
- [tool.hatch.build.targets.wheel]
- [dependency-groups]
- [tool.bumpversion]（current_version 由 bump-my-version 管理，不应被覆盖）
