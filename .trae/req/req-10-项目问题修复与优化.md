# 需求：项目问题修复与优化（iter-10）

## 需求清单

[x] 1. pyproject.toml classifiers 排序（3.8→3.9→...→3.14）
[x] 2. 移除未使用依赖 typing-extensions（dependencies，项目根+模板）
[x] 3. 移除未使用依赖 httpx（dev，项目根+模板）
[x] 4. 移除未使用依赖 pytest-mock（test，项目根+模板，违反 rule-11）
[x] 5. .pre-commit-config.yaml 添加 ruff-format hook（项目根+模板）
[x] 6. .pre-commit-config.yaml ruff 版本升级 v0.15.4 → v0.15.8（项目根+模板）
[x] 7. README.md 修正 make bump 用法（PART=patch → 默认 patch）
[x] 8. docs/index.rst 修正 make bump 用法
[x] 9. 更新 uv.lock 同步依赖变更
[x] 10. make check 全绿，覆盖率不下降（100%）
[x] 11. copier update 验证无冲突（Keeping template version 0.2.2）
[] 12. iter-10 文档与 bump
