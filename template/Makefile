# Makefile - {{ project_name }} project shortcuts
# Run `make help` to list all available commands

PACKAGE := {{ package_name }}
COV_THRESHOLD := {{ coverage_fail_under }}
PYTEST_JOBS := 8  # pytest-xdist worker count; 8 by default on Windows to avoid handle exhaustion

# Override with: make push REMOTES="origin codeup"
REMOTES = $(shell git remote)

.PHONY: help sync build b clean c test cov lint typecheck typecheck-ci check{% if use_docs %} doc{% endif %}{% if use_tox %} tox{% endif %} pub bump patch minor major push

help: ## Show this help
	@uv run python -c "import re,sys;ms=[(m.group(1),m.group(2).strip()) for f in sys.argv[1:] for l in open(f,encoding='utf-8') if (m:=re.match(r'^([a-zA-Z][\w -]*):.*?##\s*(.*)',l))];[print(f'  {n:<14} {d}') for n,d in ms]" $(MAKEFILE_LIST)

sync: ## Install development dependencies
	uv sync --extra dev

build b: ## Build distribution packages (wheel + sdist)
	uv build

clean c: ## Remove build artifacts and caches
	rm -rf build/ dist/ wheels/ *.egg-info htmlcov/ .coverage .coverage.* coverage.xml{% if use_docs %} docs/_build/{% endif %} .tox/
	rm -rf .ruff_cache/ .pyrefly_cache/ .mypy_cache/
	find src tests -type d -name __pycache__ -exec rm -rf {} +
	find src tests -type f -name "*.py[oc]" -delete

test: ## Run tests (no coverage)
	uv run pytest -m "not slow" -n $(PYTEST_JOBS)

cov: ## Run tests and generate an HTML coverage report
	uv run pytest --cov --cov-report=term --cov-fail-under=$(COV_THRESHOLD) --cov-report=html -n $(PYTEST_JOBS)
	@uv run python -c "print('Coverage report: htmlcov/index.html')"

lint: ## Lint code style (ruff)
	uv run ruff check .
	uv run ruff format --check .

typecheck: ## Type check (pyrefly)
	uv run pyrefly check

typecheck-ci: ## Type check (pyrefly, CI platform linux - catch cross-platform issues)
	uv run pyrefly check --python-platform linux

check: lint typecheck typecheck-ci cov ## Run the full gate (lint + typecheck + typecheck-ci + cov)
{% if use_docs %}
doc: ## Build the Sphinx documentation
	uv run sphinx-build -b html docs docs/_build/html
{% endif %}
{% if use_tox %}
tox: ## Run multi-version tests (tox)
	uvx tox -p auto
{% endif %}
BUMP_PART := $(filter-out bump,$(MAKECMDGOALS))

bump: ## Bump version (default patch, usage: make bump [minor|major])
	@uvx bump-my-version bump $(if $(BUMP_PART),$(firstword $(BUMP_PART)),patch) --tag
	uv sync --extra dev
	git add uv.lock
	-git diff --cached --quiet || git commit -m "chore: sync uv.lock after version bump"

patch minor major:
	@:

pub:  ## Upload to PyPI
	uvx twine upload dist/*.whl dist/*.tar.gz

push: ## Push code to all remotes (continues on failure, non-zero exit if any failed)
	@uv run python -c "import subprocess as sp,sys; remotes='$(REMOTES)'.split(); failed=[]; [failed.append(r) for r in remotes if print(f'Pushing {r}...',flush=True) or sp.run(['git','push',r]).returncode or sp.run(['git','push',r,'--tags']).returncode]; print('Failed remotes: '+', '.join(failed) if failed else 'All remotes pushed.'); sys.exit(1 if failed else 0)"

