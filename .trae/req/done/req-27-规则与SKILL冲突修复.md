# req-27：规则与 SKILL 冲突修复

## 背景

iter-26 创建 `python-project-structure` SKILL 后，对 `.trae/rules/` 与 `.trae/skills/` 全部文件做系统性冲突检查，发现 11 项问题（P0-P4 优先级）：版本陈旧、内部重复、跨文档重复、目录结构不一致、规则与 SKILL 缺乏双向引用、规则文件内部不一致等。需按优先级系统性修复，确保规则与 SKILL 形成清晰的双向引用网，避免维护时遗漏同步。

## 需求

- [x] P0-C1：python-performance SKILL GitHub Actions 版本更新（actions/checkout@v4 → v5、setup-uv@v3 → v8.3.2，添加 enable-cache 与 cache-dependency-glob），根 + 模板同步
- [x] P1-C3：python-testing SKILL 内部 pytest.ini 去重（合并"标记注册"章节与"测试配置文件"章节，避免同文件内重复示例）
- [x] P1-R1：python-project-structure SKILL 移除 .coveragerc 重复示例（改为引用 python-testing SKILL「覆盖率」章节），避免跨文档重复
- [x] P2-C2：测试目录结构在两 SKILL 间统一（python-testing 与 python-project-structure 均补 `gui/` 与 `fixtures/` 子目录），根 + 模板同步
- [x] P2-D1+P3-R2：rule-11 加 SKILL 反向引用（工具链章节末尾加引用块 + 文件末尾加「详细参考」附录表，建立 rule → SKILL 双向引用），根 + 模板同步
- [x] P3-D2：rule-12 加 python-gui-pyside SKILL 引用（末尾加「详细参考」章节），根 + 模板同步
- [x] P3-D3：rule-01 暂停条件括号内补 `.pre-commit-config.yaml`（之前提到"修改 pre-commit"但未列文件名），根 + 模板同步
- [x] P4-S2：rule-01 加 rule-02 例外注解（暂停条件第 2 条补"修改 `.trae/rules/` 下规则文件（见 rule-02 规则变更约束）"），根 + 模板同步
- [x] 验证：`make render` 4 种 project_type 全部渲染成功；rule-01/11/12 同步性检查通过；SKILL 同步性检查通过（python-subprocess 是 Jinja 模板化预期差异；python-config/logging 有 CRLF/LF 历史遗留不影响本轮）
