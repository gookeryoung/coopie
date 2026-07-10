# iter-09 需求：修复 GitHub Actions Node.js 20 弃用警告

## 需求来源

GitHub Actions 运行时报告 `astral-sh/setup-uv@v6` 使用已弃用的 Node.js 20。
官方博客 2025-09-19 宣布弃用 Node.js 20，Actions 需升级到 Node.js 24。
官方文档推荐 `astral-sh/setup-uv@v8.1.0`（Node.js 24）。

## 需求清单

- [x] 需求确认：用户报告 Build & Publish 报弃用警告，需求清晰
- [ ] 升级项目根 .github/workflows/ci.yml 和 release.yml 的 setup-uv@v6 → @v8
- [ ] 升级模板 .github/workflows/ci.yml 和 release.yml 的 setup-uv@v6 → @v8
- [ ] 检查其他 actions（checkout/setup-python）版本是否需升级
- [ ] 提交、bump、迁移 _commit，创建 iter-09 文档
