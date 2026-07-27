# iter-30：项目与文档完善

## 需求清单

- [x] P1：修复 copier.yml `_skip_if_exists` 中 `src/{{ project_name }}/*.py` 应为 `src/{{ package_name }}/*.py`（bug：project_name 含连字符，package_name 才是合法包名）
- [x] P2：修复 docs/index.rst 文档结构——toctree 缺少 usage/parameters 引用；"快速上手"部分 `import coopie` 错误（coopie 是 CLI 工具不是导入库）
- [x] P2+：修复 Sphinx 构建警告——api.rst 标题下划线过短；changelog.rst 第 9 行 inline literal 解析问题
- [x] P3 评估：changelog.rst v0.9.0（未发布）但版本号仍 0.8.7——release 流程问题，不在本轮处理
- [x] P4 评估：无 .gitattributes 导致工作区 CRLF/LF 混合——属 git config 变更（rule-01 暂停条件第 2 条），标注待用户确认
- [x] P5 评估：iter-29 P4 记录的 CRLF/LF 差异实际已自愈（git ls-files --eol 显示 SKILL 文件均为 LF），无需处理
- [x] 清理 iter-25（最旧记录），保持 iter 记录数 ≤ 5（rule-02 约束）

## 迭代目标

按用户"完善项目和文档"需求，系统性检查项目代码、配置与文档的一致性问题，修复明确 bug 与文档结构缺陷，评估其余疑似问题并记录决策。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `copier.yml` | 修改 | 第 197 行 `src/{{ project_name }}/*.py` → `src/{{ package_name }}/*.py`（修复 `_skip_if_exists` glob 匹配错误） |
| `docs/index.rst` | 重写 | toctree 补全 usage/parameters；删除错误的 `import coopie` 示例；整合 README 核心内容；引用 usage/parameters 文档 |
| `docs/api.rst` | 修改 | 标题下划线 `=======`（7 字符）→ `========`（8 字符），消除 Sphinx 警告 |
| `docs/changelog.rst` | 修改 | 第 9 行 ``>=3.8`` / ``>=3.9`` 改为 `3.8` / `3.9`，消除 inline literal 解析警告 |
| `.trae/docs/iter-25-工具链配置拆分.md` | 删除 | rule-02 迭代记录数 ≤ 5 约束，清理最旧 |
| `.trae/docs/iter-30-项目与文档完善.md` | 新建 | 本轮迭代记录 |
| `.trae/req/done/req-30-项目与文档完善.md` | 新建 | 本轮需求记录（直接归档） |

## 关键决策与依据

1. **P1 copier.yml `_skip_if_exists` bug 修复**：`_skip_if_exists` 的 glob 模式 `src/{{ project_name }}/*.py` 使用了 `project_name`（如 `my-project`），但实际包目录是 `src/{{ package_name }}/`（如 `my_project`，下划线替换连字符）。这导致 `copier update` 时用户修改的 Python 源文件不会被跳过，可能被模板覆盖。修复为 `src/{{ package_name }}/*.py`。

2. **P2 docs/index.rst 文档结构重构**：原 index.rst 存在三个问题：(a) toctree 只有 api/changelog，缺少 usage/parameters 引用，导致这两个文档孤立；(b) "快速上手"部分 `import coopie` + `# TODO: 添加使用示例` 是错误的（coopie 是 CLI 工具，不是导入的库）；(c) 内容过于简略且与 README 重复。重写为完整的文档首页：简介（含模板特性列表）→ 安装 → 快速上手（CLI 命令示例）→ 更新已有项目 → 开发，toctree 引用 usage/parameters/api/changelog 四个文档。

3. **P2+ Sphinx 构建警告修复**：
   - api.rst 标题 `API 参考`（6 字符）下划线 `=======`（7 字符）触发 "Title underline too short" 警告。虽然 7 > 6，但 Sphinx 对中文字符的宽度计算可能不同，加长到 8 字符消除警告。
   - changelog.rst 第 9 行 ``requires-python`` 从 ``>=3.8`` 升至 ``>=3.9`` 触发 "Inline literal start-string without end-string" 警告。原因是 RST 解析器在处理连续的 inline literal（``>=3.8`` 升至 ``>=3.9``）时解析混乱。改为纯文本 `3.8` / `3.9` 消除警告，语义无损失。

4. **P3 版本号不一致评估保留**：changelog.rst 有 `v0.9.0（未发布）` 条目，但 `__version__ = "0.8.7"` / `pyproject.toml` version = "0.8.7"。这是 release 流程问题：v0.9.0 的功能已实现并写入 changelog，但版本号未 bump。按 release 流程，应在发布时通过 `make bump patch`（或 minor）统一更新，不在本轮处理。

5. **P4 .gitattributes 缺失评估保留**：项目无 .gitattributes 文件，`git ls-files --eol` 显示多个文件工作区为 CRLF（Windows 检出默认），仓库存储为 LF。添加 .gitattributes 可强制 LF 统一，但属 git config 变更（rule-01 暂停条件第 2 条 "修改 CI/git config"）。决策标注待用户确认，不在本轮自主添加。

6. **P5 iter-29 P4 遗留事项已自愈**：iter-29 记录 "python-config 与 python-logging SKILL CRLF/LF 差异"，实际 `git ls-files --eol` 检查显示两个文件在根目录与 template 目录均为 LF（i/lf w/lf）。差异可能已在某次提交中被 git 规范化，无需处理。

7. **iter-25 清理**：新增 iter-30 后，`.trae/docs/` 下 iter 记录达 6 个，超过 rule-02 "保留最新 5 条记录"阈值。按 rule-02 "从最旧记录开始清理"规定，删除 iter-25（最旧）。iter-25 内容为"工具链配置拆分"，已完成且代码已体现，删除迭代记录不影响代码。

## 代码实现情况

### P1：copier.yml _skip_if_exists 修复

```yaml
# 修复前
_skip_if_exists:
  - "src/{{ project_name }}/*.py"   # project_name = my-project（含连字符，非法包名）

# 修复后
_skip_if_exists:
  - "src/{{ package_name }}/*.py"   # package_name = my_project（合法包名）
```

### P2：docs/index.rst 重写

- toctree 从 `api, changelog` 扩展为 `usage, parameters, api, changelog`
- 删除错误的 `import coopie` + `# TODO: 添加使用示例`
- 整合 README 核心内容：简介（含模板特性列表）、安装、快速上手（CLI 命令示例）、更新已有项目、开发
- 使用 `:doc:` 角色交叉引用 usage/parameters 文档

### P2+：Sphinx 警告修复

- api.rst：`=======`（7 字符）→ `========`（8 字符）
- changelog.rst：``>=3.8`` / ``>=3.9`` → `3.8` / `3.9`

### iter-25 清理

使用 `git rm` 删除 `.trae/docs/iter-25-工具链配置拆分.md`。清理后 `.trae/docs/` 下保留 iter-26~iter-30 共 5 个迭代记录，符合 rule-02 约束。

## 整合优化情况

- **文档结构完整性恢复**：docs/index.rst toctree 现引用全部 4 个文档（usage/parameters/api/changelog），无孤立文档。
- **Sphinx 构建 0 警告**：修复 api.rst 标题下划线与 changelog.rst inline literal 解析问题，`make doc` 输出 "构建成功" 无警告。
- **copier 模板正确性修复**：`_skip_if_exists` glob 模式现在正确匹配用户包目录，`copier update` 不会覆盖用户修改的 Python 源文件。
- **iter 记录数合规**：清理 iter-25 后，迭代记录数从 6 降至 5，符合 rule-02 "保留最新 5 条"约束。

## 测试验证结果

- **make render**：4 种 project_type（library/cli/gui/web）全部渲染成功，无 Jinja 错误 ✓
- **make doc**：Sphinx 构建成功，0 警告（修复前 2 警告）✓
- **copier.yml 语法**：YAML 语法正确，`_skip_if_exists` glob 模式正确 ✓
- **iter 记录数验证**：`.trae/docs/` 下 5 个迭代记录（iter-26~30）✓

## 遗留事项

- P4：添加 .gitattributes 强制 LF 统一（git config 变更，rule-01 暂停条件第 2 条），建议后续迭代处理或用户确认后添加。

## 下一轮计划

无明确下一轮计划。本轮完成项目代码（copier.yml bug）与文档（index.rst 结构 + Sphinx 警告）的完善，其余疑似问题经评估保留并记录决策依据。项目当前文档结构完整、构建无警告、模板渲染正确。
