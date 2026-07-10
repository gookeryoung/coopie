# iter-08 需求：移除项目自身 Dockerfile 支持

## 需求来源

coopie 是发布到 PyPI 的 CLI 工具/模板，自身不需要容器化部署。保留 Dockerfile 增加维护负担。template 保留 `use_docker` 选项供生成项目按需启用。

## 需求清单

- [x] 需求确认：用户确认执行
- [ ] `.copier-answers.yml` 设 `use_docker: false`
- [ ] 删除项目根 Dockerfile 和 .dockerignore
- [ ] 更新 README（特性段移除容器化、文件清单移除 Dockerfile/.dockerignore）
- [ ] 验证 make check 全绿
- [ ] 提交并创建 iter-08 文档
