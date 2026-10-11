"""coopie CLI 入口.

提供 init/update 两个命令，封装 copier copy/recopy 调用，简化模板使用。

示例::

    coopie init my-project
    coopie init my-project --url https://github.com/gookeryoung/coopie.git
    coopie update                    # 在已有项目目录中执行
    coopie update /path/to/project
    coopie update --trust            # 跳过模板执行安全确认（仅用于可信模板源）
"""

from __future__ import annotations

import contextlib
import os
import sys
from pathlib import Path
from typing import Any, Optional

# Windows 下 copier 派生的子进程（git 等）读非 ASCII 内容时可能因 GBK 区域触发
# UnicodeDecodeError。注意：PEP 540 的 UTF-8 模式只在解释器启动时读取 PYTHONUTF8，
# 进程内设置对本进程无效，仅对 copier 后续派生的子进程生效。
if os.name == "nt" and not sys.flags.utf8_mode:
    os.environ.setdefault("PYTHONUTF8", "1")

import typer

from coopie import __version__

__all__ = ["app", "main"]

# 默认模板源（国内 Gitee，访问稳定）
DEFAULT_URL = "https://gitee.com/gooker_young/coopie.git"


# ---------------------------------------------------------------------------
# copier URL 兼容 patch
# ---------------------------------------------------------------------------
# copier 9.x 的 get_repo() 仅内置 github.com / gitlab.com 两个平台前缀，
# 无法识别 Gitee、Codeup 等国内代码托管平台的 HTTPS URL。这里扩展 GIT_PREFIX，
# 并追加 gt: 简写到 REPLACEMENTS。patch 延迟到真正调用 copier 前执行。
_VCS_PATCHED = False


def _patch_copier_vcs() -> None:
    """扩展 copier 的 VCS 模块支持 Gitee / Codeup 等国内平台（幂等，可重复调用）.

    copier 在不同环境下 VCS 模块命名不同：
    - Python 3.8 + copier 9.3.x: ``copier.vcs`` （无前缀）
    - Python >=3.10 + copier 9.17+: ``copier._vcs`` （有前缀）
    用 importlib 动态导入先试 ``_vcs``，不行 fallback 到 ``vcs``。
    """
    import importlib

    try:
        vcs_mod = importlib.import_module("copier._vcs")
    except ImportError:
        vcs_mod = importlib.import_module("copier.vcs")

    extra = (
        "https://gitee.com/",
        "https://codeup.aliyun.com/",
        "https://gitlab.cn/",
        "https://gitee.cn/",
    )
    vcs_mod.GIT_PREFIX = tuple(dict.fromkeys((*vcs_mod.GIT_PREFIX, *extra)))  # pyrefly: ignore [missing-attribute]

    # copier 9.17+ 已硬编码 gh:/gl:，追加 gt: → Gitee（按 pattern 去重，避免重复调用无限膨胀）
    added = [
        (vcs_mod.re.compile(r"^gt:/?(.*\.git)$"), r"https://gitee.com/\1"),
        (vcs_mod.re.compile(r"^gt:/?(.*)$"), r"https://gitee.com/\1.git"),
    ]
    known = {(pattern.pattern, repl) for pattern, repl in vcs_mod.REPLACEMENTS}
    vcs_mod.REPLACEMENTS = [  # pyrefly: ignore [missing-attribute]
        *vcs_mod.REPLACEMENTS,
        *((pattern, repl) for pattern, repl in added if (pattern.pattern, repl) not in known),
    ]


def _ensure_copier_vcs_patched() -> None:
    """按需 patch copier VCS：延迟到真正要跑 copier 时才执行.

    patch 会触发整个 copier 包的导入（~0.9s），放在模块级会拖慢 ``--version``
    这类根本用不到 copier 的路径。copier 内部结构变化导致 patch 失败时静默降级，
    不影响主流程。
    """
    global _VCS_PATCHED  # noqa: PLW0603
    if _VCS_PATCHED:
        return
    _VCS_PATCHED = True
    with contextlib.suppress(Exception):
        _patch_copier_vcs()


def _normalize_url(url: str) -> str:
    """规范化模板 URL，确保 copier 的 get_repo() 能识别.

    - HTTPS/HTTP URL 自动补 .git 后缀（先去掉结尾斜杠，避免产生 `.../.git`）
    - SSH URL (git@...) 已自带 .git，不变
    - 本地路径 (C:/..., /path, ./...) 不变
    """
    url = url.rstrip("/")
    if url.endswith(".git"):
        return url
    if url.startswith(("https://", "http://")):
        return f"{url}.git"
    return url


def _load_answers(answers_file: Path) -> dict[str, Any]:
    """读取 copier answers 文件；文件缺失 / YAML 非法 / 非 dict 时返回空 dict."""
    import yaml

    try:
        answers = yaml.safe_load(answers_file.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    return answers if isinstance(answers, dict) else {}


def _atomic_write_text(path: Path, text: str) -> None:
    """原子写入：先落同目录临时文件再 os.replace，避免中断后留下半截文件."""
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)


def _resolve_answers_src_path(answers_file: Path) -> str:
    """读取 answers 里的 _src_path，必要时原子回写补全 .git 后缀.

    copier 首次 copy 会把 _src_path 存成去掉 .git 的形式，而其 get_repo() 又不
    识别不带 .git 的国内 HTTPS URL，导致 run_recopy 时 Template.local_abspath
    直接 Path(url) 报 "Local template must be a directory."。这里在 copier 读
    answers 之前把 _src_path 修正为带 .git 后缀的标准形式。

    返回规范化后的 _src_path；字段缺失 / 类型非字符串时返回空字符串（不回写）。
    """
    import yaml

    answers = _load_answers(answers_file)
    src = answers.get("_src_path", "")
    if not isinstance(src, str) or not src:
        return ""
    if src.endswith(".git") or not src.startswith(("https://", "http://")):
        return src

    fixed = f"{src.rstrip('/')}.git"
    answers["_src_path"] = fixed
    # 回写失败（只读/无权限）不致命：交给 copier 自己报错，避免这里抛出裸 traceback
    with contextlib.suppress(OSError, yaml.YAMLError):
        _atomic_write_text(
            answers_file,
            yaml.dump(answers, default_flow_style=False, allow_unicode=True, sort_keys=False),
        )
    return fixed


class _NoCopierUserError(Exception):
    """占位异常：copier 老版本无 UserMessageError，用于 except 兜底."""


def _user_message_error_type() -> type[Exception]:
    """返回 copier 的 UserMessageError；不可用时返回永不匹配的占位类型."""
    try:
        from copier.errors import UserMessageError
    except ImportError:
        return _NoCopierUserError
    return UserMessageError


def _warn_if_untrusted(trust: bool) -> None:
    """未显式 --trust 时提示用户：模板执行需要 copier 侧确认."""
    if not trust:
        typer.secho("提示：模板含 Jinja/任务时 copier 会请求确认，加 --trust 可跳过。", dim=True)


def _build_settings(copier_mod: Any, src_path: str, trust: bool) -> Any:
    """构造 copier Settings；未显式 --trust 或老版本无 Settings 时返回 None.

    trust 会跳过 copier 的「模板含 Jinja/_tasks，是否执行」确认，而 copier 的
    Jinja 非沙箱可执行任意代码，因此默认关闭，只在用户显式 --trust 时启用。
    """
    if not trust or not src_path or not hasattr(copier_mod, "Settings"):
        return None
    return copier_mod.Settings(trust=[src_path])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="coopie",
    help="基于 copier 的通用 Python 项目模板，提供 init/update 命令简化模板调用。",
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def _version_callback(
    version: bool = typer.Option(False, "--version", "-V", help="显示版本号并退出"),
) -> None:
    """coopie CLI."""
    if version:
        typer.echo(f"coopie {__version__}")
        raise typer.Exit


@app.command()
def init(
    destination: str = typer.Argument(..., help="目标目录路径（项目将创建在此目录）"),
    url: str = typer.Option(DEFAULT_URL, "--url", "-u", help="模板源 URL（默认 Gitee 国内源）"),
    vcs_ref: Optional[str] = typer.Option(None, "--vcs-ref", help="模板版本（git tag/branch/commit，默认最新）"),
    defaults: bool = typer.Option(False, "--defaults", help="使用默认参数，跳过交互式询问"),
    trust: bool = typer.Option(
        False,
        "--trust",
        help="信任模板源，跳过 copier 的模板执行安全确认（仅用于可信模板）",
    ),
) -> None:
    """从模板创建新项目（调用 copier copy）."""
    import copier

    _ensure_copier_vcs_patched()

    dst = Path(destination).resolve()
    template_url = _normalize_url(url)
    typer.echo(f"正在从 {template_url} 创建项目到 {dst} ...")
    _warn_if_untrusted(trust)

    kwargs: dict[str, Any] = {
        "src_path": template_url,
        "dst_path": dst,
        "vcs_ref": vcs_ref,
        "defaults": defaults,
    }
    settings = _build_settings(copier, template_url, trust)
    if settings is not None:
        kwargs["settings"] = settings

    try:
        copier.run_copy(**kwargs)
    except _user_message_error_type() as exc:
        typer.secho(f"错误：{exc}", fg="red", err=True)
        raise typer.Exit(1) from exc


@app.command()
def update(
    destination: str = typer.Argument(".", help="目标项目目录（默认当前目录）"),
    vcs_ref: Optional[str] = typer.Option(None, "--vcs-ref", help="模板版本（git tag/branch/commit，默认最新）"),
    defaults: bool = typer.Option(False, "--defaults", help="使用默认参数，跳过交互式询问"),
    trust: bool = typer.Option(
        False,
        "--trust",
        help="信任模板源，跳过 copier 的模板执行安全确认（仅用于可信模板）",
    ),
) -> None:
    """更新已有项目（调用 copier recopy）."""
    import copier

    _ensure_copier_vcs_patched()

    dst = Path(destination).resolve()
    answers_file = dst / ".copier-answers.yml"
    if not answers_file.exists():
        typer.secho(
            f"错误：{dst} 不是 copier 生成的项目（缺少 .copier-answers.yml）",
            fg="red",
            err=True,
        )
        raise typer.Exit(1)

    # 一次读取 + 解析：必要时原子回写，直接返回规范化后的模板源（供 trust 使用）
    src_path = _resolve_answers_src_path(answers_file)

    typer.echo(f"正在更新项目 {dst} ...")
    _warn_if_untrusted(trust)

    kwargs: dict[str, Any] = {
        "dst_path": dst,
        "vcs_ref": vcs_ref,
        "defaults": defaults,
    }
    settings = _build_settings(copier, src_path, trust)
    if settings is not None:
        kwargs["settings"] = settings

    try:
        copier.run_recopy(**kwargs)
    except _user_message_error_type() as exc:
        typer.secho(f"错误：{exc}", fg="red", err=True)
        raise typer.Exit(1) from exc


def main() -> None:  # pragma: no cover
    """CLI 主入口（[project.scripts] 指向此函数）."""
    app()
