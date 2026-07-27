# 需求清单

- [x] R1：迭代循环从「计划 → 实现 → 测试 → 文档 → 验证」五步升级为「收集 → 计划 → 实现 → 测试 → 文档 → 验证」六步。
- [x] R2：明确"每次用户需求驱动 20 轮迭代任务"作为默认迭代规模，写入 rule-01。
- [x] R3：迭代任务之间不询问用户意见（强化既有"迭代间自动衔接"约束）。
- [x] R4：新增"收集"环节定义：获取前一轮或几轮迭代后的信息（含 CI/CD 执行结果，失败则纳入本轮计划修复）；获取本轮计划所需的最佳实践 SKILL（与已有 SKILL 冲突则整合，必要时找用户确认）。
- [x] R5：将 `rule-11-python-standards.md` 移动到 `python-standards` SKILL 模块。
- [x] R6：将 `rule-12-pyside-dev.md` 内容整合到 `python-gui-pyside` SKILL 模块。
- [x] R7：同步更新 rule-01、rule-03 中对 rule-11/rule-12 的引用为 SKILL 引用。
- [x] R8：根目录 `.trae/` 与 `template/.trae/` 双份同步。
