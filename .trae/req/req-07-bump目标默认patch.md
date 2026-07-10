# iter-07 需求：bump 目标默认 patch

## 需求来源

用户反馈 `make bump` 报错"用法: make bump PART=<patch|minor|major>"不好用，要求：
- `make bump` 默认 patch
- `make bump minor` 支持 minor
- `make bump major` 支持 major

## 需求清单

- [x] 需求确认：需求清晰无歧义，直接执行
- [x] 修改项目根 Makefile bump 目标：默认 patch，支持位置参数
- [x] 修改模板 Makefile bump 目标：同步
- [x] 验证：make -n bump / make -n bump minor 命令正确
- [x] bump 版本，迁移 _commit，创建 iter-07 文档
