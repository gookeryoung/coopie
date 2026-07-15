"""coopie CLI 测试."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from coopie.cli import DEFAULT_URL, app

runner = CliRunner()


def test_version_flag() -> None:
    """--version 应输出版本号并退出 0."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "coopie" in result.stdout


def test_no_args_shows_help() -> None:
    """无参数应显示帮助."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "coopie" in result.stdout.lower()
    assert "Usage" in result.stdout or "用法" in result.stdout


def test_init_calls_copier_copy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """init 命令应调用 copier copy --trust."""
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest])

    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0][:4] == ["copier", "copy", "--trust", DEFAULT_URL]
    assert calls[0][-1] == dest


def test_init_with_custom_url(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """--url 应覆盖默认模板源."""
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    custom_url = "https://github.com/gookeryoung/coopie.git"
    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest, "--url", custom_url])

    assert result.exit_code == 0
    assert calls[0][3] == custom_url


def test_init_with_vcs_ref(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """--vcs-ref 应传递给 copier."""
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest, "--vcs-ref", "v0.8.0"])

    assert result.exit_code == 0
    assert "--vcs-ref" in calls[0]
    assert "v0.8.0" in calls[0]


def test_init_with_defaults_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """--defaults 应传递给 copier."""
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest, "--defaults"])

    assert result.exit_code == 0
    assert "--defaults" in calls[0]


def test_init_copier_not_found(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """copier 不存在时应报错并退出 1."""

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        raise FileNotFoundError(cmd[0])

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest])

    assert result.exit_code == 1
    assert "copier" in result.stdout


def test_init_copier_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """copier 返回非零时应传递退出码."""

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        raise subprocess.CalledProcessError(42, cmd)

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest])

    assert result.exit_code == 42


def test_update_calls_copier_recopy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update 命令应调用 copier recopy --trust."""
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    (project_dir / ".copier-answers.yml").write_text("# test", encoding="utf-8")

    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    result = runner.invoke(app, ["update", str(project_dir)])

    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0][:3] == ["copier", "recopy", "--trust"]


def test_update_without_answers_file(tmp_path: Path) -> None:
    """目录缺少 .copier-answers.yml 应报错退出 1."""
    project_dir = tmp_path / "no-answers"
    project_dir.mkdir()

    result = runner.invoke(app, ["update", str(project_dir)])

    assert result.exit_code == 1
    assert ".copier-answers.yml" in result.stdout


def test_update_defaults_to_current_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update 无参数时默认使用当前目录."""
    (tmp_path / ".copier-answers.yml").write_text("# test", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    result = runner.invoke(app, ["update"])

    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0][:3] == ["copier", "recopy", "--trust"]


def test_update_with_vcs_ref(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update --vcs-ref 应传递给 copier."""
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    (project_dir / ".copier-answers.yml").write_text("# test", encoding="utf-8")

    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    result = runner.invoke(app, ["update", str(project_dir), "--vcs-ref", "v0.8.0"])

    assert result.exit_code == 0
    assert "--vcs-ref" in calls[0]
    assert "v0.8.0" in calls[0]


def test_update_with_defaults_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update --defaults 应传递给 copier."""
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    (project_dir / ".copier-answers.yml").write_text("# test", encoding="utf-8")

    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    result = runner.invoke(app, ["update", str(project_dir), "--defaults"])

    assert result.exit_code == 0
    assert "--defaults" in calls[0]


def test_run_copier_sets_utf8_mode(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """_run_copier 应设置 PYTHONUTF8=1 避免 Windows GBK 区域读取中文 answers 失败."""
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    (project_dir / ".copier-answers.yml").write_text("# test", encoding="utf-8")

    captured_env: dict[str, str] = {}

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        captured_env.update(kwargs.get("env", {}))
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr("coopie.cli.subprocess.run", fake_run)

    result = runner.invoke(app, ["update", str(project_dir)])

    assert result.exit_code == 0
    assert captured_env.get("PYTHONUTF8") == "1"
