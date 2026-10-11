# Changelog

本项目所有显著变更记录于此。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Changed

- `coopie init` / `coopie update` 默认不再自动信任模板源：模板含 Jinja/任务时 copier 会请求执行确认，非交互场景（CI/脚本）将报错退出；确认模板来源可信后显式加 `--trust` 跳过确认。

### Security

- CLI `--trust` 默认关闭，避免静默执行第三方模板中的任意代码（copier 的 Jinja 非沙箱）。
- 模板生成的 Web 项目 `python -m <包名>` 默认监听 `127.0.0.1` 并关闭 reload，可用 `UVICORN_HOST` / `UVICORN_PORT` / `UVICORN_RELOAD` 环境变量覆盖。
- 模板生成的 CI workflow 声明最小权限 `permissions: contents: read`；Dockerfile 以非 root 用户运行。
