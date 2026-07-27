# req-29：规则与 SKILL 体系清理整理

## 背景

iter-28 完成迭代流程六步化与 Python/PySide 规则 SKILL 化后，需对整个规则与 SKILL 体系做系统性冲突与冗余检查，清理不必要内容，确保体系内聚清晰。

## 需求

- [x] P0：归档 `.trae/req/` 下 9 个已完成但未归档的需求文件（req-19~req-27，req-22/28 此前已归档）到 `.trae/req/done/`，恢复 rule-02 需求记录约束
- [x] P1 评估：python-standards 与各专项 SKILL 概念性重叠——评估为设计意图（简表 vs 详细模式），iter-27 已通过引用方式修复实质性重复，无需处理
- [x] P2 评估：rule-03 提及 python-fastapi SKILL 但根目录无——评估为设计意图（仅 web 项目生成），无需处理
- [x] P3 评估：根目录 python-gui-pyside SKILL 硬编码 `coopie`——评估为双份同步约定（根目录为 coopie 自身用，template 为模板源），保留
- [x] P4 评估：python-config/python-logging SKILL CRLF/LF 差异——修复需改 .gitattributes（工具链配置变更，暂停边界），暂不处理
- [x] P5 评估：rule-09 命令行传递章节——对 Windows/PowerShell 用户必要，保留
