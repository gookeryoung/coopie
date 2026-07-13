# iter-21：GUI 设计规范与 template/rule-12 填充

## 迭代目标

基于用户提供的 Figma 设计图，结合 PySide2/PySide6 最佳实践，制定基于工作流的桌面 GUI 设计规范，填充 `template/.trae/rules/rule-12-gui-pyside-standards.md`（随模板分发给 GUI 类型项目）。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `template/.trae/rules/{% if project_type == 'gui' %}rule-12-gui-pyside-standards.md{% endif %}` | 新增 | 419 行，GUI 设计规范 + PySide2/6 技术标准 |
| `template/.trae/rules/{% if project_type == 'gui' %}rule-12-pyqt-standards.md{% endif %}` | 删除 | 旧空文件，避免 GUI 项目生成两个 rule-12 |
| `.copier-answers.yml` | 修改 | `_commit: v0.6.0 → v0.7.0` |
| `pyproject.toml` | 修改 | `version: 0.6.0 → 0.7.0`（bumpversion） |
| `.trae/req/req-21-gui设计规范与模板rule12填充.md` | 新增 | 需求文档 |

## 关键决策与依据

### 1. Figma 图片分析方式

模型无法直接读取图片，采用 `uv run --with pillow --with numpy python` 脚本分析：
- 颜色频率统计：提取主色调（teal #0887A0 占比 ~50%）
- 行/列亮度投影：识别横向分割线（header 40px、toolbar 50px、statusbar 28px）与纵向分割（sidebar 220px）
- 区域聚类：识别五区布局（header/toolbar/sidebar/content/statusbar）

### 2. 设计令牌提取

| 令牌 | 值 | 用途 |
|------|-----|------|
| `COLOR_PRIMARY` | `#0887A0` | 主色（teal），主操作按钮/选中态 |
| `COLOR_ACCENT` | `#87C6BB` | 辅色（mint），悬停/链接 |
| `COLOR_TEXT_SECONDARY` | `#518394` | 次要文本 |
| `COLOR_BG_MUTED` | `#E5EDE0` | 静音背景（sage） |
| `SIDEBAR_WIDTH` | `220px` | 侧边栏宽度 |
| `HEADER_HEIGHT` | `40px` | 顶栏高度 |

### 3. 文件命名与条件渲染

- 旧文件名：`{% if project_type == 'gui' %}rule-12-pyqt-standards.md{% endif %}`（空）
- 新文件名：`{% if project_type == 'gui' %}rule-12-gui-pyside-standards.md{% endif %}`（419 行）
- 单引号约束：条件文件名用 `'gui'` 而非 `"gui"`（Windows 文件名不允许 `"`）
- 删除旧文件避免 GUI 项目同时生成两个 rule-12

### 4. 项目根 rule-12 不动

项目根 `.trae/rules/rule-12-pyqt-standards.md` 是 coopie 自身使用（library 类型），不随模板分发，本次不修改。

### 5. 版本号 minor bump

新增模板内容（GUI 设计规范）属于功能增加，bump minor：0.6.0 → 0.7.0。

## 验证结果

### 模板渲染验证

- GUI 项目（`project_type=gui`）：生成 `rule-12-gui-pyside-standards.md`，内容含设计令牌与 PySide2/6 规范
- Library 项目（`project_type=library`）：不生成 rule-12 文件

### copier update 验证

- 临时改 `_src_path` 为本地路径 `/home/zhou/coopie`
- `uvx copier update --pretend -A` 输出 `Keeping template version 0.7.0`，无冲突
- coopie 自身为 library 类型，模板 rule-12 变更不影响其工作树

### 测试与门禁

```
uv run ruff check src tests  → All checks passed!
uv run pytest -m "not slow" --cov=coopie --cov-fail-under=95
  → 57 passed, coverage 100.00%
```

## 遗留事项

- 项目根 `.trae/rules/rule-12-pyqt-standards.md` 与 template 版本内容差异较大（前者纯技术规范，后者含设计令牌），后续如需统一须用户授权修改 `.trae/rules/`
- Figma 设计仅覆盖"通用布局与导航"，表单/CRUD/对话框工作流未涉及，后续可扩展
- `.trae/assets/figma.png` 为临时参考文件，未纳入版本控制
