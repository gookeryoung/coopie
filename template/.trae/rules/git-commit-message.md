---
name: "git-commit-message"
alwaysApply: true
---

## 提交前门禁

**每次 `git commit` 前必须本地通过 `make check`，无例外。** 这是对 CI/CD 的最低尊重，禁止"先提交再说，CI 跑了再修"。

- **强制门禁命令**：`make check`（= `lint` + `typecheck` + `cov`，定义见 `Makefile`）。三项必须全绿方可 `git add` / `git commit` / `git push`。
- **失败即阻断**：lint / typecheck / cov 任一项失败时禁止任何提交动作；必须定位根因修复后重跑 `make check`，不放宽断言、不绕过覆盖率检查、不使用 `--no-verify` 等方式跳过本地钩子。
- **CI 失败必复现**：CI/CD lint 失败时，禁止仅凭"本地通过"假设跳过排查；必须在本地复现 CI 同款命令确认通过后再提交修复。CI 等价命令（见 `.github/workflows/ci.yml`）：
  - `uv run ruff check src tests`
  - `uv run ruff format --check src tests`
  - `uv run pyrefly check`
  - `uv run pytest -m "not slow" --cov=fspack --cov-fail-under=95`
- **门禁子命令清单**：
  - `make lint`：`uv run ruff check .` + `uv run ruff format --check .`
  - `make typecheck`：`uv run pyrefly check`
  - `make cov`：`uv run pytest -m "not slow" --cov=fspack --cov-fail-under=95`
  - `make check`：上述三项全跑（提交前用此命令）
- **规则变更亦适用**：修改 `.trae/rules/` 下规则文件后，同样须跑 `make check` 确认未破坏既有门禁。
- **执行记录**：收尾总结中须注明"已本地通过 `make check`"字样，便于追溯。

## 提交信息格式

- 使用中文编写，简洁明了，不超过一段落。
- 必须包含变更类型前缀，采用 `类型: 描述` 格式。
- 变更类型包括：
  - `feat`：新增功能
  - `fix`：修复缺陷
  - `refactor`：重构（不改变外部行为）
  - `docs`：文档更新
  - `style`：格式调整（不影响代码逻辑）
  - `test`：测试相关
  - `chore`：构建、依赖、工具链等杂项
  - `perf`：性能优化
  - `build`：构建系统或外部依赖变更
  - `ci`：CI 配置变更
- 描述部分说明"做了什么"，必要时补充"为什么"。
- 单条提交仅包含一个逻辑变更，避免混合多个无关改动。
- 禁止仅写"update"、"fix bug"等模糊描述；禁止中英文混用描述。
- 涉及 issue/任务编号时，置于段末括号内，如 `(refs #123)`。

## 正面示例

- `feat: 新增侧边栏折叠功能，支持快捷键 Ctrl+B 切换`
- `fix: 修复 QThread 退出时未等待导致 worker 泄漏的问题 (refs #42)`
- `refactor: 将样式令牌加载逻辑抽取到 theme.py，消除 main.py 中的重复代码`

## 反面示例

- `update`：缺少类型前缀，描述模糊，无法判断变更性质
- `修复了一些问题`：缺少类型前缀，未说明修复了什么问题
- `feat: add sidebar collapse feature and fix thread leak and update docs`：单条提交混合多个无关变更，且中英文混用

## 命令行传递

- **PowerShell 不支持 heredoc**：`cat <<'EOF' ... EOF`、`<<EOF` 等 heredoc 语法在 PowerShell 中无效，多行提交信息须用多个 `-m` 参数传递，每个 `-m` 作为一段落，段落间自动以空行分隔。
- 多段萾示例（PowerShell 兼容）：
  ```powershell
  git commit -m "feat: 新增侧边栏折叠功能" -m "支持快捷键 Ctrl+B 切换，状态持久化到 settings.json (refs #42)"
  ```
- 禁止在 PowerShell 中使用以下 heredoc 形式（会原样作为字面量传入，导致提交信息错乱）：
  ```powershell
  git commit -m "$(cat <<'EOF'
  feat: 新增侧边栏折叠功能

  支持快捷键 Ctrl+B 切换
  EOF
  )"
  ```
- 单段落提交可直接用单个 `-m`；仅当需要标题+正文结构时才用多个 `-m`。
- bash/zsh 环境下 heredoc 可正常使用，本约束仅针对 PowerShell。
