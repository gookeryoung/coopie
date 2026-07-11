# skill-08：移除项目自身 Dockerfile 支持（归档自 iter-08）

> 归档时间：2026-07-11（iter-15 时按 rule-01 阈值触发归档）

## 概要

coopie 是发布到 PyPI 的 CLI 工具/模板，自身不需要容器化部署。移除项目自身的 Dockerfile 支持，template 保留 `use_docker` 选项供生成项目按需启用。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `.copier-answers.yml` | 修改 | `use_docker: true → false` |
| `Dockerfile` | 删除 | 项目自身不再需要容器化 |
| `.dockerignore` | 删除 | 同上 |
| `README.md` | 修改 | 特性段移除"容器化"行，文件清单移除 Dockerfile/.dockerignore |
| `uv.lock` | 修改 | 依赖 marker 变化（uv 重新解析） |

## 关键决策与依据

1. **项目自身 vs 模板分离**：coopie 通过 `uvx`/`pip install` 使用，不需要容器化部署；template 的 `use_docker` 选项保留，供生成项目按需启用。
2. **`use_docker: false` 效果**：copier update 时不再渲染 Dockerfile 模板（`{% if use_docker %}Dockerfile{% endif %}` 命名），已有文件需手动删除。
3. **不 bump 版本**：仅项目配置变更，模板未改动，无需 bump 或迁移 `_commit`。

## 验证结果

- `make check`：ruff/pyrefly/pytest 23 passed，覆盖率 100%
- `uvx copier update -A`：`Keeping template version 0.1.14`，Dockerfile/.dockerignore 不再生成

## 遗留事项

无。template 的 `use_docker` 选项保持不变，生成项目仍可按需启用 Dockerfile。
