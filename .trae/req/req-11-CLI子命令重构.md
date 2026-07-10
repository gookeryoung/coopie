# 需求：CLI 子命令重构（iter-11）

## 需求清单

[x] 1. cli.py 重构为子命令模式（new/init/update/test），移除旧接口
[x] 2. new 命令：copier copy 到子目录，传 project_name + author 数据
[x] 3. init 命令：copier copy 到当前目录，project_name 从目录名派生，非空目录提示确认
[x] 4. update 命令：copier update + 可选 -A/-T
[x] 5. test 命令：copier update --pretend + 可选 -A/-T
[x] 6. test_cli.py 重写覆盖所有子命令分支
[x] 7. README.md 更新 CLI 用法为子命令
[x] 8. docs/index.rst 同步更新用法
[x] 9. ruff/pyrefly/pytest 全绿，覆盖率 >= 95%（实际 100%）
[x] 10. copier update 验证无冲突（_commit v0.2.2→v0.2.3，无文件冲突）
[] 11. bump + push
