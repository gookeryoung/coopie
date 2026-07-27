# req-24：移除 initial_version 模板变量

## 背景

`initial_version` 作为 copier 模板问题，每次 `copier update` 都会重新询问并参与渲染。各项目初始版本可能不同（0.1.0、1.0.0 等），且项目创建后版本号由 bump-my-version 管理，不再应被模板变量影响。保留该变量既增加 update 时的交互负担，又容易因值变化导致冲突（覆盖用户已 bump 的版本号）。

## 需求

- [x] 从 `copier.yml` 移除 `initial_version` 问题定义
- [x] 模板 `pyproject.toml` 硬编码 `version = "0.1.0"` 与 `current_version = "0.1.0"`
- [x] 模板 `src/{{ package_name }}/__init__.py` 硬编码 `__version__ = "0.1.0"`
- [x] 更新 `README.md` 参数表，移除 `initial_version` 行
- [x] 更新 `docs/parameters.rst`，移除 `initial_version` 段落
- [x] 从 `.copier-answers.yml` 移除 `initial_version` 字段
- [x] 验证：ruff/pyrefly/pytest 全绿 + 渲染测试通过
