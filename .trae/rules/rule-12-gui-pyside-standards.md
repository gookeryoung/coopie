# PySide2/PySide6 (Qt5/Qt6) GUI 开发规范

适用于 `project_type=gui` 的生成项目。在 `rule-11-python-standards.md` 基础上补充 Qt 桌面应用的设计规范与技术约束。

模板按 Python 版本自动区分绑定：`PySide2`（Python ≤ 3.10）/ `PySide6`（Python ≥ 3.11），代码须双兼容。

## 设计系统（Design Tokens）

所有 QSS 与代码须引用令牌常量，禁止散落硬编码颜色/尺寸。令牌集中定义在 `src/{{ package_name }}/theme.py`，QSS 通过 `string.Template` 占位符引用（见「样式」段）。

### 色彩系统

| 令牌 | 色值 | 用途 |
|------|------|------|
| `COLOR_PRIMARY` | `#0887A0` | 主色：头部条、侧边栏背景、主操作按钮、选中态 |
| `COLOR_PRIMARY_DARK` | `#00829E` | 主色按下态、分割线 |
| `COLOR_ACCENT` | `#87C6BB` | 强调色：成功状态、辅助高亮 |
| `COLOR_TEXT_ON_PRIMARY` | `#FFFFFF` | 主色背景上的文字/图标 |
| `COLOR_TEXT_PRIMARY` | `#2C3E50` | 主文字（深色，用于白底内容区） |
| `COLOR_TEXT_SECONDARY` | `#518394` | 次级文字、说明、禁用态 |
| `COLOR_BG_APP` | `#FFFFFF` | 应用底色、内容区背景 |
| `COLOR_BG_MUTED` | `#E5EDE0` | 浅底：卡片间隙、分组背景 |
| `COLOR_BORDER` | `#D1DDE2` | 边框、分割线 |
| `COLOR_DANGER` | `#E74C3C` | 错误/危险操作 |
| `COLOR_WARNING` | `#F39C12` | 警告 |
| `COLOR_SUCCESS` | `#27AE60` | 成功 |

### 排版

| 令牌 | 字号 | 字重 | 用途 |
|------|------|------|------|
| `FONT_TITLE` | 18px | Bold | 窗口标题、页面标题 |
| `FONT_HEADING` | 15px | Bold | 区块标题、分组标题 |
| `FONT_BODY` | 13px | Regular | 正文、表单标签 |
| `FONT_CAPTION` | 11px | Regular | 说明文字、状态栏、表头 |

字体族：`"PingFang SC", "Microsoft YaHei", "Segoe UI", "Helvetica Neue", Arial, sans-serif`（macOS/Windows/Linux 顺序回退）。

### 间距尺度

8px 基准网格，所有间距须为 8 的倍数：

| 令牌 | 值 | 用途 |
|------|-----|------|
| `SPACING_XS` | 4px | 图标与文字间隙 |
| `SPACING_SM` | 8px | 控件内边距、紧凑间隙 |
| `SPACING_MD` | 16px | 控件间间隙、表单字段间距 |
| `SPACING_LG` | 24px | 区块内边距 |
| `SPACING_XL` | 32px | 区块间间隙 |

### 圆角与尺寸

| 令牌 | 值 | 用途 |
|------|-----|------|
| `RADIUS_SM` | 4px | 按钮、输入框 |
| `RADIUS_MD` | 6px | 卡片、面板 |
| `CONTROL_HEIGHT` | 32px | 按钮/输入框标准高度 |
| `CONTROL_HEIGHT_SM` | 26px | 紧凑控件 |
| `SIDEBAR_WIDTH` | 220px | 侧边栏宽度 |
| `HEADER_HEIGHT` | 40px | 头部条高度 |
| `TOOLBAR_HEIGHT` | 44px | 工具栏高度 |
| `STATUSBAR_HEIGHT` | 28px | 状态栏高度 |

## 布局规范

### 主窗口结构

「头部 + 侧边栏 + 内容区 + 状态栏」四区结构，用 `QVBoxLayout`（外层）嵌套 `QHBoxLayout`（中区），**禁用绝对定位** `setGeometry`：

```
┌──────────────────────────────────────────────────────────┐
│ HeaderBar  (COLOR_PRIMARY, 高 HEADER_HEIGHT)             │
├──────────────────────────────────────────────────────────┤
│            │                                             │
│  Sidebar   │           Content Area                      │
│ (COLOR_    │  (COLOR_BG_APP, 可滚动)                     │
│  PRIMARY,  │                                             │
│  宽 SIDEBAR│                                             │
│  _WIDTH)   │                                             │
│            │                                             │
├────────────┴─────────────────────────────────────────────┤
│ StatusBar  (COLOR_BG_MUTED, 高 STATUSBAR_HEIGHT)         │
└──────────────────────────────────────────────────────────┘
```

要点：
- 外层顺序：header → (sidebar + content 的 `QHBoxLayout`，sidebar 与 content 之间用 `QSplitter` 可拖拽) → statusbar
- Content 用 `QStackedWidget` 配合侧边栏切换；侧边栏可折叠（`setSizes([0, width])`）
- 所有 Layout `setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)`
- 最小 `800×600`，默认 `1280×800`；宽 < 1000px 时侧边栏折叠为图标条（56px）
- 内容区卡片用 `QGridLayout` 自适应列数（`resizeEvent` 中重算）

### 布局通用约束

- 优先 `QVBoxLayout`/`QHBoxLayout`/`QGridLayout`/`QFormLayout`，**禁用** `setGeometry`（除固定尺寸弹窗）
- 嵌套用 `addLayout()`，部件 `addWidget()`；伸缩比 `addWidget(widget, stretch=N)` 或 `addStretch()`
- 窗口尺寸策略 `setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)`
- 响应式用 `QSplitter` 而非固定比例

## 导航模式

### Header 区
- 左右两侧，中间用 Spacer 分隔
- 左侧 Tab 切换业务功能（按业务流程从左至右布局），切换时 Sidebar 与 Content 同步变化
- 右侧通用按钮（`设置`/`帮助`/`关于` 等），点击进入独立对话框

### 侧边栏（一级导航，首选）
`QListWidget` 或自定义 `QWidget`：背景 `COLOR_PRIMARY`、文字 `COLOR_TEXT_ON_PRIMARY`；每项 40px，图标 20×20 + `FONT_BODY`；选中态 `COLOR_PRIMARY_DARK` + 左侧 3px `COLOR_ACCENT` 竖条；`currentRowChanged` → `stack.setCurrentIndex`。

### 选项卡与面包屑
- 次级 `QTabWidget`：Tab 高 36px、`FONT_BODY`，选中 Tab 底部 2px `COLOR_PRIMARY` 下划线，内容区 `COLOR_BORDER` + `RADIUS_MD`
- 面包屑用 `QLabel` + `>` 分隔：`FONT_CAPTION`/`COLOR_TEXT_SECONDARY`，当前页 `COLOR_TEXT_PRIMARY` + Bold；点击上级触发 `navigation_requested` 信号

## 兼容性（关键约束）

### 版本与依赖

- **PySide2 仅支持 Python 3.6-3.10**：PyPI 最新 wheel `5.15.2.1`，无 3.11+ wheel。
- **PySide6 支持 Python 3.8+**：3.11+ 环境必选，PySide2 不可用。
- 依赖声明（模板自动生成，勿手改）：

```toml
dependencies = [
    "PySide2>=5.15.2.1; python_version <= '3.10'",
    "PySide6>=6.5.0; python_version >= '3.11'",
]
```

pip/uv 按 Python 版本只安装其一。

### API 差异速查

| 场景 | PySide2 (Qt5) | PySide6 (Qt6) |
|------|---------------|---------------|
| 事件循环 | `app.exec_()` | `app.exec()`（`exec_` 已弃用） |
| 对齐枚举 | `Qt.AlignCenter` | `Qt.AlignmentFlag.AlignCenter` |
| 方向枚举 | `Qt.Horizontal` | `Qt.Orientation.Horizontal` |
| 键盘修饰 | `Qt.ControlModifier` | `Qt.KeyboardModifier.ControlModifier` |
| 窗口标志 | `Qt.Window` | `Qt.WindowType.Window` |
| 鼠标按钮 | `Qt.LeftButton` | `Qt.MouseButton.LeftButton` |
| itemDataRole | `Qt.DisplayRole` | `Qt.ItemDataRole.DisplayRole` |
| 拖放动作 | `Qt.CopyAction` | `Qt.DropAction.CopyAction` |

### 双兼容编码模式

import 用 try/except；事件循环兼容写法：

```python
try:
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import Qt, Signal, Slot
except ImportError:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt, Signal, Slot

run = app.exec if hasattr(app, "exec") else app.exec_
return run()
```

枚举：跨版本运行用短名 `Qt.AlignCenter`（两代均支持，PySide6 仅发 DeprecationWarning）；仅 PySide6 则用全路径。

## 模块与入口

- 入口 `src/{{ package_name }}/main.py`：`QApplication(sys.argv)` → 构建主窗口 → 事件循环（见上兼容写法）
- `main()` 加 `# pragma: no cover`（事件循环阻塞），拆出 `create_main_window()` 等可测函数
- 业务逻辑放纯 Python 模块（不 import PySide）便于单测；GUI 层只做信号槽连接与状态展示
- 惰性导入重型部件（QWebEngineView 等）以加快启动

## 信号槽

- 新式信号槽，**禁用** `SIGNAL/SLOT` 字符串语法
- 信号定义为类属性：`value_changed = Signal(int)`
- 连接用方法引用：`button.clicked.connect(self._on_clicked)`；避免重复连接（多次 connect 多次触发）
- disconnect 用 `try/except RuntimeError`（连接已断开会抛错）
- 跨线程 worker → UI 用 `Qt.QueuedConnection`

## 资源系统

- `.qrc` 管理图标/样式表，编译为 `_rc.py`（`pyside2-rcc`/`pyside6-rcc`），引用用 `:/` 前缀：`QIcon(":/icons/app.png")`
- `.ui` 用 `pyside2-uic`/`pyside6-uic` 编译为 `.py`（比运行时 `QUiLoader` 快，推荐）
- 资源变更后须重新编译 `_rc.py` 并纳入版本控制（构建环境可能缺 rcc 工具链）
- 大文件（视频/字体）用磁盘路径加载，不进 `.qrc`

## 事件循环

- `QApplication` 全局单例，传入 `sys.argv`（解析 `-style` 等命令行参数）
- 长任务**禁止主线程执行**（冻结 UI），用 `QThread` 或 `QThreadPool + QRunnable`
- 定时器 `QTimer.singleShot(ms, callback)` 或 `QTimer(timeout=cb).start(ms)`，不用 `time.sleep`
- 事件过滤器 `installEventFilter` + 重写 `eventFilter()`，优先于子类化

## QThread 线程

- **Worker 模式（推荐）**：QObject 子类化 + `moveToThread(thread)`，信号槽跨线程通信
- **子类化模式**：重写 `run()`，`start()` 启动，`finished` 通知结束
- **禁止非主线程操作 GUI 部件**（QLabel.setText 等），只通过信号回主线程
- 退出：`thread.quit() + thread.wait()` 或 `QThread.requestInterruption() + isInterruptionRequested()`
- 清理：`finished` → `deleteLater`，避免线程对象泄漏
- 互斥锁 `QMutex + QMutexLocker`（RAII）或 `threading.Lock`

## 样式（QSS）

QSS 不支持变量，用 Python `string.Template` 渲染。`theme.py` 定义令牌，`style.qss` 用占位符，加载时替换：

```python
# theme.py
COLOR_PRIMARY = "#0887A0"
COLOR_TEXT_ON_PRIMARY = "#FFFFFF"

QSS_TOKENS = {"COLOR_PRIMARY": COLOR_PRIMARY, "COLOR_TEXT_ON_PRIMARY": COLOR_TEXT_ON_PRIMARY}
```

```css
/* style.qss */
QListWidget#sidebar {
    background-color: ${COLOR_PRIMARY};
    color: ${COLOR_TEXT_ON_PRIMARY};
    border: none;
    font-size: 13px;
}
QListWidget#sidebar::item:selected {
    background-color: ${COLOR_PRIMARY_DARK};
    border-left: 3px solid ${COLOR_ACCENT};
}
```

```python
# main.py 加载 QSS
from pathlib import Path
from string import Template
from {{ package_name }} import theme

def load_stylesheet() -> str:
    """加载 QSS 并替换设计令牌占位符."""
    qss = Path(__file__).parent / "style.qss"
    return Template(qss.read_text("utf-8")).substitute(theme.QSS_TOKENS)

app.setStyleSheet(load_stylesheet())
```

- 样式表用 `.qss` 文件管理，**避免硬编码**内联样式
- 选择器粒度到部件类型 + objectName：`QPushButton#okButton { ... }`，不用全局限定
- 主题切换通过替换 `.qss` 重新加载，不在代码中分支样式
- macOS 默认风格与 QSS 冲突时用 `app.setStyle("Fusion")` 统一

## 测试（pytest-qt）

- `qapp` fixture 提供单例 `QApplication`（自动管理生命周期，兼容 PySide2/PySide6）
- `qtbot` 模拟交互：`mouseClick`/`keyClicks`/`addWidget`
- 等待信号 `qtbot.waitSignal(widget.signal, timeout=1000)`，断言 `blocker.args`
- GUI 测试加 `@pytest.mark.gui`（或 `slow`），CI 默认 `-m "not slow"` 跳过
- 无头环境设 `QT_QPA_PLATFORM=offscreen`（CI 用 xvfb 或 offscreen 平台插件）
