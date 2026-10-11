# CLI trust 安全契约设计

来源：用户反馈"copier 的 Jinja 非沙箱可执行任意代码，CLI 不应自动信任模板源"（req 无对应条目，需求来自对话）。

## trust 语义

- [x] `coopie init` / `coopie update` 均提供 `--trust` 选项（默认 `False`）：跳过 copier 对「模板含 Jinja/任务」的执行安全确认。
- [x] 默认**不**自动 trust：copier 9.17+ 仅在显式 `--trust` 时构造 `Settings(trust=[<模板源>])` 传入 `run_copy`/`run_recopy`；老版本（无 `Settings`）不传 `settings` 参数。
- [x] `init` 的 trust 对象是 `--url` 规范化后的 URL；`update` 的 trust 对象是 answers 文件里规范化后的 `_src_path`。
- [x] 未加 `--trust` 时 CLI 打印 dim 提示（`_warn_if_untrusted`）：告知模板含任务时 copier 会请求确认、可加 `--trust` 跳过。

## 错误映射

- [x] `run_copy` / `run_recopy` 抛出的 `copier.errors.UserMessageError` 统一映射为红色错误输出 + 退出码 1（`_user_message_error_type` 兼容无该异常的老版本 copier，用永不匹配的占位类型兜底）。
- [x] 非交互场景（CI/脚本）未 trust 且模板含任务时，copier 抛 `UserMessageError`，CLI 以退出码 1 结束并给出明确错误信息。

## 行为变更说明（相对旧版）

- 旧版 `init`/`update` 自动把模板源放进 `Settings.trust`（静默信任）；新版必须显式 `--trust`。影响：旧脚本/CI 中含任务的模板在非交互场景会因确认失败报错退出，需显式加 `--trust`。
- 已在 README、docs/usage.rst、CHANGELOG 中说明。
