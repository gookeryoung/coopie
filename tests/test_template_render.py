"""copier 模板渲染测试：验证 Python 版本变量在 min/max 各组合下的派生正确性."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import copier
import pytest

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent


def _render(tmp_path: Path, data: dict[str, Any]) -> Path:
    """用给定数据渲染模板到临时目录，返回目标路径.

    vcs_ref="HEAD" 使 copier 以工作树（含未提交修改）为渲染源，
    否则默认检出最新 tag 的已提交版本。
    """
    dst = tmp_path / "proj"
    copier.run_copy(
        src_path=str(TEMPLATE_ROOT),
        dst_path=dst,
        data=data,
        vcs_ref="HEAD",
        defaults=True,
        quiet=True,
    )
    return dst


def _read(dst: Path, relpath: str) -> str:
    """读取渲染产物中的文本文件."""
    return (dst / relpath).read_text(encoding="utf-8")


def test_min_equals_max_ci_matrix_deduped(tmp_path: Path) -> None:
    """min==max 时 CI 矩阵应去重为单版本，job name 不应出现重复."""
    dst = _render(tmp_path, {"min_python_version": "3.14", "max_python_version": "3.14"})
    ci = _read(dst, ".github/workflows/ci.yml")
    assert 'python-version: ["3.14"]' in ci
    assert "name: Test (Python 3.14)" in ci
    assert "3.14 & 3.14" not in ci


def test_min_lt_max_matrix_keeps_two_versions(tmp_path: Path) -> None:
    """min<max 时 CI 矩阵保留首尾两个版本."""
    dst = _render(tmp_path, {"min_python_version": "3.10", "max_python_version": "3.12"})
    ci = _read(dst, ".github/workflows/ci.yml")
    assert 'python-version: ["3.10", "3.12"]' in ci
    assert "name: Test (Python 3.10 & 3.12)" in ci


def test_min_equals_max_tox_envlist_single_env(tmp_path: Path) -> None:
    """min==max 时 tox envlist 应只有单环境."""
    dst = _render(tmp_path, {"min_python_version": "3.8", "max_python_version": "3.8", "use_tox": True})
    tox = _read(dst, "tox.ini")
    assert "envlist = py38" in tox


def test_min_lt_max_tox_envlist_full_range(tmp_path: Path) -> None:
    """min<max 时 tox envlist 应覆盖完整区间."""
    dst = _render(tmp_path, {"min_python_version": "3.10", "max_python_version": "3.12", "use_tox": True})
    tox = _read(dst, "tox.ini")
    assert "envlist = py310, py311, py312" in tox


def test_min_equals_max_classifiers_single_version(tmp_path: Path) -> None:
    """min==max 时 pyproject 分类器应只含一个具体版本."""
    dst = _render(tmp_path, {"min_python_version": "3.8", "max_python_version": "3.8"})
    pyproject = _read(dst, "pyproject.toml")
    version_lines = [line for line in pyproject.splitlines() if '"Programming Language :: Python :: 3.' in line]
    assert version_lines == ['    "Programming Language :: Python :: 3.8",']


def test_min_lt_max_classifiers_full_range(tmp_path: Path) -> None:
    """min<max 时 pyproject 分类器应覆盖完整区间."""
    dst = _render(tmp_path, {"min_python_version": "3.10", "max_python_version": "3.12"})
    pyproject = _read(dst, "pyproject.toml")
    for version in ("3.10", "3.11", "3.12"):
        assert f'"Programming Language :: Python :: {version}",' in pyproject


def test_min_equals_max_dockerfile_installs_once(tmp_path: Path) -> None:
    """min==max 时 Dockerfile 不应重复安装同一版本."""
    dst = _render(tmp_path, {"min_python_version": "3.12", "max_python_version": "3.12", "use_docker": True})
    dockerfile = _read(dst, "Dockerfile")
    assert "RUN uv python install 3.12\n" in dockerfile
    assert "uv python install 3.12 3.12" not in dockerfile
    assert "FROM docker.m.daocloud.io/python:3.12-slim" in dockerfile


def test_min_lt_max_dockerfile_installs_both(tmp_path: Path) -> None:
    """min<max 时 Dockerfile 应安装两个版本."""
    dst = _render(tmp_path, {"min_python_version": "3.10", "max_python_version": "3.12", "use_docker": True})
    dockerfile = _read(dst, "Dockerfile")
    assert "RUN uv python install 3.10 3.12" in dockerfile


def test_min_equals_max_readme_shows_single_version(tmp_path: Path) -> None:
    """min==max 时 README 特性行应只显示一个版本."""
    dst = _render(tmp_path, {"min_python_version": "3.14", "max_python_version": "3.14"})
    readme = _read(dst, "README.md")
    assert "**Python 版本**：3.14" in readme
    assert "3.14 ~ 3.14" not in readme


def test_min_gt_max_validator_rejects(tmp_path: Path) -> None:
    """min>max 应触发 max_python_version 的 validator 拒绝渲染."""
    with pytest.raises(ValueError, match="不能低于最低版本"):
        _render(tmp_path, {"min_python_version": "3.14", "max_python_version": "3.10"})


def test_min_equals_max_boundary_accepted(tmp_path: Path) -> None:
    """min==max 是合法边界，不应触发 validator."""
    dst = _render(tmp_path, {"min_python_version": "3.10", "max_python_version": "3.10", "use_tox": True})
    tox = _read(dst, "tox.ini")
    assert "envlist = py310" in tox
