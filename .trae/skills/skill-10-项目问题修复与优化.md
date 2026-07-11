# skill-10：项目问题修复与优化（归档自 iter-10）

> 归档时间：2026-07-11（iter-15 时按 rule-01 阈值触发归档）

## 概要

修复项目审计发现的问题：classifiers 排序、未使用依赖清理（typing-extensions/httpx/pytest-mock）、pre-commit hook 补全（ruff-format）、ruff 版本升级、文档修正。

## 改动文件清单

| 文件 | 改动 |
|------|------|
| `pyproject.toml` | classifiers 排序；移除 typing-extensions（dependencies）、httpx（dev）、pytest-mock（test） |
| `template/pyproject.toml` | 同步移除 typing-extensions、httpx、pytest-mock |
| `.pre-commit-config.yaml` | ruff v0.15.4→v0.15.8；添加 ruff-format hook |
| `template/.pre-commit-config.yaml` | 同步 ruff 升级 + ruff-format hook |
| `README.md` | `make bump PART=patch` → `make bump`（默认 patch） |
| `docs/index.rst` | 同步 make bump 用法修正 |
| `uv.lock` | 同步依赖变更（移除 httpx/pytest-mock 及传递依赖 anyio/h11/httpcore/sniffio） |
| `pyproject.toml` / `src/coopie/__init__.py` | bump 0.2.2 → 0.2.3 |

## 关键决策与依据

1. **classifiers 排序**：经多次 copier update 后乱序（3.10-3.14 后接 3.8-3.9）。模板用 `{% for v in supported_py_versions %}` 渲染正确，项目根手动修正为升序。
2. **移除未使用依赖**：grep 确认 src/tests/docs 全无 import。
   - typing-extensions：rule-11 说仅用于 `override`/`TypeVar` 前向兼容，代码未用。`from __future__ import annotations` 已延迟注解求值，`str | None` 在 3.8 运行时安全。
   - httpx：dev 依赖但代码无 HTTP 客户端调用。
   - pytest-mock：test 依赖但无 `mocker` fixture，且 rule-11 明确禁用。
3. **pre-commit 添加 ruff-format hook**：原配置只有 `ruff`（lint + --fix），缺少格式化 hook。Makefile 的 `lint` 目标会跑 `ruff format --check`，但 pre-commit 不拦截格式问题。添加 `ruff-format` hook 与 Makefile 对齐。
4. **保留 pytest-xdist/pytest-html/pytest-asyncio**：pytest 生态标准插件（并行加速、HTML 报告、异步测试），作为模板标准测试工具链保留合理。

## 验证结果

- `uv lock`：成功移除 httpx/pytest-mock 及传递依赖（anyio/h11/httpcore/sniffio）
- `make check`：ruff/pyrefly 0 errors、pytest 23 passed、覆盖率 100%
- `uvx copier update -A`：`Keeping template version 0.2.2`，无冲突

## 遗留事项

`.python-version`（3.8→3.14）和 `.readthedocs.yaml`（3.8→3.13）被本地工具反复篡改。缓解：`git update-index --skip-worktree .python-version`。`.readthedocs.yaml` 触发源待排查。
