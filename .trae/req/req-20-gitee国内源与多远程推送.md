# iter-20 需求：Gitee 国内源与多远程推送

## 背景

coopie 默认模板源是 GitHub，国内访问不稳定导致 `coopie new` 卡死（iter-19 已加超时保护但未改默认源）。项目已增加 Gitee 国内远程 `https://gitee.com/gooker_young/coopie`，需完善相关逻辑优先从国内源拉取。

## 需求清单

- [ ] CLI 默认模板源改为 Gitee（`https://gitee.com/gooker_young/coopie`），GitHub 通过 `--template`/`COOPIE_TEMPLATE_REPO` 作为备选
- [ ] Makefile `push` 目标改为遍历 `git remote` 推送所有远程，不硬编码远程名（模板需兼容用户自定义远程名场景）
- [ ] 同步修改 `template/Makefile`（用户项目模板）的 `push` 目标
- [ ] `.copier-answers.yml` 的 `_src_path` 改为 Gitee 地址
- [ ] 更新 `tests/test_cli.py` 中 GitHub 默认源断言为 Gitee
- [ ] 更新 `README.md` 与 `docs/index.rst` 中默认源说明
- [ ] Gitee 仓库需设为公开（HTTPS 匿名 clone 必须，用户已确认）

## 约束

- **不硬编码远程名**：模板中 push 遍历 `git remote`，适用于远程名不叫 "gitee" 的用户场景
- 兼容性：保留 `--template`/`COOPIE_TEMPLATE_REPO` 覆盖默认源的能力（iter-19 已实现）
- 验收：`make check` 全套门禁通过；`coopie new` 默认源能匿名 clone（Gitee 设为公开后）

## 不在范围

- 不改 iter-19 的超时/RUST_LOG 处理逻辑（已稳定）
- 不增加新依赖
