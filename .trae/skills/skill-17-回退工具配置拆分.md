# skill-17：回退工具配置拆分（归档自 iter-17/req-17）

## 迭代目标

回退 iter-16 的工具配置拆分方案，将 ruff/pyrefly/coverage/pytest 工具配置放回 pyproject.toml，移除 `_skip_if_exists`，回到 iter-16 前的原始状态。

## 需求确认

用户反馈 iter-16 方向错误：工具配置相对标准不需要拆分，`[project.optional-dependencies]` 这类用户频繁定制的项目相关内容才需要解析合并措施。用户选择方案 D（回退拆分 + 接受原始状态）。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `template/pyproject.toml` | 修改 | 恢复工具配置段（coverage/pytest/ruff/pyrefly，Jinja 变量版） |
| `pyproject.toml` | 修改 | 恢复工具配置段（渲染值版，版本保持 0.4.4） |
| `copier.yml` | 修改 | 移除 `_skip_if_exists` 段（3 行） |
| `template/ruff.toml` | 删除 | iter-16 创建的独立配置 |
| `template/pyrefly.toml` | 删除 | iter-16 创建的独立配置 |
| `template/.coveragerc` | 删除 | iter-16 创建的独立配置 |
| `template/pytest.ini` | 删除 | iter-16 创建的独立配置 |
| `ruff.toml` | 删除 | iter-16 创建的独立配置 |
| `pyrefly.toml` | 删除 | iter-16 创建的独立配置 |
| `.coveragerc` | 删除 | iter-16 创建的独立配置 |
| `pytest.ini` | 删除 | iter-16 创建的独立配置 |

## 关键决策与依据

1. **回退到 iter-16 前准确状态**：通过 `git show 1693e92:<file>` 获取 iter-16 重构提交前的文件内容，确保回退准确。工具配置段的键顺序与 1693e92 完全一致（template 的 `[tool.coverage.report]` 为 `fail_under` 在前，项目根为 `exclude_lines` 在前——这是 iter-16 前就已存在的渲染差异）。

2. **`[project.optional-dependencies]` 合并问题暂不解决**：用户选择的方案 D 是"接受原始状态"，即回到 copier 行级 diff3 三方合并。该问题的其他方案（_tasks 脚本用 tomllib 合并、_migrations 版本迁移）均未被选择，留待未来需要时再评估。

3. **归档 iter-13/req-13 → skill-13**：添加 iter-17 后 docs/ 和 req/ 各达 5 文件，触发 rule-01 归档阈值（≥5），归档最旧的 iter-13/req-13 至 skill-13，目录降至 4 文件。

## 验证结果

- ruff check：All checks passed!
- ruff format --check：5 files already formatted
- pyrefly check：0 errors
- pytest：42 passed, 100% coverage
- git status：3 个修改文件（copier.yml/pyproject.toml/template/pyproject.toml）+ 8 个删除文件

## 遗留事项

- `[project.optional-dependencies]` 的 TOML 语义合并问题仍未解决，用户在 copier update 时可能遇到依赖列表行级冲突。当前接受 copier 行级 diff3 行为，冲突时手动解决。

## 需求清单（归档自 req-17）

- [x] 恢复 template/pyproject.toml 工具配置段（Jinja 变量版）
- [x] 恢复 pyproject.toml 工具配置段（渲染值版）
- [x] 移除 copier.yml 中的 `_skip_if_exists` 段
- [x] 删除 8 个独立配置文件（template/ 和项目根各 4 个）
- [x] make check 验证回退后状态正常
- [x] bump 版本 0.4.4 → 0.4.5 + push
- [x] 更新 memory 文件（移除 _skip_if_exists 约定）

## 约束

- 回退到 iter-16 前（commit 1693e92）的准确状态，不引入新变更
- `[project.optional-dependencies]` 的 TOML 语义合并问题暂不解决（接受 copier 行级 diff3 原始状态）
- 标准门禁：ruff + pyrefly + pytest 95% 覆盖率

## 验收标准

- pyproject.toml（项目根 + 模板）包含完整的工具配置段
- copier.yml 无 `_skip_if_exists` 段
- 8 个独立配置文件已删除
- make check 全绿
