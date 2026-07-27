# iter-28：迭代流程与规则 SKILL 化

## 需求清单

- [x] R1：迭代循环从「计划 → 实现 → 测试 → 文档 → 验证」五步升级为「收集 → 计划 → 实现 → 测试 → 文档 → 验证」六步。
- [x] R2：明确"每次用户需求驱动 20 轮迭代任务"作为默认迭代规模，写入 rule-01。
- [x] R3：迭代任务之间不询问用户意见（强化既有"迭代间自动衔接"约束）。
- [x] R4：新增"收集"环节定义：获取前一轮或几轮迭代后的信息（含 CI/CD 执行结果，失败则纳入本轮计划修复）；获取本轮计划所需的最佳实践 SKILL（与已有 SKILL 冲突则整合，必要时找用户确认）。
- [x] R5：将 `rule-11-python-standards.md` 移动到 `python-standards` SKILL 模块。
- [x] R6：将 `rule-12-pyside-dev.md` 内容整合到 `python-gui-pyside` SKILL 模块。
- [x] R7：同步更新 rule-01、rule-03 中对 rule-11/rule-12 的引用为 SKILL 引用。
- [x] R8：根目录 `.trae/` 与 `template/.trae/` 双份同步。

## 迭代目标

按用户三大核心需求重构开发流程规则与 SKILL 体系：（1）迭代循环升级为六步（新增"收集"环节），并固化"每次用户需求默认驱动 20 轮迭代任务、迭代间不询问用户意见"约束；（2）明确"收集"环节职责——回顾前序迭代、获取 CI/CD 结果、获取最佳实践 SKILL 并处理冲突；（3）将 Python 与 PySide 硬约束规则（rule-11/rule-12）迁移到 SKILL 模块，rules/ 目录仅保留流程性与全局性规则。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `.trae/rules/rule-01-开发流程.md` | 修改 | 核心原则第2条五步→六步；新增"迭代规模"原则（20 轮、迭代间不询问）；自主执行保障第1条补"20 轮连续推进"；迭代循环新增"收集"步骤（含回顾前序/CI-CD/SKILL/需求扫描四个子项）；"计划"补"CI/CD 失败修复列为高优先级子任务"；"实现"中 `rule-11-python-standards.md` 引用改为 `python-standards` SKILL；多阶段项目/收尾中"回「计划」"改为"回「收集」" |
| `template/.trae/rules/rule-01-开发流程.md` | 修改 | 同步根目录变更 |
| `.trae/rules/rule-03-触发场景.md` | 修改 | "Python 项目须遵守 `rule-11-python-standards.md` 硬约束"改为"Python 项目开发前**必须**调用 `python-standards` SKILL"；语言场景列表新增 `python-standards` SKILL 条目；PySide 项目场景描述补充"含 PySide 硬约束简表、设计系统、四区布局..." |
| `template/.trae/rules/rule-03-触发场景.md` | 修改 | 同步根目录变更 |
| `.trae/rules/rule-11-python-standards.md` | 删除 | 内容迁移到 `python-standards` SKILL |
| `.trae/rules/rule-12-pyside-dev.md` | 删除 | 内容整合到 `python-gui-pyside` SKILL |
| `template/.trae/rules/rule-11-python-standards.md` | 删除 | 同步根目录删除 |
| `template/.trae/rules/rule-12-pyside-dev.md` | 删除 | 同步根目录删除 |
| `.trae/skills/python-standards/SKILL.md` | 新建 | rule-11 内容 SKILL 化：frontmatter（name+description）+ 何时调用 + 16 章硬约束简表 + 详细参考附录表；硬编码 `coopie`/`95`/`py38`/`3.8` |
| `template/.trae/skills/python-standards/SKILL.md` | 新建 | 同步根目录结构，Jinja 化：`{{ package_name }}`/`{{ coverage_fail_under }}`/`{{ target_py }}`/`{{ min_python_version }}` |
| `.trae/skills/python-gui-pyside/SKILL.md` | 修改 | "双兼容"章节后插入「## 硬约束简表」章节（架构与分层/配置与资源/控件与窗口生命周期/性能），内容来自 rule-12 |
| `template/.trae/skills/python-gui-pyside/SKILL.md` | 修改 | 同步根目录变更 |
| `.trae/skills/python-class-design/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（1 处） |
| `.trae/skills/python-testing/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（1 处） |
| `.trae/skills/python-subprocess/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（6 处） |
| `.trae/skills/python-performance/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（2 处） |
| `.trae/skills/python-config/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（4 处） |
| `.trae/skills/python-cli/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（6 处） |
| `.trae/skills/python-logging/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（4 处） |
| `.trae/skills/python-project-structure/SKILL.md` | 修改 | rule-11/rule-12 引用替换为对应 SKILL（7 处） |
| `template/.trae/skills/python-class-design/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/python-testing/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/python-subprocess/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/python-performance/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/python-config/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/python-cli/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/python-logging/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/python-project-structure/SKILL.md` | 修改 | 同步根目录变更 |
| `template/.trae/skills/{% if project_type == 'web' %}python-fastapi{% endif %}/SKILL.md` | 修改 | rule-11 引用替换为 `python-standards` SKILL（1 处） |
| `.trae/req/req-28-迭代流程与规则SKILL化.md` | 新建 | 需求记录（已完成） |

## 关键决策与依据

1. **六步循环新增"收集"作为第一步**：用户需求明确要求"收集 → 计划 → 实现 → 测试 → 文档 → 验证"。收集环节定义为四个子项：回顾前序迭代、获取 CI/CD 结果、获取最佳实践 SKILL、扫描需求清单。其中"获取 CI/CD 结果"在 CI/CD 失败时将修复任务纳入本轮计划——这把"被动修复"变为"主动收集"，避免 CI/CD 红灯被遗忘。

2. **20 轮迭代规模作为默认值写入核心原则**：用户要求"每次用户需求驱动 20 轮迭代任务"。放在核心原则而非自主执行保障中，强调其作为流程硬约束（非建议）。同时在自主执行保障第1条补"20 轮迭代任务在初始确认范围内连续推进，不因单轮完成而暂停询问"——消除"单轮完成是否要继续"的歧义。

3. **迭代间不询问用户意见的强化**：原 rule-01 已有"迭代间自动衔接"，本轮在其基础上补"20 轮连续推进，不因单轮完成而暂停询问"，进一步固化"长任务自主执行"语义。

4. **rule-11 移动到 `python-standards` SKILL（而非分散到各 SKILL）**：rule-11 是跨领域通用硬约束简表（工具链/类型注解/数据结构/并发/测试/日志/安全/性能/Git 等），各章节已有对应专项 SKILL 承载详细模式。选择独立成 SKILL 而非分散整合，原因：（a）保留"硬约束简表"作为单一查阅入口，避免读者在 11 个 SKILL 间跳转找硬约束；（b）各专项 SKILL 仍承载详细模式与代码模板，分工清晰；（c）与 rule-03 触发场景中"Python 项目开发前**必须**调用 `python-standards` SKILL"形成单向引用，闭环明确。

5. **rule-12 整合到 `python-gui-pyside` SKILL（而非独立成新 SKILL）**：与 rule-11 不同，rule-12 是 PySide 单领域硬约束，python-gui-pyside SKILL 已是该领域的唯一 SKILL。选择整合而非独立：（a）避免新增仅含简表的 SKILL 增加导航成本；（b）python-gui-pyside SKILL 已有"双兼容（关键约束）"章节作为硬约束性质内容，"硬约束简表"作为独立章节插入位置自然；（c）rule-12 末尾原本就指向 python-gui-pyside SKILL，整合后形成单一来源。

6. **template 版本 python-standards SKILL Jinja 化**：rule-11 template 版本原本硬编码 `coopie`/`95`（历史遗留，未 Jinja 化）。迁移到 SKILL 时一并修复：`{{ package_name }}`/`{{ coverage_fail_under }}`/`{{ target_py }}`/`{{ min_python_version }}`。其他 SKILL（python-testing/python-project-structure）已 Jinja 化，新 SKILL 保持一致。

7. **SKILL 引用替换统一格式**：所有 SKILL 文件中对 rule-11/rule-12 的引用统一替换为 `` `python-standards` SKILL `` 与 `` `python-gui-pyside` SKILL ``（仅 SKILL 名用反引号，"SKILL" 词不带反引号）。替换按长串优先（`rule-11-python-standards.md` → `rule-11`），避免短串误匹配。

8. **rules/ 目录精简为 4 个文件**：删除 rule-11/rule-12 后，rules/ 仅保留 rule-01（开发流程）、rule-02（产物约束）、rule-03（触发场景）、rule-09（git 提交规则）——全部为流程性/全局性规则。Python 与 PySide 硬约束全部 SKILL 化，rules/ 与 skills/ 职责清晰分离。

9. **"未达标准回「收集」"而非"回「计划」"**：六步循环后，回退起点改为"收集"。原因：收集是六步之首，回退到收集可以重新评估 CI/CD 状态、SKILL 适用性、需求清单，避免直接进入计划而忽略环境变化。

## 代码实现情况

### R1-R4：rule-01 六步循环与收集环节

核心原则新增"迭代规模"条；自主执行保障第1条补"20 轮连续推进"；迭代循环新增"收集"步骤（含四个子项），"计划"补 CI/CD 失败修复优先级，"实现"中 rule-11 引用改为 `python-standards` SKILL；多阶段项目与收尾中"回「计划」"改为"回「收集」"。

### R5：python-standards SKILL 新建

新 SKILL 位于 `.trae/skills/python-standards/SKILL.md` 与 `template/.trae/skills/python-standards/SKILL.md`。结构：frontmatter（name/description）→ 标题 → 概述 → 何时调用 → 工具链 → 兼容性 → 类型注解 → 数据结构 → 模块与导入 → 函数设计 → 异常处理 → 并发 → 测试 → 代码风格 → Pythonic 风格 → 日志 → 路径与资源 → 安全 → 性能 → Git 与提交 → 详细参考（附录表）。内容与原 rule-11 完全一致（除 frontmatter 与"何时调用"章节为新增）。

### R6：python-gui-pyside SKILL 整合 rule-12

在 python-gui-pyside SKILL.md 的「双兼容」章节后、「项目骨架」章节前，插入「## 硬约束简表」章节，包含四个子章节：架构与分层、配置与资源、控件与窗口生命周期、性能。内容与原 rule-12 完全一致（除"详细参考"章节，因 SKILL 自身即是详细参考目的地）。

### R7：rule-03 触发场景更新

语言场景首段改为"Python 项目开发前**必须**调用 `python-standards` SKILL 获取跨领域通用硬约束"；列表新增 `python-standards` SKILL 条目；PySide 项目场景描述补充"含 PySide 硬约束简表、设计系统、四区布局、信号槽、QThread、QSS 样式等"。

### R8：根目录与 template 双份同步

所有改动在根目录与 template 同步：
- rule-01/rule-03：内容完全相同（无 Jinja 变量）
- python-standards SKILL：根目录硬编码 `coopie`/`95`/`py38`/`3.8`；template Jinja 化 `{{ package_name }}`/`{{ coverage_fail_under }}`/`{{ target_py }}`/`{{ min_python_version }}`
- python-gui-pyside SKILL：内容完全相同（无 Jinja 变量）
- 其他 9 个 SKILL：仅 rule-11/rule-12 引用替换，无 Jinja 变量化改动

### SKILL 引用替换（17 个文件、59 处）

按长串优先顺序：`rule-11-python-standards.md` → `rule-11` → `rule-12-pyside-dev.md` → `rule-12`，分别替换为 `` `python-standards` SKILL `` 与 `` `python-gui-pyside` SKILL ``。

## 整合优化情况

- **rules/ 目录精简**：从 6 个文件减至 4 个，全部为流程性/全局性规则；Python/PySide 硬约束全部 SKILL 化。
- **SKILL 体系扩展**：新增 `python-standards` SKILL 作为跨领域通用硬约束总纲，与其他 11 个专项 SKILL 形成"总纲 + 专项"双层结构。
- **rule ↔ SKILL 引用网简化**：rule-03（触发调度）→ python-standards SKILL（Python 通用）→ 各专项 SKILL（详细模式）；rule-03 → python-gui-pyside SKILL（PySide 全栈）。原 rule-11/rule-12 末尾的"详细参考"附录表迁移到 python-standards SKILL 末尾，python-gui-pyside SKILL 自身即承载详细参考。
- **历史遗留 Jinja 化修复**：rule-11 template 版本原本硬编码 `coopie`/`95`，迁移到 SKILL 时一并 Jinja 化。
- **收集环节闭环化**：CI/CD 失败 → 收集 → 计划修复 → 实现 → 测试 → 验证；SKILL 冲突 → 收集 → 整合/找用户确认 → 计划。两条闭环显式写入 rule-01。

## 测试验证结果

- **copier 模板渲染验证**：`make render` 4 种 project_type（library/cli/gui/web）全部渲染成功，无 Jinja 错误。
- **python-standards SKILL 生成验证**：4 种 project_type 渲染后均生成 `.trae/skills/python-standards/SKILL.md` ✓
- **rule-11/rule-12 删除验证**：4 种 project_type 渲染后 `.trae/rules/` 仅含 4 个规则文件（rule-01/02/03/09）✓
- **Jinja 变量渲染验证**：渲染后 python-standards SKILL 中 `{{ package_name }}` → `my_project`、`{{ coverage_fail_under }}` → `95`、`{{ target_py }}` → `py38`、`{{ min_python_version }}` → `3.8`，无残留 `{{` 或 `{%` ✓
- **rule-01 内容验证**：渲染后 rule-01 第11行包含"六步" ✓，第12行包含"20 轮迭代任务" ✓，第29行包含"收集"步骤 ✓，第31行包含"获取 CI/CD 执行结果" ✓
- **python-gui-pyside SKILL 验证**：渲染后第31行包含"## 硬约束简表" ✓
- **rule-11/rule-12 残留检查**：
  - `.trae/rules/` 与 `template/.trae/rules/`：无 rule-11/rule-12 残留 ✓
  - `.trae/skills/` 与 `template/.trae/skills/`：无 rule-11/rule-12 残留（17 个 SKILL 文件 59 处引用全部替换）✓
- **历史记录保留**：`.trae/docs/iter-*.md`、`.trae/req/*.md`、`docs/changelog.rst` 中的 rule-11/rule-12 引用作为历史记录保留，未修改。

## 遗留事项

- python-gui-pyside SKILL 的 template 版本仍硬编码 `coopie`（如 `src/coopie/`、`from coopie import theme`、`coopie GUI 入口`等代码模板），未 Jinja 化为 `{{ package_name }}`。这是历史遗留问题（与 rule-11 同期），本轮未处理。建议后续统一 Jinja 化。
- python-config 与 python-logging SKILL 在根目录与 template 目录存在 CRLF/LF 行尾差异（iter-27 遗留），本轮未处理。

## 下一轮计划

无明确下一轮计划。本轮完成后，rules/ 目录精简为 4 个流程性规则文件，Python/PySide 硬约束全部 SKILL 化，迭代循环升级为六步并固化 20 轮规模与迭代间不询问约束。后续可根据使用反馈继续调整。
