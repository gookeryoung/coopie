# req-31：添加 .gitattributes 强制 LF 行尾

## 背景

iter-30 P4 遗留事项：项目无 .gitattributes 文件，工作区 CRLF/LF 混合（48 个文件工作区 CRLF）。属 git config 变更（rule-01 暂停条件第 2 条），需用户确认后执行。用户已确认"可以执行"。

## 需求

- [x] 添加根目录 .gitattributes，强制文本文件 LF 行尾，Windows 脚本 CRLF，二进制文件 binary
- [x] 添加 template/.gitattributes（随模板分发，内容与根目录一致）
- [x] 执行 git add --renormalize 验证仓库行尾状态
- [x] 验证 make render 确保模板渲染正常
