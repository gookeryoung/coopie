"""copier 模板渲染测试：验证 Python 版本变量在 min/max 各组合下的派生正确性."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

import copier
import pytest

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def template_snapshot(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """把 copier.yml + template/ 快照为本地模板源（含未提交的工作树改动）.

    直接对仓库根渲染需配合 vcs_ref="HEAD"，每个用例都要走一次 git clone
    （实测 ~14.8s/次）；快照成普通目录后 copier 走本地渲染路径（实测 ~4.9s/次）。
    两者产物一致，差异仅在 .copier-answers.yml 的 _src_path/_commit，用例不依赖。
    """
    dst = tmp_path_factory.mktemp("coopie-template")
    shutil.copy2(TEMPLATE_ROOT / "copier.yml", dst / "copier.yml")
    shutil.copytree(TEMPLATE_ROOT / "template", dst / "template")
    return dst


@pytest.fixture(scope="session")
def render(
    template_snapshot: Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> Callable[[dict[str, Any]], Path]:
    """渲染模板，按 data 缓存产物，避免相同参数的用例重复渲染."""
    cache: dict[str, Path] = {}

    def _render(data: dict[str, Any]) -> Path:
        key = json.dumps(data, sort_keys=True)
        if key not in cache:
            dst = tmp_path_factory.mktemp("render")
            copier.run_copy(
                src_path=str(template_snapshot),
                dst_path=dst,
                data=data,
                defaults=True,
                quiet=True,
            )
            cache[key] = dst
        return cache[key]

    return _render


def _read(dst: Path, relpath: str) -> str:
    """读取渲染产物中的文本文件."""
    return (dst / relpath).read_text(encoding="utf-8")


def test_min_equals_max_ci_matrix_deduped(render: Callable[[dict[str, Any]], Path]) -> None:
    """min==max 时 CI 矩阵应去重为单版本，job name 不应出现重复."""
    dst = render({"min_python_version": "3.14", "max_python_version": "3.14"})
    ci = _read(dst, ".github/workflows/ci.yml")
    assert 'python-version: ["3.14"]' in ci
    assert "name: Test (Python 3.14)" in ci
    assert "3.14 & 3.14" not in ci


def test_min_lt_max_matrix_keeps_two_versions(render: Callable[[dict[str, Any]], Path]) -> None:
    """min<max 时 CI 矩阵保留首尾两个版本."""
    dst = render({"min_python_version": "3.10", "max_python_version": "3.12"})
    ci = _read(dst, ".github/workflows/ci.yml")
    assert 'python-version: ["3.10", "3.12"]' in ci
    assert "name: Test (Python 3.10 & 3.12)" in ci


def test_min_equals_max_tox_envlist_single_env(render: Callable[[dict[str, Any]], Path]) -> None:
    """min==max 时 tox envlist 应只有单环境."""
    dst = render({"min_python_version": "3.8", "max_python_version": "3.8", "use_tox": True})
    tox = _read(dst, "tox.ini")
    assert "envlist = py38" in tox


def test_min_lt_max_tox_envlist_full_range(render: Callable[[dict[str, Any]], Path]) -> None:
    """min<max 时 tox envlist 应覆盖完整区间."""
    dst = render({"min_python_version": "3.10", "max_python_version": "3.12", "use_tox": True})
    tox = _read(dst, "tox.ini")
    assert "envlist = py310, py311, py312" in tox


def test_min_equals_max_classifiers_single_version(render: Callable[[dict[str, Any]], Path]) -> None:
    """min==max 时 pyproject 分类器应只含一个具体版本."""
    dst = render({"min_python_version": "3.8", "max_python_version": "3.8"})
    pyproject = _read(dst, "pyproject.toml")
    version_lines = [line for line in pyproject.splitlines() if '"Programming Language :: Python :: 3.' in line]
    assert version_lines == ['    "Programming Language :: Python :: 3.8",']


def test_min_lt_max_classifiers_full_range(render: Callable[[dict[str, Any]], Path]) -> None:
    """min<max 时 pyproject 分类器应覆盖完整区间."""
    dst = render({"min_python_version": "3.10", "max_python_version": "3.12"})
    pyproject = _read(dst, "pyproject.toml")
    for version in ("3.10", "3.11", "3.12"):
        assert f'"Programming Language :: Python :: {version}",' in pyproject


def test_min_equals_max_dockerfile_installs_once(render: Callable[[dict[str, Any]], Path]) -> None:
    """min==max 时 Dockerfile 不应重复安装同一版本."""
    dst = render({"min_python_version": "3.12", "max_python_version": "3.12", "use_docker": True})
    dockerfile = _read(dst, "Dockerfile")
    assert "RUN uv python install 3.12\n" in dockerfile
    assert "uv python install 3.12 3.12" not in dockerfile
    assert "FROM docker.m.daocloud.io/python:3.12-slim" in dockerfile


def test_min_lt_max_dockerfile_installs_both(render: Callable[[dict[str, Any]], Path]) -> None:
    """min<max 时 Dockerfile 应安装两个版本."""
    dst = render({"min_python_version": "3.10", "max_python_version": "3.12", "use_docker": True})
    dockerfile = _read(dst, "Dockerfile")
    assert "RUN uv python install 3.10 3.12" in dockerfile


def test_min_equals_max_readme_shows_single_version(render: Callable[[dict[str, Any]], Path]) -> None:
    """min==max 时 README 特性行应只显示一个版本."""
    dst = render({"min_python_version": "3.14", "max_python_version": "3.14"})
    readme = _read(dst, "README.md")
    assert "**Python 版本**：3.14" in readme
    assert "3.14 ~ 3.14" not in readme


def test_min_gt_max_validator_rejects(render: Callable[[dict[str, Any]], Path]) -> None:
    """min>max 应触发 max_python_version 的 validator 拒绝渲染."""
    with pytest.raises(ValueError, match="不能低于最低版本"):
        render({"min_python_version": "3.14", "max_python_version": "3.10"})


def test_min_equals_max_boundary_accepted(render: Callable[[dict[str, Any]], Path]) -> None:
    """min==max 是合法边界，不应触发 validator."""
    dst = render({"min_python_version": "3.10", "max_python_version": "3.10", "use_tox": True})
    tox = _read(dst, "tox.ini")
    assert "envlist = py310" in tox
