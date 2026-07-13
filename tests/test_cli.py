"""coopie CLI 测试，覆盖 cli.py 全部分支."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

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


# --- _build_parser ---


def test_build_parser_new(monkeypatch: pytest.MonkeyPatch) -> None:
    """new 子命令解析 project_name."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.command == "new"
    assert args.project_name == "my-project"


def test_build_parser_init(monkeypatch: pytest.MonkeyPatch) -> None:
    """init 子命令无位置参数."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.command == "init"


def test_build_parser_update(monkeypatch: pytest.MonkeyPatch) -> None:
    """update 子命令默认不带 skip 标志."""
    monkeypatch.setattr(sys, "argv", ["coopie", "update"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.command == "update"
    assert args.skip_answered is False
    assert args.skip_tasks is False


def test_build_parser_update_short_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    """update -A -T 解析为 skip_answered/skip_tasks."""
    monkeypatch.setattr(sys, "argv", ["coopie", "update", "-A", "-T"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.skip_answered is True
    assert args.skip_tasks is True


def test_build_parser_test(monkeypatch: pytest.MonkeyPatch) -> None:
    """test 子命令支持 -A -T."""
    monkeypatch.setattr(sys, "argv", ["coopie", "test", "-A", "-T"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.command == "test"
    assert args.skip_answered is True
    assert args.skip_tasks is True


def test_build_parser_version_long(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """--version 打印版本号并退出（退出码 0）."""
    monkeypatch.setattr(sys, "argv", ["coopie", "--version"])
    parser = cli._build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args()
    assert exc.value.code == 0
    assert cli.__version__ in capsys.readouterr().out


def test_build_parser_version_short(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """-V 打印版本号并退出（退出码 0）."""
    monkeypatch.setattr(sys, "argv", ["coopie", "-V"])
    parser = cli._build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args()
    assert exc.value.code == 0
    assert cli.__version__ in capsys.readouterr().out


def test_build_parser_no_command_exits(monkeypatch: pytest.MonkeyPatch) -> None:
    """无子命令时 argparse 报错退出."""
    monkeypatch.setattr(sys, "argv", ["coopie"])
    parser = cli._build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args()


def test_build_parser_new_type(monkeypatch: pytest.MonkeyPatch) -> None:
    """new --type gui 解析为 project_type=gui."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project", "--type", "gui"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.project_type == "gui"


def test_build_parser_new_type_default_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """new 不带 --type 时 project_type 默认 None."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.project_type is None


def test_build_parser_new_invalid_type(monkeypatch: pytest.MonkeyPatch) -> None:
    """new --type 非法值报错退出."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project", "--type", "invalid"])
    parser = cli._build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args()


def test_build_parser_init_type(monkeypatch: pytest.MonkeyPatch) -> None:
    """init --type web 解析为 project_type=web."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init", "--type", "web"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.project_type == "web"


# --- _is_directory_nonempty ---


def test_is_directory_nonempty_empty(tmp_path: Path) -> None:
    """空目录返回 False."""
    assert cli._is_directory_nonempty(tmp_path) is False


def test_is_directory_nonempty_with_file(tmp_path: Path) -> None:
    """有文件的目录返回 True."""
    (tmp_path / "file.txt").write_text("hello")
    assert cli._is_directory_nonempty(tmp_path) is True


def test_is_directory_nonempty_only_git(tmp_path: Path) -> None:
    """只有 .git 目录时返回 False."""
    (tmp_path / ".git").mkdir()
    assert cli._is_directory_nonempty(tmp_path) is False


# --- main: new ---


def test_main_new_without_git_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """无 git 配置时执行 copier copy，不含 author 数据."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
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
    assert "https://gitee.com/gooker_young/coopie.git" in cmd
    assert (tmp_path / "my_project").is_dir()
    assert not any("author_" in c for c in cmd)


def test_main_new_with_git_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """有 git 配置时附带 author_name 和 author_email."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
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


def test_main_new_only_author_name(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """仅有 user.name 时只附带 author_name."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    monkeypatch.chdir(tmp_path)

    def fake_git_config(key: str) -> str | None:
        return "gooker" if key == "user.name" else None

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


def test_main_new_only_author_email(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """仅有 user.email 时只附带 author_email."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    monkeypatch.chdir(tmp_path)

    def fake_git_config(key: str) -> str | None:
        return "gooker@qq.com" if key == "user.email" else None

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


def test_main_new_called_process_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """copier copy 失败时退出."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)

    def fake_run(cmd: list[str], **kwargs: object) -> None:
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit, match="1"):
        cli.main()


def test_main_new_with_type(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """new --type gui 时传递 project_type=gui 给 copier."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project", "--type", "gui"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "project_type=gui" in captured["cmd"]


def test_main_new_without_type_no_project_type(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """new 不带 --type 时命令不含 project_type."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert not any("project_type=" in c for c in captured["cmd"])


# --- main: init ---


def test_main_init_empty_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """空目录直接初始化，project_name 从目录名派生."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    cmd = captured["cmd"]
    assert "copy" in cmd
    assert f"project_name={tmp_path.name}" in cmd
    assert "." in cmd


def test_main_init_nonempty_confirm(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """非空目录用户确认 y 时继续初始化."""
    (tmp_path / "existing.txt").write_text("hello")
    monkeypatch.setattr(sys, "argv", ["coopie", "init"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "copy" in captured["cmd"]


def test_main_init_nonempty_cancel(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """非空目录用户输入 n 时取消初始化."""
    (tmp_path / "existing.txt").write_text("hello")
    monkeypatch.setattr(sys, "argv", ["coopie", "init"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "cmd" not in captured


def test_main_init_with_git_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """init 附带 author 数据."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init"])
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


def test_main_init_called_process_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """init copier copy 失败时退出."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)

    def fake_run(cmd: list[str], **kwargs: object) -> None:
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit, match="1"):
        cli.main()


def test_main_init_with_type(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """init --type cli 时传递 project_type=cli 给 copier."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init", "--type", "cli"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "project_type=cli" in captured["cmd"]


def test_main_init_without_type_no_project_type(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """init 不带 --type 时命令不含 project_type."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert not any("project_type=" in c for c in captured["cmd"])


# --- main: update ---


def test_main_update(monkeypatch: pytest.MonkeyPatch) -> None:
    """update 执行 copier update 命令."""
    monkeypatch.setattr(sys, "argv", ["coopie", "update"])
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert captured["cmd"] == ["uvx", "copier", "update"]


def test_main_update_skip_answered(monkeypatch: pytest.MonkeyPatch) -> None:
    """update -A 在命令中追加 --skip-answered."""
    monkeypatch.setattr(sys, "argv", ["coopie", "update", "-A"])
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert captured["cmd"] == ["uvx", "copier", "update", "--skip-answered"]


def test_main_update_skip_tasks(monkeypatch: pytest.MonkeyPatch) -> None:
    """update -T 在命令中追加 --skip-tasks."""
    monkeypatch.setattr(sys, "argv", ["coopie", "update", "-T"])
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert captured["cmd"] == ["uvx", "copier", "update", "--skip-tasks"]


def test_main_update_called_process_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """copier update 失败时退出."""
    monkeypatch.setattr(sys, "argv", ["coopie", "update"])

    def fake_run(cmd: list[str], **kwargs: object) -> None:
        raise subprocess.CalledProcessError(2, cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit, match="2"):
        cli.main()


# --- main: test ---


def test_main_test(monkeypatch: pytest.MonkeyPatch) -> None:
    """test 命令执行 copier update --pretend."""
    monkeypatch.setattr(sys, "argv", ["coopie", "test"])
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert captured["cmd"] == ["uvx", "copier", "update", "--pretend"]


def test_main_test_skip_answered(monkeypatch: pytest.MonkeyPatch) -> None:
    """test -A 在命令中追加 --skip-answered."""
    monkeypatch.setattr(sys, "argv", ["coopie", "test", "-A"])
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert captured["cmd"] == ["uvx", "copier", "update", "--pretend", "--skip-answered"]


def test_main_test_skip_tasks(monkeypatch: pytest.MonkeyPatch) -> None:
    """test -T 在命令中追加 --skip-tasks."""
    monkeypatch.setattr(sys, "argv", ["coopie", "test", "-T"])
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert captured["cmd"] == ["uvx", "copier", "update", "--pretend", "--skip-tasks"]


# --- _resolve_template_repo ---


def test_resolve_template_repo_cli_value(monkeypatch: pytest.MonkeyPatch) -> None:
    """--template 选项优先于环境变量和默认值."""
    monkeypatch.setenv("COOPIE_TEMPLATE_REPO", "https://env.example/repo")
    assert cli._resolve_template_repo("https://cli.example/repo") == "https://cli.example/repo"


def test_resolve_template_repo_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """无 --template 时用环境变量."""
    monkeypatch.setenv("COOPIE_TEMPLATE_REPO", "https://env.example/repo")
    assert cli._resolve_template_repo(None) == "https://env.example/repo"


def test_resolve_template_repo_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """无 --template 且无环境变量时用默认 Gitee 仓库."""
    monkeypatch.delenv("COOPIE_TEMPLATE_REPO", raising=False)
    assert cli._resolve_template_repo(None) == "https://gitee.com/gooker_young/coopie.git"


def test_resolve_template_repo_cli_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """--template 覆盖环境变量."""
    monkeypatch.setenv("COOPIE_TEMPLATE_REPO", "https://env.example/repo")
    assert cli._resolve_template_repo("/local/path") == "/local/path"


def test_resolve_template_repo_empty_env_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    """环境变量为空字符串时退回默认."""
    monkeypatch.setenv("COOPIE_TEMPLATE_REPO", "")
    assert cli._resolve_template_repo(None) == "https://gitee.com/gooker_young/coopie.git"


# --- _build_parser: --template ---


def test_build_parser_new_template(monkeypatch: pytest.MonkeyPatch) -> None:
    """new --template 解析为 template 字段."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project", "--template", "/local/path"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.template == "/local/path"


def test_build_parser_new_template_default_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """new 不带 --template 时 template 默认 None."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.template is None


def test_build_parser_init_template(monkeypatch: pytest.MonkeyPatch) -> None:
    """init --template 解析."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init", "--template", "/local/path"])
    parser = cli._build_parser()
    args = parser.parse_args()
    assert args.template == "/local/path"


# --- _run_copier: timeout / env ---


def test_run_copier_timeout(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """copier 超时时 sys.exit(1) 并打印提示."""

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        raise subprocess.TimeoutExpired(cmd, 600)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(SystemExit, match="1"):
        cli._run_copier(["uvx", "copier", "update"])
    err = capsys.readouterr().err
    assert "超时" in err
    assert "COOPIE_TEMPLATE_REPO" in err


def test_run_copier_passes_timeout_and_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """_run_copier 传递 timeout 和 env（含 RUST_LOG=warning）给 subprocess.run."""
    captured: dict[str, Any] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli._run_copier(["uvx", "copier", "update"])
    kwargs: dict[str, Any] = captured["kwargs"]
    assert kwargs["timeout"] == cli._COPIER_TIMEOUT
    assert kwargs["check"] is True
    assert kwargs["env"]["RUST_LOG"] == "warning"


def test_run_copier_preserves_other_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """_run_copier 的 env 保留父进程其他环境变量."""
    monkeypatch.setenv("MY_CUSTOM_VAR", "custom_value")
    captured: dict[str, dict[str, str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        env = kwargs["env"]
        assert isinstance(env, dict)
        captured["env"] = env
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli._run_copier(["uvx", "copier", "update"])
    assert captured["env"]["MY_CUSTOM_VAR"] == "custom_value"
    assert captured["env"]["RUST_LOG"] == "warning"


# --- main: new/init with --template ---


def test_main_new_with_template(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """new --template 传递给 copier 命令."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project", "--template", "/local/template"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "/local/template" in captured["cmd"]


def test_main_new_template_env_var(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """new 无 --template 但有 COOPIE_TEMPLATE_REPO 时用环境变量."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("COOPIE_TEMPLATE_REPO", "https://mirror.example/repo")
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "https://mirror.example/repo" in captured["cmd"]
    assert not any("gitee.com/gooker_young/coopie" in c for c in captured["cmd"])


def test_main_new_template_default(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """new 无 --template 无环境变量时用默认仓库."""
    monkeypatch.setattr(sys, "argv", ["coopie", "new", "my-project"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("COOPIE_TEMPLATE_REPO", raising=False)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "https://gitee.com/gooker_young/coopie.git" in captured["cmd"]


def test_main_init_with_template(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """init --template 传递给 copier 命令."""
    monkeypatch.setattr(sys, "argv", ["coopie", "init", "--template", "/local/template"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "_get_git_config", lambda _: None)
    captured: dict[str, list[str]] = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        captured["cmd"] = cmd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    cli.main()
    assert "/local/template" in captured["cmd"]
