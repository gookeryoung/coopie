"""coopie 基础冒烟测试."""

from __future__ import annotations

import coopie


def test_version_is_string() -> None:
    """__version__ 应为非空字符串."""
    assert isinstance(coopie.__version__, str)
    assert coopie.__version__


def test_package_importable() -> None:
    """包应可正常导入."""
    assert hasattr(coopie, "__all__")
    assert "__version__" in coopie.__all__
