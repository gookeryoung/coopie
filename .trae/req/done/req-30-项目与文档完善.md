# req-30：项目与文档完善

## 背景

iter-29 完成规则与 SKILL 体系清理整理后，需对项目代码、配置与文档做系统性一致性检查，修复 bug 与文档结构缺陷。

## 需求

- [x] P1：修复 copier.yml `_skip_if_exists` 中 `src/{{ project_name }}/*.py` 应为 `src/{{ package_name }}/*.py`（bug：project_name 含连字符，package_name 才是合法包名）
- [x] P2：修复 docs/index.rst 文档结构——toctree 缺少 usage/parameters 引用；"快速上手"部分 `import coopie` 错误（coopie 是 CLI 工具不是导入库）
- [x] P2+：修复 Sphinx 构建警告——api.rst 标题下划线过短；changelog.rst 第 9 行 inline literal 解析问题
- [x] P3 评估：changelog.rst v0.9.0（未发布）但版本号仍 0.8.7——release 流程问题，不在本轮处理
- [x] P4 评估：无 .gitattributes 导致工作区 CRLF/LF 混合——属 git config 变更（rule-01 暂停条件第 2 条），标注待用户确认
- [x] P5 评估：iter-29 P4 记录的 CRLF/LF 差异实际已自愈，无需处理
