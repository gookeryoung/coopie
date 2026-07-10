"""coopie CLI 测试，覆盖 cli.py 全部分支."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from coopie import cli

# --- _get_git_config ---


def test_get_git_config_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """git config 查询成功时返回去空白后的值."""
    fake_result = SimpleNamespace(stdout="gooker\n")

    def fake_run(*args: object, **kwargs: object) -> SimpleNamespace:
        return fake_result

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert cli._get_git_config("user.name") == "gooker"


def test_get_git_config_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """git config 输出为空时返回 None."""
    fake_result = SimpleNamespace(stdout="")

    def fake_run(*args: object, **kwargs: object) -> SimpleNamespace:
        return fake_result

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert cli._get_git_config("user.name") is None


def test_get_git_config_filenotfounderror(monkeypatch: pytest.MonkeyPatch) -> None:
    """git 命令不存在（FileNotFoundError）时返回 None."""

    def raise_fnf(*a: object, **kw: object) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(subprocess, "run", raise_fnf)
    assert cli._get_git_config("user.name") is None


def test_get_git_config_oserror(monkeypatch: pytest.MonkeyPatch) -> None:
    """git 命令执行 OS 错误时返回 None."""

    def raise_os(*a: object, **kw: object) -> None:
        raise OSError

    monkeypatch.setattr(subprocess, "run", raise_os)
    assert cli._get_git_config("user.name") is None


# --- _get_args ---


def test_get_args_project_name(monkeypatch: pytest.MonkeyPatch) -> None:
    """解析位置参数 project_name."""
    monkeypatch.setattr(sys, "argv", ["coopie", "my-project"])
    args = cli._get_args()
    assert args.project_name == "my-project"
    assert args.update is False


def test_get_args_update_long(monkeypatch: pytest.MonkeyPatch) -> None:
    """解析 --update 长选项."""
    monkeypatch.setattr(sys, "argv", ["coopie", "--update"])
    args = cli._get_args()
    assert args.update is True
    assert args.project_name is None


def test_get_args_update_short(monkeypatch: pytest.MonkeyPatch) -> None:
    """解析 -U 短选项."""
    monkeypatch.setattr(sys, "argv", ["coopie", "-U"])
    args = cli._get_args()
    assert args.update is True


def test_get_args_no_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """无参数时 project_name 为 None、update 为 False."""
    monkeypatch.setattr(sys, "argv", ["coopie"])
    args = cli._get_args()
    assert args.project_name is None
    assert args.update is False


# --- main: 互斥与缺参退出 ---


def test_main_update_with_project_name_exits(monkeypatch: pytest.MonkeyPatch) -> None:
    """--update 与 project_name 同时提供时退出."""
    monkeypatch.setattr(sys, "argv", ["coopie", "--update", "my-project"])
    with pytest.raises(SystemExit, match="互斥"):
        cli.main()


def test_main_no_args_exits(monkeypatch: pytest.MonkeyPatch) -> None:
    """无参数时退出."""
    monkeypatch.setattr(sys, "argv", ["coopie"])
    with pytest.raises(SystemExit, match="required"):
        cli.main()


# --- main: --update 流程 ---


def test_main_update(monkeypatch: pytest.MonkeyPatch) -> None:
    """--update 执行 copier update 命令."""
    monkeypatch.setattr(sys, "argv", ["coopie", "--update"])
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert captured["cmd"] == ["uvx", "--with", "jinja2-time", "copier", "update", "--trust"]


def test_main_update_called_process_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """copier update 失败时退出."""
    monkeypatch.setattr(sys, "argv", ["coopie", "--update"])

    def fake_run(cmd: list[str], **kwargs: object) -> None:
        raise subprocess.CalledProcessError(2, cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit, match="2"):
        cli.main()


# --- main: copy 流程 ---


def test_main_copy_without_git_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """无 git 配置时执行 copier copy，不含 author 数据."""
    monkeypatch.setattr(sys, "argv", ["coopie", "my-project"])
    monkeypatch.chdir(tmp_path)

    def fake_git_config(key: str) -> str | None:
        return None

    monkeypatch.setattr(cli, "_get_git_config", fake_git_config)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    cmd = captured["cmd"]
    assert "copier" in cmd
    assert "copy" in cmd
    assert "project_name=my-project" in cmd
    assert "https://github.com/gookeryoung/coopie" in cmd
    assert (tmp_path / "my_project").is_dir()
    assert not any("author_" in c for c in cmd)


def test_main_copy_with_git_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """有 git 配置时附带 author_name 和 author_email."""
    monkeypatch.setattr(sys, "argv", ["coopie", "my-project"])
    monkeypatch.chdir(tmp_path)

    def fake_git_config(key: str) -> str | None:
        if key == "user.name":
            return "gooker"
        if key == "user.email":
            return "gooker@qq.com"
        return None

    monkeypatch.setattr(cli, "_get_git_config", fake_git_config)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    cmd = captured["cmd"]
    assert "author_name=gooker" in cmd
    assert "author_email=gooker@qq.com" in cmd


def test_main_copy_only_author_name(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """仅有 user.name 时只附带 author_name."""

    def fake_git_config(key: str) -> str | None:
        return "gooker" if key == "user.name" else None

    monkeypatch.setattr(sys, "argv", ["coopie", "my-project"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", fake_git_config)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    cmd = captured["cmd"]
    assert "author_name=gooker" in cmd
    assert not any("author_email=" in c for c in cmd)


def test_main_copy_only_author_email(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """仅有 user.email 时只附带 author_email."""

    def fake_git_config(key: str) -> str | None:
        return "gooker@qq.com" if key == "user.email" else None

    monkeypatch.setattr(sys, "argv", ["coopie", "my-project"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", fake_git_config)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    cmd = captured["cmd"]
    assert "author_email=gooker@qq.com" in cmd
    assert not any("author_name=" in c for c in cmd)


def test_main_copy_called_process_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """copier copy 失败时退出."""
    monkeypatch.setattr(sys, "argv", ["coopie", "my-project"])
    monkeypatch.chdir(tmp_path)

    def fake_git_config(key: str) -> str | None:
        return None

    monkeypatch.setattr(cli, "_get_git_config", fake_git_config)

    def fake_run(cmd: list[str], **kwargs: object) -> None:
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit, match="1"):
        cli.main()
