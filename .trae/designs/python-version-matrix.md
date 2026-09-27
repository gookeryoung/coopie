# Python 版本矩阵设计

来源：用户反馈"最高版本与最低版本相同时，生成的 CI/CD 等配置出现重复 Python 版本"（req 无对应条目，需求来自对话）。

## 变量契约（copier.yml）

- 询问变量：`min_python_version`（默认 3.8）、`max_python_version`（默认 3.14），choices 均为 3.8–3.14。
- `max_python_version` 携带 validator：`min|replace('.','')|int > max|replace('.','')|int` 时拒绝，错误信息为"最高版本（X）不能低于最低版本（Y）"。必须数值比较，字符串比较 `"3.8" > "3.14"` 会误判。
- 计算变量（`when: false`，不写入 answers 文件，可被后续问题与模板引用）：
  - `target_py`：`py` + min 去点（ruff target-version 用）。
  - `supported_py_versions`：闭区间 [min, max] 的 JSON 数组，是版本区间的**单一事实来源**；`all_versions = ["3.8"..."3.14"]` 字面量仅在此处定义。
  - `tox_envlist`：由 `supported_py_versions` 派生（如 `py310, py311, py312`）。
  - `ci_test_versions`：`[supported_py_versions|first, supported_py_versions|last]|unique|list`，min==max 时自动去重为单元素。

## 生成物行为（min==max 边界）

- `.github/workflows/ci.yml`：矩阵 `python-version: ["3.14"]`（单 job）；job name 为 `Test (Python 3.14)`，多版本时为 `Test (Python X & Y)`（`ci_test_versions|join(' & ')`）。
- `Dockerfile`：`uv python install {{ min }}`，仅当 min != max 时追加第二个版本。
- `tox.ini`：`envlist = py314`（单环境）。
- `pyproject.toml` classifiers：仅一个 `Python :: 3.x` 具体版本行。
- `README.md` 特性行：min==max 时只显示单版本，不显示 `X ~ X`。

## 测试

- `tests/test_template_render.py`：以 `copier.run_copy(vcs_ref="HEAD", defaults=True)` 渲染工作树模板，覆盖 min==max、min<max、min>max（validator 拒绝）三类场景，断言 CI 矩阵/job name、tox envlist、classifiers、Dockerfile、README 的派生结果。
- 渲染必须传 `vcs_ref="HEAD"`：copier 对本地 git 模板默认检出最新 tag，会绕过未提交修改。

## 维护约束

- 新增 Python 版本支持时需同步修改三处：`min_python_version.choices`、`max_python_version.choices`、`supported_py_versions` 内的 `all_versions` 字面量。
