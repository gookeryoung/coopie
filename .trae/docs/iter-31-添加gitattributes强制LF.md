# iter-31：添加 .gitattributes 强制 LF 行尾

## 需求清单

- [x] P4（iter-30 遗留）：项目无 .gitattributes 文件，工作区 CRLF/LF 混合（48 个文件工作区 CRLF），添加 .gitattributes 强制 LF 统一（用户已确认执行）

## 迭代目标

按用户确认执行 iter-30 遗留事项 P4，添加 .gitattributes 文件强制 LF 行尾规范化，消除跨平台协作的行尾差异问题。

## 改动文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `.gitattributes` | 新建 | 根目录 .gitattributes（coopie 自身用），强制文本文件 LF，Windows 脚本 CRLF，二进制文件 binary |
| `template/.gitattributes` | 新建 | 模板版本（随项目分发），内容与根目录一致 |
| `.trae/docs/iter-26-python项目结构骨架SKILL.md` | 删除 | rule-02 迭代记录数 ≤ 5 约束，清理最旧 |
| `.trae/docs/iter-31-添加gitattributes强制LF.md` | 新建 | 本轮迭代记录 |
| `.trae/req/done/req-31-添加gitattributes强制LF.md` | 新建 | 本轮需求记录（直接归档） |

## 关键决策与依据

1. **.gitattributes 内容设计**：
   - `* text=auto eol=lf`：默认所有文本文件使用 LF 行尾（跨平台一致）
   - `*.bat`/`*.cmd`/`*.ps1 text eol=crlf`：Windows 脚本使用 CRLF（PowerShell/批处理在 Windows 上需要 CRLF）
   - 二进制文件（图片/压缩包/编译产物等）标记为 `binary`，不做行尾转换

2. **根目录与 template 双份同步**：
   - 根目录 `.gitattributes` 服务于 coopie 仓库自身的行尾规范化
   - `template/.gitattributes` 作为模板源，随 copier copy 分发给用户项目，确保生成的项目也具备行尾规范化能力
   - 两份内容完全一致（.gitattributes 无项目特定变量，无需 Jinja 渲染）

3. **git add --renormalize 无变更**：
   - 执行 `git add --renormalize .` 后 `git status` 无变更，说明仓库存储已经是 LF（i/lf），只是 Windows 检出时工作区为 CRLF（w/crlf）
   - .gitattributes 的作用是确保未来提交时自动规范化为 LF，避免新文件引入 CRLF

4. **iter-26 清理**：新增 iter-31 后，`.trae/docs/` 下 iter 记录达 6 个，超过 rule-02 "保留最新 5 条记录"阈值。按 rule-02 "从最旧记录开始清理"规定，删除 iter-26（最旧）。iter-26 内容为"python 项目结构骨架 SKILL"，已完成且代码已体现，删除迭代记录不影响代码。

## 代码实现情况

### .gitattributes 内容

```gitattributes
# Git 行尾规范化
# 默认所有文本文件使用 LF 行尾（跨平台一致）
* text=auto eol=lf

# Windows 脚本使用 CRLF
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# 二进制文件（不做行尾转换）
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.icns binary
*.pdf binary
*.zip binary
*.gz binary
*.tar binary
*.tgz binary
*.whl binary
*.egg binary
*.pyc binary
*.pyo binary
*.so binary
*.dll binary
*.dylib binary
*.qrc binary
*.qss binary
```

### git add --renormalize 验证

```bash
$ git add --renormalize .
$ git status
# 无变更，说明仓库存储已经是 LF
```

### iter-26 清理

使用 `git rm` 删除 `.trae/docs/iter-26-python项目结构骨架SKILL.md`。清理后 `.trae/docs/` 下保留 iter-27~iter-31 共 5 个迭代记录，符合 rule-02 约束。

## 整合优化情况

- **跨平台行尾一致性**：.gitattributes 强制 LF，未来所有平台（Windows/Linux/macOS）提交的文件都将规范化为 LF，消除 CRLF/LF 混合问题
- **模板分发**：template/.gitattributes 确保生成的用户项目也具备行尾规范化能力，避免用户项目出现同样的 CRLF/LF 问题
- **iter 记录数合规**：清理 iter-26 后，迭代记录数从 6 降至 5，符合 rule-02 "保留最新 5 条"约束

## 测试验证结果

- **make render**：4 种 project_type（library/cli/gui/web）全部渲染成功，生成的项目均包含 `.gitattributes` 文件 ✓
- **git add --renormalize**：无变更，确认仓库存储已是 LF ✓
- **iter 记录数验证**：`.trae/docs/` 下 5 个迭代记录（iter-27~31）✓

## 遗留事项

无。iter-30 P4 遗留事项已处理完毕。

## 下一轮计划

无明确下一轮计划。本轮完成 .gitattributes 添加与 iter-26 清理，项目行尾规范化体系建立完成。
