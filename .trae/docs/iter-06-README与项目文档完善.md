# iter-06：README 与项目文档完善

## 迭代目标

结合 coopie 作为 copier 模板的特点，完善项目根 README 与模板 README，补充 badge 信息，同步完善 docs/index.rst 文档。

## 需求确认

按 rule-01 需求分析规则，创建 `.trae/req/req-06-README与项目文档完善.md` 并与用户确认：
- Badge 范围：两者都做（项目根 README 加 badge + 模板 README 补充 PyPI badge）
- 完善对象：两者都完善（项目根 README + 模板 README）

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `README.md` | 修改 | 补充 CI/PyPI/Python/License/Coverage 五个 badge；用法部分补充 coopie CLI 工具说明（`uvx coopie`、`coopie -U`、CLI 选项表）；生成后步骤补充 Make 快捷命令段 |
| `template/README.md` | 修改 | badge 区补充 PyPI 版本 badge（置首）；新增"特性"段，按 `use_cicd`/`use_docs`/`use_tox`/`use_docker` 条件渲染 |
| `docs/index.rst` | 修改 | 重写：补充 RST 格式 badge（image directive + 替换引用）；补充用法段（CLI + copier 命令）；补充 Make 快捷命令段；修复"简介"重复句号；开发命令与 Makefile 对齐 |
| `.trae/req/req-06-README与项目文档完善.md` | 新建 | 需求分析文档 |
| `pyproject.toml` / `src/coopie/__init__.py` | bump | 0.1.12 → 0.1.13 |
| `.copier-answers.yml` | 迁移 | `_commit: v0.1.12 → v0.1.13` |

## 关键决策与依据

1. **badge 顺序**：PyPI 版本置首（最重要的版本信息），其后 CI → Python → License → Coverage。项目根与模板一致。

2. **模板特性段条件渲染**：`{% if use_cicd %}`/`{% if use_docs %}`/`{% if use_tox %}`/`{% if use_docker %}` 条件渲染对应特性行，与项目实际配置匹配。`tox_envlist` 变量渲染多版本测试范围（如 `py38, py39, ..., py314`）。

3. **README 结构性冲突**：copier update 迁移 `_commit` 时，项目根 README（自定义文档）与模板 README 渲染结果整体冲突，用 `git checkout --ours README.md` 保留项目版本。这是 iter-05 记录的结构性问题，每次模板 README 改动都会触发。

4. **docs/index.rst badge 格式**：RST 用 `.. |name| image:: url :target: url :alt: text` 声明替换引用，再用 `|name| |name2|` 行内显示。与 Markdown badge 功能等价但语法不同。

5. **.dockerignore/Dockerfile 误删恢复**：bump 时发现这两个文件被删除（原因未明，疑似历史 `make clean` 副作用或 copier update 行为），用 `git checkout --` 恢复。

## 验证结果

- `make check`：ruff 全绿、pyrefly 0 errors、pytest 23 passed、覆盖率 100%。
- 模板渲染验证（非 git 副本 `copier copy`）：README badge 正确渲染（PyPI/CI/Python/License/Coverage），特性段条件渲染正确。
- 干净 `uvx copier update -A`：`Keeping template version 0.1.13`，无冲突无错误。

## 提交历史

```
bdf96c2 chore: 迁移 _commit 至 v0.1.13 完成 README 文档完善同步
cbd0b57 chore: bump version 0.1.12 → 0.1.13  (tag: v0.1.13)
91f907f docs: 完善 README 与项目文档
```

## 遗留事项

1. **README 结构性冲突**：每次 copier update 改模板 README 时都会整体冲突，需手动 `git checkout --ours README.md`。
2. **.dockerignore/Dockerfile 误删原因未明**：bump 时发现被删除，恢复后正常。需关注后续是否复现。
3. **rule-01 需求分析**：本次迭代已按新规则创建 `.trae/req/req-06` 需求文档并确认，后续迭代继续遵守。
