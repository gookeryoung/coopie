# skill-06：README 与项目文档完善（归档自 iter-06）

> 归档时间：2026-07-11（iter-12 时按 rule-01 归档）

## 概要

结合 coopie 作为 copier 模板的特点，完善项目根 README 与模板 README，补充 badge 信息，同步完善 docs/index.rst 文档。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `README.md` | 修改 | 补充 CI/PyPI/Python/License/Coverage 五个 badge；用法部分补充 coopie CLI 工具说明；生成后步骤补充 Make 快捷命令段 |
| `template/README.md` | 修改 | badge 区补充 PyPI 版本 badge（置首）；新增"特性"段，按 `use_cicd`/`use_docs`/`use_tox`/`use_docker` 条件渲染 |
| `docs/index.rst` | 修改 | 重写：RST 格式 badge、用法段、Make 快捷命令段 |
| `pyproject.toml` / `src/coopie/__init__.py` | bump | 0.1.12 → 0.1.13 |
| `.copier-answers.yml` | 迁移 | `_commit: v0.1.12 → v0.1.13` |

## 关键决策与依据

1. **badge 顺序**：PyPI 版本置首，其后 CI → Python → License → Coverage。项目根与模板一致。
2. **模板特性段条件渲染**：`{% if use_cicd %}`/`{% if use_docs %}`/`{% if use_tox %}`/`{% if use_docker %}` 条件渲染对应特性行。
3. **README 结构性冲突**：copier update 迁移 `_commit` 时，项目根 README（自定义文档）与模板 README 渲染结果整体冲突，用 `git checkout --ours README.md` 保留项目版本。
4. **docs/index.rst badge 格式**：RST 用 `.. |name| image:: url` 声明替换引用，再用 `|name| |name2|` 行内显示。

## 验证结果

- `make check`：ruff 全绿、pyrefly 0 errors、pytest 23 passed、覆盖率 100%。
- 干净 `uvx copier update -A`：`Keeping template version 0.1.13`，无冲突无错误。

## 遗留事项

1. **README 结构性冲突**：每次 copier update 改模板 README 时都会整体冲突，需手动 `git checkout --ours README.md`。
