# 测试基础设施设计

来源：CLI 安全化与渲染测试提速迭代（req 无对应条目，需求来自对话）。

## 渲染测试（tests/test_template_render.py）

- [x] 渲染源为「快照」：session fixture `template_snapshot` 把 `copier.yml` + `template/` 复制到临时目录，copier 走本地目录渲染路径。
- [x] 不再使用 `vcs_ref="HEAD"` 直接渲染仓库根：该方式每次都走 git clone（实测 ~14.8s/次），快照后为 ~4.9s/次；两者产物一致，差异仅在 `.copier-answers.yml` 的 `_src_path/_commit`，用例不依赖这两个字段。
- [x] session fixture `render` 按 `data` 的 JSON 序列化键缓存渲染产物：相同参数的用例复用同一目录，用例必须只读产物、不得修改文件。
- [x] validator 拒绝场景（min>max）通过 `pytest.raises` 断言，不进入缓存。

## 覆盖率并发约定

- [x] `.coveragerc` 的 `concurrency = multiprocessing`：测试经 pytest-xdist（Makefile `-n 8`）多进程并行，各 worker 覆盖率需按 multiprocessing 合并；设为 `thread` 会导致覆盖率无法正确合并（实测从 96% 掉到 74%）。
- [x] 若未来测试放弃 xdist 改回单进程，此配置可保留（multiprocessing 合并对单进程同样正确）。

## copier VCS patch 测试约定

- [x] `src/coopie/cli.py` 的 copier VCS patch 为按需执行（`_ensure_copier_vcs_patched`），测试通过 autouse fixture `_patched_copier_vcs` 显式触发，保证断言环境一致。
- [x] patch 必须幂等：`GIT_PREFIX` 按 tuple 去重、`REPLACEMENTS` 按 (pattern, repl) 去重，重复调用不膨胀。
