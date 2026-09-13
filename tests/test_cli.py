"""coopie CLI 测试."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from typer.testing import CliRunner

from coopie.cli import (
    DEFAULT_URL,
    _ensure_answers_url_normalized,
    _normalize_url,
    _patch_copier_vcs,
    _read_answers_src_path,
    app,
)

runner = CliRunner()


def test_version_flag() -> None:
    """--version 应输出版本号并退出 0."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "coopie" in result.stdout


def test_no_args_shows_help() -> None:
    """无参数应显示帮助（exit_code 可能是 0 或 2，取决于 Typer 版本）."""
    result = runner.invoke(app, [])
    assert "coopie" in result.stdout.lower()
    assert "Usage" in result.stdout or "用法" in result.stdout


# ---------------------------------------------------------------------------
# _normalize_url 单测
# ---------------------------------------------------------------------------


class TestNormalizeUrl:
    def test_https_no_git(self) -> None:
        assert _normalize_url("https://gitee.com/gooker_young/coopie") == "https://gitee.com/gooker_young/coopie.git"

    def test_https_with_git(self) -> None:
        assert (
            _normalize_url("https://gitee.com/gooker_young/coopie.git") == "https://gitee.com/gooker_young/coopie.git"
        )

    def test_http_no_git(self) -> None:
        assert _normalize_url("http://example.com/repo") == "http://example.com/repo.git"

    def test_ssh(self) -> None:
        ssh = "git@gitee.com:gooker_young/coopie.git"
        assert _normalize_url(ssh) == ssh

    def test_local_path(self) -> None:
        assert _normalize_url("./local/template") == "./local/template"
        assert _normalize_url("/tmp/tpl") == "/tmp/tpl"


# ---------------------------------------------------------------------------
# _ensure_answers_url_normalized 单测
# ---------------------------------------------------------------------------


class TestEnsureAnswersUrl:
    def test_https_without_git_suffix_is_fixed(self, tmp_path: Path) -> None:
        answers = {
            "_src_path": "https://gitee.com/gooker_young/coopie",
            "_commit": "v0.9.7",
            "package_name": "demo",
        }
        f = tmp_path / ".copier-answers.yml"
        f.write_text(yaml.dump(answers), encoding="utf-8")

        _ensure_answers_url_normalized(f)

        loaded = yaml.safe_load(f.read_text(encoding="utf-8"))
        assert loaded["_src_path"] == "https://gitee.com/gooker_young/coopie.git"

    def test_https_already_has_git_suffix_not_touched(self, tmp_path: Path) -> None:
        answers = {
            "_src_path": "https://gitee.com/gooker_young/coopie.git",
            "_commit": "v0.9.7",
        }
        f = tmp_path / ".copier-answers.yml"
        f.write_text(yaml.dump(answers), encoding="utf-8")

        _ensure_answers_url_normalized(f)

        loaded = yaml.safe_load(f.read_text(encoding="utf-8"))
        assert loaded["_src_path"] == "https://gitee.com/gooker_young/coopie.git"

    def test_ssh_url_not_touched(self, tmp_path: Path) -> None:
        answers = {
            "_src_path": "git@gitee.com:gooker_young/coopie.git",
            "_commit": "v0.9.7",
        }
        f = tmp_path / ".copier-answers.yml"
        f.write_text(yaml.dump(answers), encoding="utf-8")

        _ensure_answers_url_normalized(f)

        loaded = yaml.safe_load(f.read_text(encoding="utf-8"))
        assert loaded["_src_path"] == "git@gitee.com:gooker_young/coopie.git"

    def test_missing_file_is_skipped(self, tmp_path: Path) -> None:
        _ensure_answers_url_normalized(tmp_path / "nonexistent.yml")

    def test_invalid_yaml_is_skipped(self, tmp_path: Path) -> None:
        f = tmp_path / ".copier-answers.yml"
        f.write_text(":::: invalid ::::", encoding="utf-8")
        # 不应抛异常
        _ensure_answers_url_normalized(f)

    def test_non_dict_yaml_is_skipped(self, tmp_path: Path) -> None:
        f = tmp_path / ".copier-answers.yml"
        f.write_text("just a string", encoding="utf-8")
        _ensure_answers_url_normalized(f)


# ---------------------------------------------------------------------------
# init 命令
# ---------------------------------------------------------------------------


def test_init_calls_copier_copy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """init 命令应调 copier.run_copy，传 src_path=带 .git 的 DEFAULT_URL."""
    captured: dict[str, Any] = {}

    def fake_run_copy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_copy", fake_run_copy)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest])

    assert result.exit_code == 0
    assert captured["src_path"] == DEFAULT_URL  # DEFAULT_URL 已带 .git
    assert captured["dst_path"] == Path(dest).resolve()
    assert captured["vcs_ref"] is None
    assert captured["defaults"] is False
    # trust 里包含模板 URL（仅 copier 9.17+ 有 Settings）
    if "settings" in captured and captured["settings"] is not None:
        assert DEFAULT_URL in captured["settings"].trust


def test_init_with_custom_url_normalized(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """--url 不带 .git 后缀时应自动补."""
    captured: dict[str, Any] = {}

    def fake_run_copy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_copy", fake_run_copy)

    custom_url = "https://github.com/gookeryoung/coopie"  # 不带 .git
    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest, "--url", custom_url])

    assert result.exit_code == 0
    # 应被 _normalize_url 补成 .git
    assert captured["src_path"] == "https://github.com/gookeryoung/coopie.git"


def test_init_with_vcs_ref(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """--vcs-ref 应传递给 copier."""
    captured: dict[str, Any] = {}

    def fake_run_copy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_copy", fake_run_copy)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest, "--vcs-ref", "v0.8.0"])

    assert result.exit_code == 0
    assert captured["vcs_ref"] == "v0.8.0"


def test_init_with_defaults_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """--defaults 应传递给 copier."""
    captured: dict[str, Any] = {}

    def fake_run_copy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_copy", fake_run_copy)

    dest = str(tmp_path / "my-project")
    result = runner.invoke(app, ["init", dest, "--defaults"])

    assert result.exit_code == 0
    assert captured["defaults"] is True


# ---------------------------------------------------------------------------
# update 命令
# ---------------------------------------------------------------------------


def _make_answers(project_dir: Path, src_path: str = "https://gitee.com/gooker_young/coopie") -> None:
    """在 project_dir 创建 .copier-answers.yml."""
    project_dir.mkdir(parents=True, exist_ok=True)
    answers = {"_src_path": src_path, "_commit": "v0.9.7", "package_name": "demo"}
    (project_dir / ".copier-answers.yml").write_text(yaml.dump(answers, sort_keys=False), encoding="utf-8")


def test_update_calls_copier_recopy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update 命令应调 copier.run_recopy."""
    project_dir = tmp_path / "my-project"
    _make_answers(project_dir)

    captured: dict[str, Any] = {}

    def fake_run_recopy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_recopy", fake_run_recopy)

    result = runner.invoke(app, ["update", str(project_dir)])

    assert result.exit_code == 0
    assert captured["dst_path"] == project_dir.resolve()
    assert captured["vcs_ref"] is None
    assert captured["defaults"] is False
    # trust 里包含 answers 中的 src_path（已被补成 .git，仅 copier 9.17+ 有 Settings）
    if "settings" in captured and captured["settings"] is not None:
        assert "https://gitee.com/gooker_young/coopie.git" in captured["settings"].trust


def test_update_fixes_answers_src_path_git_suffix(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update 前应把 answers 里不带 .git 的 HTTPS URL 修正."""
    project_dir = tmp_path / "my-project"
    _make_answers(project_dir, src_path="https://gitee.com/gooker_young/coopie")

    def fake_run_recopy(**kwargs: Any) -> None:
        return None

    monkeypatch.setattr("copier.run_recopy", fake_run_recopy)

    runner.invoke(app, ["update", str(project_dir)])

    # answers 文件应被修正
    loaded = yaml.safe_load((project_dir / ".copier-answers.yml").read_text(encoding="utf-8"))
    assert loaded["_src_path"] == "https://gitee.com/gooker_young/coopie.git"


def test_update_without_answers_file(tmp_path: Path) -> None:
    """目录缺少 .copier-answers.yml 应报错退出 1."""
    project_dir = tmp_path / "no-answers"
    project_dir.mkdir()

    result = runner.invoke(app, ["update", str(project_dir)])

    assert result.exit_code == 1
    assert ".copier-answers.yml" in result.output


def test_update_defaults_to_current_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update 无参数时默认使用当前目录."""
    _make_answers(tmp_path)
    monkeypatch.chdir(tmp_path)

    captured: dict[str, Any] = {}

    def fake_run_recopy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_recopy", fake_run_recopy)

    result = runner.invoke(app, ["update"])

    assert result.exit_code == 0
    assert captured["dst_path"] == tmp_path.resolve()


def test_update_with_vcs_ref(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update --vcs-ref 应传递给 copier."""
    project_dir = tmp_path / "my-project"
    _make_answers(project_dir)

    captured: dict[str, Any] = {}

    def fake_run_recopy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_recopy", fake_run_recopy)

    result = runner.invoke(app, ["update", str(project_dir), "--vcs-ref", "v0.8.0"])

    assert result.exit_code == 0
    assert captured["vcs_ref"] == "v0.8.0"


def test_update_with_defaults_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """update --defaults 应传递给 copier."""
    project_dir = tmp_path / "my-project"
    _make_answers(project_dir)

    captured: dict[str, Any] = {}

    def fake_run_recopy(**kwargs: Any) -> None:
        captured.update(kwargs)

    monkeypatch.setattr("copier.run_recopy", fake_run_recopy)

    result = runner.invoke(app, ["update", str(project_dir), "--defaults"])

    assert result.exit_code == 0
    assert captured["defaults"] is True


def test_update_copier_user_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """copier 抛出 UserMessageError 应转为退出码 1."""
    import copier.errors

    project_dir = tmp_path / "my-project"
    _make_answers(project_dir)

    def fake_run_recopy(**kwargs: Any) -> None:
        raise copier.errors.UserMessageError("目标目录不干净")

    monkeypatch.setattr("copier.run_recopy", fake_run_recopy)

    result = runner.invoke(app, ["update", str(project_dir)])

    assert result.exit_code == 1
    assert "目标目录不干净" in result.output


# ---------------------------------------------------------------------------
# GIT_PREFIX patch 验证
# ---------------------------------------------------------------------------


def _get_vcs_module() -> Any:
    """获取 copier 的 VCS 内部模块（兼容 copier 9.3.x 的 vcs 和 9.17+ 的 _vcs）."""
    import importlib

    try:
        return importlib.import_module("copier._vcs")
    except ImportError:
        return importlib.import_module("copier.vcs")


def test_git_prefix_patch_includes_gitee() -> None:
    """_patch_copier_vcs 后 GIT_PREFIX 应包含 Gitee/Codeup 等国内平台."""
    vcs_mod = _get_vcs_module()
    assert "https://gitee.com/" in vcs_mod.GIT_PREFIX
    assert "https://codeup.aliyun.com/" in vcs_mod.GIT_PREFIX


def test_get_repo_recognizes_gitee_https() -> None:
    """get_repo 应能识别 Gitee HTTPS URL（带/不带 .git 后缀）."""
    vcs_mod = _get_vcs_module()
    get_repo = vcs_mod.get_repo

    # 不带 .git 后缀
    assert get_repo("https://gitee.com/gooker_young/coopie") is not None
    # 带 .git 后缀
    assert get_repo("https://gitee.com/gooker_young/coopie.git") is not None
    # Codeup
    assert get_repo("https://codeup.aliyun.com/cndev/python/coopie") is not None


# ---------------------------------------------------------------------------
# _patch_copier_vcs 的 fallback 分支覆盖
# ---------------------------------------------------------------------------


def test_patch_vcs_fallback_to_vcs_module(monkeypatch: pytest.MonkeyPatch) -> None:
    """当 _vcs 不可用时应 fallback 到 vcs（Python 3.8 路径）."""
    import sys

    import copier

    original_meta_path = list(sys.meta_path)

    # 在 meta_path 最前面插入一个 finder，阻止 copier._vcs 被加载
    class _BlockVCSFinder:
        @classmethod
        def find_spec(cls, fullname: str, _path: Any = None, _target: Any = None) -> Any:
            if fullname == "copier._vcs":
                raise ImportError("blocked for test")
            return None

    sys.meta_path.insert(0, _BlockVCSFinder)
    monkeypatch.setattr(sys, "meta_path", original_meta_path)

    # 清掉缓存
    if hasattr(copier, "_vcs"):
        delattr(copier, "_vcs")
    sys.modules.pop("copier._vcs", None)

    # 不应抛异常，说明走到了 fallback 分支
    _patch_copier_vcs()

    # fallback 后 vcs 模块的 GIT_PREFIX 也应包含国内平台
    from copier import vcs as vcs_mod

    assert "https://gitee.com/" in vcs_mod.GIT_PREFIX


# ---------------------------------------------------------------------------
# _read_answers_src_path 异常分支覆盖
# ---------------------------------------------------------------------------


class TestReadAnswersSrcPath:
    def test_normal_dict(self, tmp_path: Path) -> None:
        f = tmp_path / ".copier-answers.yml"
        f.write_text(yaml.dump({"_src_path": "https://github.com/a/b.git"}), encoding="utf-8")
        assert _read_answers_src_path(f) == "https://github.com/a/b.git"

    def test_yaml_parse_error_returns_empty(self, tmp_path: Path) -> None:
        """YAML 解析失败应返回空字符串."""
        f = tmp_path / ".copier-answers.yml"
        f.write_text(":::: not valid yaml ::::", encoding="utf-8")
        assert _read_answers_src_path(f) == ""

    def test_non_dict_returns_empty(self, tmp_path: Path) -> None:
        """YAML 解析结果不是 dict 应返回空字符串."""
        f = tmp_path / ".copier-answers.yml"
        f.write_text("just a plain string", encoding="utf-8")
        assert _read_answers_src_path(f) == ""
