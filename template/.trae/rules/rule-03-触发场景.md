---
name: "rule-03-触发场景"
alwaysApply: true
---

# 触发场景

开发前须调用对应 SKILL 获取设计系统、代码模板与硬约束。所有代码须遵守 SKILL.md 中的最佳实践，禁止项见 SKILL.md「常见陷阱」。

## 语言场景

Python 项目须遵守 `rule-11-python-standards.md` 硬约束；涉及以下领域时调用对应 SKILL 获取详细参考：

- 类设计（dataclass/ABC/Enum/缓存/继承组合/设计模式）→ `python-class-design` SKILL
- 并发（threading/concurrent.futures/multiprocessing/asyncio/线程安全）→ `python-concurrency` SKILL
- 文件 I/O（pathlib/读写/上下文管理/临时文件/序列化/原子写入）→ `python-file-io` SKILL
- 测试（pytest fixtures/parametrize/mock/coverage/pytest-qt）→ `python-testing` SKILL
- CLI 开发（Click/Typer/子命令/进度/配置/测试）→ `python-cli` SKILL

## 项目场景

- PySide2/PySide6 GUI 项目（`project_type=gui`）：开发前**必须**调用 `gui-pyside` SKILL（见 rule-12）。
- FastAPI Web 项目（`project_type=web`）：开发前**必须**调用 `fastapi` SKILL。
