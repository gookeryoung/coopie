# iter-12 需求：项目类型选择与编码规范

## 背景

当前模板仅通过 `use_cli` 布尔开关控制是否生成 `[project.scripts]` 入口，无"项目类型"概念。
用户希望增加项目类型选择（如 gui: PySide2、web: FastAPI 等），根据类型配置对应依赖与入口模板，
并制定 PySide2 编码规范（rule-12-pyqt-standards.md）。

## 需求

- [x] 新增 copier 变量 `project_type`（library/cli/gui/web），默认 library
- [x] 根据 project_type 配置对应依赖：
  - library/cli: 无额外依赖
  - gui: PySide2（环境标记 `python_version <= "3.10"`，因 PyPI wheel 仅支持 3.6-3.10）
  - web: fastapi + uvicorn[standard]
- [x] 根据 project_type 生成入口模板文件：
  - cli: src/{package_name}/cli.py（与 use_cli 对齐）
  - gui: src/{package_name}/main.py（PySide2 QApplication 入口）
  - web: src/{package_name}/app.py（FastAPI app 实例）
- [x] CLI（coopie new/init）增加 `--type` 选项传递 project_type
- [x] 填充 `.trae/rules/rule-12-pyqt-standards.md`（PySide2 编码规范，最佳实践）
- [x] 模板内 rule-12 条件渲染（project_type=gui 时生成到生成项目）
- [x] `.copier-answers.yml` 添加 `project_type: library`（coopie 自身 use_cli=true，避免 cli.py 模板冲突）
- [x] README 同步更新 project_type 说明（项目根 + 模板）
- [x] 测试覆盖（CLI --type 选项，覆盖率 100%）
- [x] 验证：ruff + pyrefly + pytest 100% + copier update 无冲突
- [x] bump 版本（feat → minor 0.2.4 → 0.3.0）+ 迁移 _commit v0.2.3 → v0.3.0

## 约束

- 保留 `use_cli` 向后兼容，`project_type=cli` 等价 `use_cli=true`（[project.scripts] 条件改为 `use_cli or project_type == "cli"`）
- PySide2 PyPI 官方 wheel 最新 5.15.2.1，仅支持 Python 3.6-3.10，依赖加环境标记
- rule-12 规范说明 PySide2 版本限制，建议 gui 项目 max_python_version 设为 3.10
- 标准门禁：ruff + pyrefly + pytest 95% 覆盖率

## 验收标准

- copier.yml 含 project_type 变量（4 选项）
- 模板正确条件化依赖与入口文件
- rule-12 规范完整（PySide2 最佳实践，覆盖信号槽/布局/资源/线程/测试/打包等）
- 全套门禁通过
- copier update 无冲突
