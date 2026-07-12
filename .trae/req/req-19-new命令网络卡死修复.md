# req-19：`new` 命令网络卡死修复

## 背景

`coopie new` 调用 `uvx copier copy https://github.com/gookeryoung/coopie ...`，copier 需 `git clone` GitHub 仓库拉取模板。国内访问 GitHub 不稳定，`git clone` 30 秒仍超时，导致命令卡死。同时 `subprocess.run` 无 timeout，用户只能 Ctrl+C 中断。

附带问题：环境变量 `RUST_LOG=info`（Trae IDE 设置）导致 `uv`（Rust 写的）输出大量 `INFO add_decision` PubGrub 解析日志，干扰诊断、污染输出。

## 需求

- [x] `coopie new`/`coopie init` 支持 `--template <url|path>` 选项指定模板源
- [x] 支持 `COOPIE_TEMPLATE_REPO` 环境变量覆盖默认模板源
- [x] 优先级：`--template` > `COOPIE_TEMPLATE_REPO` > 默认 GitHub 仓库
- [x] `subprocess.run` 加 timeout，超时后给出友好错误提示（建议用户用 `--template` 指定本地/镜像源）
- [x] 调用 `uvx` 时覆盖 `RUST_LOG=warning`，静默 INFO 级 PubGrub 日志
- [x] `update`/`test` 命令同样受益于 timeout 和日志静默
- [x] 测试覆盖：选项解析、优先级、timeout 异常、RUST_LOG 覆盖；覆盖率 ≥ 95%
- [x] 同步更新 README 和 docs/index.rst
- [x] ruff/pyrefly/pytest 全绿
- [x] 实际验证 `coopie new --template <local>` 不卡
- [x] bump 版本、迁移 `_commit`、copier update 无冲突
