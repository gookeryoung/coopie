# skill-14：精简 README 用户导向（归档自 iter-14/req-14）

## 需求

- 精简项目根 README（175 行），删除/压缩非用户导向段落（特性清单、文件清单、设计依据）
- 突出快速开始、CLI 命令、可配置选项、生成后步骤
- 修正 use_docker 默认值（copier.yml 为 false，README 误写 true）

## 关键决策

1. **删除特性清单**：技术特点折叠到 intro 一句话，用户关心的是怎么用而非包含什么。
2. **删除文件树**：用户生成后自见，无需提前罗列。
3. **删除设计依据**：内部决策（src layout 选型等）不属于用户导向内容。
4. **修正 use_docker 默认值**：copier.yml 为 `false`，README 误写 `true`，顺带修正。
5. **author_name/email 默认值改为"git 配置"**：更准确反映 CLI 自动填充行为。

## 验证结果

- pytest 42 passed, 100% coverage
- 模板未变，无需 bump / copier update
- README 从 175 行精简至 77 行
