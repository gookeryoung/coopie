# iter-29：规则与 SKILL 体系清理整理

## 需求清单

- [x] P0：归档 `.trae/req/` 下 8 个已完成但未归档的需求文件（req-19/20/21/23/24/25/26/27）到 `.trae/req/done/`
- [x] P1 评估：python-standards 与各专项 SKILL 概念性重叠——设计意图，无需处理
- [x] P2 评估：rule-03 提及 python-fastapi SKILL 但根目录无——设计意图，无需处理
- [x] P3 评估：根目录 python-gui-pyside SKILL 硬编码 `coopie`——双份同步约定，保留
- [x] P4 评估：python-config/python-logging CRLF/LF 差异——修复需改 .gitattributes（暂停边界），暂不处理
- [x] P5 评估：rule-09 命令行传递章节——对 Windows 用户必要，保留
- [x] 清理 iter-24（最旧记录），保持 iter 记录数 ≤ 5（rule-02 约束）

## 迭代目标

按用户"分析确认规则、SKILL 是否存在冲突或者不必要的，清理整理"需求，系统性检查规则与 SKILL 体系的冲突与冗余，清理明确违反 rule-02 的需求归档缺失问题，评估并记录其余疑似冲突的处理决策。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `.trae/req/req-19-new命令网络卡死修复.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/req-20-gitee国内源与多远程推送.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/req-21-gui设计规范与模板rule12填充.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/req-23-恢复cli工具.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/req-24-移除initial_version模板变量.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/req-25-工具链配置拆分.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/req-26-python项目结构骨架SKILL.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/req-27-规则与SKILL冲突修复.md` | 移动 | 归档到 `.trae/req/done/` |
| `.trae/req/done/req-29-规则与SKILL体系清理整理.md` | 新建 | 本轮需求记录（直接归档） |
| `.trae/docs/iter-24-移除initial_version模板变量.md` | 删除 | rule-02 迭代记录数 ≤ 5 约束，清理最旧 |
| `.trae/docs/iter-29-规则与SKILL体系清理整理.md` | 新建 | 本轮迭代记录 |

## 关键决策与依据

1. **P0 需求归档为唯一明确清理项**：收集阶段系统性检查发现，req-19~req-27 共 8 个需求文件均已标记 `[x]` 完成但未归档到 `done/`，违反 rule-02 "已完成的 req 记录移动到 `.trae/req/done/` 目录下"约束。这是本轮唯一明确的清理项，其余疑似冲突经评估均为设计意图或历史遗留。

2. **P1 概念性重叠是设计意图**：python-standards SKILL 作为跨领域通用硬约束简表，与各专项 SKILL（python-class-design/python-concurrency/python-file-io/python-testing/python-logging/python-config/python-subprocess/python-performance/python-cli/python-project-structure）存在概念性重叠。这是"简表 vs 详细模式"的分层设计：python-standards 提供单一查阅入口，各专项 SKILL 提供详细模式与代码模板。iter-27 已通过引用方式修复实质性重复（如 .coveragerc/pytest.ini 示例的去重），当前引用关系健康，无需处理。

3. **P2 python-fastapi SKILL 缺失是设计意图**：rule-03 提及 `python-fastapi` SKILL，根目录 `.trae/skills/` 无此 SKILL，template 目录有（Jinja 条件生成 `{% if project_type == 'web' %}python-fastapi{% endif %}/`）。这与 python-gui-pyside SKILL 的设计模式一致：领域专属 SKILL 仅对应项目类型生成。coopie 自身是 CLI 项目，不需要 fastapi SKILL，无冲突。

4. **P3 根目录 python-gui-pyside SKILL 硬编码 `coopie` 保留**：根目录 `.trae/skills/python-gui-pyside/SKILL.md` 硬编码 `coopie`（12 处），template 版本 Jinja 化为 `{{ package_name }}`。这与 iter-28 确立的"根目录为 coopie 自身用（硬编码），template 为模板源（Jinja 化）"双份同步约定一致。coopie 自身虽是 CLI 项目不使用 GUI SKILL，但保留根目录副本可维持 SKILL 体系完整性，避免破坏同步约定。决策保留。

5. **P4 CRLF/LF 差异暂不处理**：python-config 与 python-logging SKILL 在根目录与 template 目录存在 CRLF/LF 行尾差异（iter-27/28 遗留）。修复需修改 `.gitattributes` 强制 LF 统一，但 `.gitattributes` 属工具链配置文件（rule-01 暂停条件第 2 条），需暂停确认。决策暂不处理，标注为后续待办。

6. **P5 rule-09 命令行传递章节保留**：rule-09 中"命令行传递"章节占 16 行（约 50% 篇幅），主要讲 PowerShell heredoc 不支持。对 bash/zsh 用户不必要，但对 Windows/PowerShell 用户必要（PowerShell heredoc 会原样字面量传入导致提交信息错乱）。coopie 用户的开发环境以 Windows 为主要平台，决策保留。

7. **iter-24 清理**：新增 iter-29 后，`.trae/docs/` 下 iter 记录达 6 个，超过 rule-02 "保留最新 5 条记录"阈值。按 rule-02 "从最旧记录开始清理"规定，删除 iter-24（最旧）。iter-24 内容为"移除 initial_version 模板变量"，已完成且代码已体现，删除迭代记录不影响代码。

## 代码实现情况

### P0：需求文件归档

使用 `git mv` 将 8 个已完成需求文件从 `.trae/req/` 移动到 `.trae/req/done/`：
- req-19-new命令网络卡死修复.md
- req-20-gitee国内源与多远程推送.md
- req-21-gui设计规范与模板rule12填充.md
- req-23-恢复cli工具.md
- req-24-移除initial_version模板变量.md
- req-25-工具链配置拆分.md
- req-26-python项目结构骨架SKILL.md
- req-27-规则与SKILL冲突修复.md

归档后 `.trae/req/` 目录下仅剩 `done/` 子目录，所有已完成需求集中归档。req-22/28 此前已归档。

### iter-24 清理

使用 `git rm` 删除 `.trae/docs/iter-24-移除initial_version模板变量.md`。清理后 `.trae/docs/` 下保留 iter-25~iter-29 共 5 个迭代记录，符合 rule-02 约束。

## 整合优化情况

- **恢复 rule-02 需求归档约束**：8 个已完成需求文件归档到 `done/`，需求清单扫描（收集阶段"扫描需求清单"子项）不再受已完成需求干扰。
- **iter 记录数合规**：清理 iter-24 后，迭代记录数从 6 降至 5，符合 rule-02 "保留最新 5 条"约束。
- **疑似冲突评估归档**：P1~P5 五项疑似冲突经评估均为设计意图、历史遗留或必要内容，决策与依据记入迭代记录，避免后续重复检查。

## 测试验证结果

- **归档验证**：`.trae/req/` 下仅 `done/` 子目录，`done/` 含 11 个已完成需求文件（req-18~29，除 req-22 原名"移除cli工具改为纯模板仓库"外）✓
- **iter 记录数验证**：`.trae/docs/` 下 5 个迭代记录（iter-25~29）✓
- **规则与 SKILL 引用网验证**：rules/ 目录无 rule-11/rule-12 残留引用；SKILL 间引用关系健康（python-standards 作为总纲被 11 个专项 SKILL 引用）✓

## 遗留事项

- P4：python-config 与 python-logging SKILL 的 CRLF/LF 行尾差异（iter-27/28 遗留），修复需修改 `.gitattributes`（工具链配置变更，暂停边界），建议后续迭代处理。

## 下一轮计划

无明确下一轮计划。本轮完成规则与 SKILL 体系的冲突检查与清理整理，明确清理项（P0 需求归档 + iter-24 清理）已执行，其余疑似冲突经评估保留并记录决策依据。体系当前内聚清晰，无实质性冲突。
