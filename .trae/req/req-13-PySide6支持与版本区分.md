# iter-13 需求：PySide6 支持与版本区分

## 背景

iter-12 新增 `project_type=gui` 仅支持 PySide2（环境标记 `python_version <= "3.10"`）。
但 PySide2 PyPI wheel 仅支持 Python 3.6-3.10，无法在 3.11+ 上安装。
用户希望对于不支持 PySide2 的 Python 版本（3.11+）改用 PySide6，按版本自动区分库依赖。

## 需求

- [ ] 模板 pyproject.toml gui 依赖按 Python 版本区分：
  - `PySide2>=5.15.2.1; python_version <= "3.10"`
  - `PySide6>=6.5.0; python_version >= "3.11"`
- [ ] main.py 模板兼容 PySide2/PySide6（try/except import + exec 兼容写法）
- [ ] copier.yml project_type=gui 的 help 文本更新（反映双绑定）
- [ ] rule-12 规则更新（项目根 + 模板内），同时覆盖 PySide2 和 PySide6：
  - 标题改为 PySide2/PySide6
  - 工具链表增加 PySide6
  - 兼容性段说明按版本自动选择
  - 代码示例用兼容写法
  - 枚举差异（Qt.AlignCenter → Qt.AlignmentFlag.AlignCenter 等）
- [ ] README 同步更新 project_type 说明
- [ ] 验证：ruff + pyrefly + pytest 95% + copier update 无冲突
- [ ] bump 版本（feat → minor 0.3.0 → 0.4.0）+ 迁移 _commit

## 约束

- 不增加 copier 变量让用户手选绑定，按 Python 版本自动区分（单一模板）
- PySide2/PySide6 API 差异：exec_ vs exec、枚举命名空间、import 路径，模板代码用兼容写法
- rule-12 文件名保持 `rule-12-pyqt-standards.md` 不变
- 标准门禁：ruff + pyrefly + pytest 95% 覆盖率

## 验收标准

- gui 依赖声明含 PySide2（py<=3.10）和 PySide6（py>=3.11）两条
- main.py 模板可同时在 PySide2 和 PySide6 环境下运行
- rule-12 覆盖双绑定的最佳实践
- 全套门禁通过 + copier update 无冲突
