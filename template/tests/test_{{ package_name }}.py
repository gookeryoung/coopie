"""{{ package_name }} 基础冒烟测试."""

from __future__ import annotations

import {{ package_name }}


def test_version_is_string() -> None:
    """__version__ 应为非空字符串."""
    assert isinstance({{ package_name }}.__version__, str)
    assert {{ package_name }}.__version__


def test_package_importable() -> None:
    """包应可正常导入."""
    assert hasattr({{ package_name }}, "__all__")
    assert "__version__" in {{ package_name }}.__all__
