# iter-18 需求：Windows 文件名兼容

## 背景

用户在 Windows（MINGW64）执行 `git pull` 报错：
```
error: invalid path 'template/.trae/rules/{% if project_type == "gui" %}rule-12-pyqt-standards.md{% endif %}'
error: invalid path 'template/src/{{ package_name }}/{% if project_type == "cli" %}cli.py{% endif %}'
error: invalid path 'template/src/{{ package_name }}/{% if project_type == "gui" %}main.py{% endif %}'
error: invalid path 'template/src/{{ package_name }}/{% if project_type == "web" %}app.py{% endif %}'
```

根因：copier 模板的 Jinja2 条件文件名中使用双引号 `"`（如 `{% if project_type == "gui" %}`），而 Windows 文件系统不允许 `"` 出现在文件名中（非法字符：`\ / : * ? " < > |`）。

## 需求

- [x] 将 4 个模板条件文件名中的双引号 `"` 改为单引号 `'`（Jinja2 两者均支持）
- [x] 验证 copier 渲染条件文件名仍正常工作（gui/cli/web 三种类型）
- [x] make check 全绿
- [x] bump 版本 + push

## 约束

- 仅改文件名，不改文件内容（文件内容中的 `"` 合法，无需改）
- 单引号在 Jinja2 中与双引号语义完全等价
- 标准门禁：ruff + pyrefly + pytest 95% 覆盖率

## 验收标准

- 4 个模板文件名不再含 `"`
- copier copy 三种 project_type 均正确渲染条件文件
- Windows 上 `git pull` 不再报 invalid path
