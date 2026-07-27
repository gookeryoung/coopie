# iter-21 需求：GUI 设计规范与 template/rule-12 填充

## 背景

`template/.trae/rules/rule-12-gui-pyside-standards.md` 当前为空。需基于 Figma 设计（`https://www.figma.com/slides/iJJHXhX1oKDJmB8QvGdOBf`）结合 PySide2/6 最佳实践，建立基于工作流的桌面 GUI 设计规范，填充该文件，随模板分发给用户项目。

## 需求来源

用户请求："请给予 FIGMA 设计，建立基于工作流的桌面 GUI 的设计规范，结合 pyside2/6 最佳实践制定。"

## 范围（用户确认）

- **目标文件**：`template/.trae/rules/rule-12-gui-pyside-standards.md`（当前为空，填充后随模板分发）
- **工作流场景**：通用布局与导航（主窗口/侧边栏/工具栏/状态栏布局，菜单与导航模式）
- **Figma 内容获取**：用户导出关键页面图片，Agent 读取图像分析提取设计规范
- **结合点**：在 PySide2/6 技术规范基础上，补充设计层面的规范（布局栅格、间距尺度、导航模式、组件层级等）

## 需求清单

- [x] 1. 接收并分析用户导出的 Figma 图片，提取设计要素（布局结构、导航模式、间距/尺度、组件层级）
- [x] 2. 起草 `template/.trae/rules/rule-12-gui-pyside-standards.md` 内容，结构包含：
  - [x] 2.1 概述与适用范围
  - [x] 2.2 工具链（PySide2/PySide6 兼容）
  - [x] 2.3 布局规范（主窗口结构、栅格、间距尺度）
  - [x] 2.4 导航模式（侧边栏/Tab/面包屑等）
  - [x] 2.5 组件层级与样式（QSS、主题）
  - [x] 2.6 信号槽与状态管理
  - [x] 2.7 线程与长任务
  - [x] 2.8 测试（pytest-qt）
  - [x] 2.9 打包（PyInstaller）
- [x] 3. 同步保留项目根 `.trae/rules/rule-12-pyqt-standards.md`（项目自身使用，不强制同步）
- [x] 4. 验证：模板渲染检查（`copier copy` 非 git 副本，确认 rule-12 文件正确生成）
- [x] 5. 版本 bump + _commit 迁移 + copier update 验证
- [x] 6. 创建 iter-21 文档，归档检查

## 约束

- 修改 `.trae/rules/` 需用户授权（已获：用户确认填充 template/rule-12）
- PySide2/PySide6 双兼容（Python ≤ 3.10 / ≥ 3.11）
- 不增加新依赖
- 设计规范须可执行（有具体尺度/模式，非泛泛而谈）

## 不在范围

- 不改 iter-19/iter-20 的 CLI/Makefile 逻辑
- 不涉及表单/CRUD/对话框工作流（本次仅"通用布局与导航"；后续可扩展）
- 不修改项目根 rule-12（除非用户后续要求同步）

## 待用户提供

- Figma 导出的关键页面图片（PNG/JPG），覆盖主窗口布局与导航模式
