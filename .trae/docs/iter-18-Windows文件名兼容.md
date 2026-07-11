# iter-18：Windows 文件名兼容

## 迭代目标

修复 Windows 上 `git pull` 报 `invalid path` 错误，根因为 copier 模板的 Jinja2 条件文件名中使用双引号 `"`，而 Windows 文件系统不允许该字符。

## 改动文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `template/.trae/rules/{% if project_type == 'gui' %}rule-12-pyqt-standards.md{% endif %}` | 重命名 | `"` → `'` |
| `template/src/{{ package_name }}/{% if project_type == 'cli' %}cli.py{% endif %}` | 重命名 | `"` → `'` |
| `template/src/{{ package_name }}/{% if project_type == 'gui' %}main.py{% endif %}` | 重命名 | `"` → `'` |
| `template/src/{{ package_name }}/{% if project_type == 'web' %}app.py{% endif %}` | 重命名 | `"` → `'` |
| `.trae/skills/skill-14-精简README用户导向.md` | 新建 | 归档自 iter-14/req-14（阈值触发） |

## 关键决策与依据

1. **仅改文件名，不改文件内容**：Windows 文件系统非法字符 `\ / : * ? " < > |` 仅影响文件名，文件内容中的 `"` 合法无需改动。模板内 `.toml`/`.md`/`.py` 文件内容中的 `project_type == "gui"` 等表达式保持不变。

2. **单引号与双引号在 Jinja2 中语义等价**：Jinja2 模板引擎对字符串字面量不区分单双引号，`{% if project_type == 'gui' %}` 与 `{% if project_type == "gui" %}` 完全等价。单引号 `'` 在 Windows 文件名中合法。

3. **验证方式**：用非 git 副本（`rsync --exclude='.git'`）渲染三种 project_type（gui/cli/web），确认条件文件正确生成（gui→main.py+rule-12、cli→cli.py、web→app.py）。

## 验证结果

- ruff check / ruff format --check / pyrefly check：全绿
- pytest：42 passed, 100% coverage
- copier copy 渲染验证（非 git 副本）：
  - gui：生成 main.py + rule-12-pyqt-standards.md ✓
  - cli：生成 cli.py ✓
  - web：生成 app.py ✓

## 遗留事项

无。Windows 文件名兼容问题已解决，用户在 Windows 上 `git pull` 不再报 invalid path。
