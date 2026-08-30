# Makefile - coopie 快捷命令
# 运行 `make help` 查看所有可用命令

.PHONY: help sync build b clean c lint typecheck typecheck-ci check test cov doc render bump patch minor major push

help: ## 显示帮助信息
	@uv run python -c "import re,sys;ms=[(m.group(1),m.group(2).strip()) for f in sys.argv[1:] for l in open(f,encoding='utf-8') if (m:=re.match(r'^([a-zA-Z][\w -]*):.*?##\s*(.*)',l))];[print(f'  {n:<14} {d}') for n,d in ms]" $(MAKEFILE_LIST)

sync: ## 安装开发依赖
	uv sync --extra dev

build b: ## 构建 Python 包
	uv build

clean c: ## 清理构建产物与缓存
	rm -rf build/ dist/ wheels/ *.egg-info htmlcov/ .coverage .coverage.* coverage.xml docs/_build/ .tox/ .preview/
	rm -rf .ruff_cache/ .pyrefly_cache/ .mypy_cache/
	find docs -type d -name __pycache__ -exec rm -rf {} +
	find docs -type f -name "*.py[oc]" -delete

lint: ## 代码风格检查 (ruff)
	uv run ruff check .
	uv run ruff format --check .

typecheck: ## 类型检查 (pyrefly)
	uv run pyrefly check

typecheck-ci: ## 类型检查 (pyrefly, CI 平台 linux — 捕获跨平台问题)
	uv run pyrefly check --python-platform linux

check: lint typecheck typecheck-ci cov ## 运行全套门禁 (lint + typecheck + typecheck-ci + cov)

test: ## 运行测试
	uv run pytest

cov: ## 运行测试并生成 HTML 覆盖率报告
	uv run pytest --cov --cov-report=html
	@echo "覆盖率报告：htmlcov/index.html"

doc: ## 构建 Sphinx 文档
	uv run sphinx-build -b html docs docs/_build/html

render: ## 渲染验证四种 project_type（输出到 .preview/）
	@rm -rf .preview && mkdir .preview
	@echo "渲染 library..."
	@uvx copier copy --trust --defaults --vcs-ref HEAD . .preview/lib || true
	@echo "渲染 cli..."
	@uvx copier copy --trust --defaults --vcs-ref HEAD . .preview/cli --data project_type=cli || true
	@echo "渲染 gui..."
	@uvx copier copy --trust --defaults --vcs-ref HEAD . .preview/gui --data project_type=gui || true
	@echo "渲染 web..."
	@uvx copier copy --trust --defaults --vcs-ref HEAD . .preview/web --data project_type=web || true
	@echo "渲染完成，检查 .preview/{lib,cli,gui,web}/"

BUMP_PART := $(filter-out bump,$(MAKECMDGOALS))

bump: ## 版本号 bump (默认 patch，用法: make bump [minor|major])
	@uvx bump-my-version bump $(if $(BUMP_PART),$(firstword $(BUMP_PART)),patch) --tag

patch minor major:
	@:

push: ## 推送代码到所有远程仓库
	@uv run python -c "import subprocess as sp; [print(f'\u63a8\u9001 {r}...',flush=True) or (sp.run(['git','push',r],check=True) and sp.run(['git','push',r,'--tags'],check=True)) for r in sp.check_output(['git','remote'],text=True).split()]"
