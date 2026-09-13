"""coopie CLI 入口.

提供 init/update 两个命令，封装 copier copy/recopy 调用，简化模板使用。

示例::

    coopie init my-project
    coopie init my-project --url https://github.com/gookeryoung/coopie.git
    coopie update                    # 在已有项目目录中执行
    coopie update /path/to/project
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

# Windows 下 copier 读 yaml 时若遇到非 ASCII 内容会因 GBK 区域触发
# UnicodeDecodeError。PEP 540 UTF-8 模式在进程启动前设置才生效，这里
# 设环境变量让后续 import copier 时能被正确识别。
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
# 无法识别 Gitee、Codeup 等国内代码托管平台的 HTTPS URL。这里在 import
# copier 后立即扩展 GIT_PREFIX，并追加 gt: 简写到 REPLACEMENTS。
def _patch_copier_vcs() -> None:
    """扩展 copier 的 VCS 模块支持 Gitee / Codeup 等国内平台.

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
    merged = tuple(dict.fromkeys((*vcs_mod.GIT_PREFIX, *extra)))
    vcs_mod.GIT_PREFIX = merged  # pyrefly: ignore [missing-attribute]

    # copier 9.17+ 已硬编码 gh:/gl:，直接追加 gt: → Gitee
    vcs_mod.REPLACEMENTS = [  # pyrefly: ignore [missing-attribute]
        *vcs_mod.REPLACEMENTS,
        (vcs_mod.re.compile(r"^gt:/?(.*\.git)$"), r"https://gitee.com/\1"),
        (vcs_mod.re.compile(r"^gt:/?(.*)$"), r"https://gitee.com/\1.git"),
    ]


_patch_copier_vcs()


def _normalize_url(url: str) -> str:
    """规范化模板 URL，确保 copier 的 get_repo() 能识别.

    - HTTPS/HTTP URL 自动补 .git 后缀
    - SSH URL (git@...) 已自带 .git，不变
    - 本地路径 (C:/..., /path, ./...) 不变
    """
    if url.endswith(".git"):
        return url
    if url.startswith(("https://", "http://")):
        return f"{url}.git"
    return url


def _ensure_answers_url_normalized(answers_file: Path) -> None:
    """确保 answers 文件里的 _src_path 能被 copier 识别.

    copier 在首次 copy 时会把 _src_path 存成规范化后的形式（去掉 .git 后缀），
    而 copier 自身的 get_repo() 又不识别不带 .git 的国内 HTTPS URL，导致
    run_recopy 时 Template.local_abspath 直接 Path(url) 报 "Local template
    must be a directory."。这里在 copier 读 answers 之前把 _src_path 修正为
    带 .git 后缀的标准形式。
    """
    import yaml

    try:
        answers = yaml.safe_load(answers_file.read_text(encoding="utf-8"))
    except Exception:
        # 读不出来就不动——让 copier 自己报错，保持行为一致
        return

    if not isinstance(answers, dict):
        return

    src = answers.get("_src_path", "")
    if src and not src.endswith(".git") and src.startswith(("https://", "http://")):
        answers["_src_path"] = f"{src}.git"
        answers_file.write_text(
            yaml.dump(answers, default_flow_style=False, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )


def _read_answers_src_path(answers_file: Path) -> str:
    """从 answers 文件读出 _src_path（纯读取，不改写）."""
    import yaml

    try:
        answers = yaml.safe_load(answers_file.read_text(encoding="utf-8"))
    except Exception:
        return ""
    if not isinstance(answers, dict):
        return ""
    return str(answers.get("_src_path", ""))


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
) -> None:
    """从模板创建新项目（调用 copier copy）."""
    import copier

    dst = Path(destination).resolve()
    template_url = _normalize_url(url)
    typer.echo(f"正在从 {template_url} 创建项目到 {dst} ...")

    kwargs: dict[str, Any] = {
        "src_path": template_url,
        "dst_path": dst,
        "vcs_ref": vcs_ref,
        "defaults": defaults,
    }
    # copier 9.17+ 引入了 Settings/trust；老版本不传此参数
    if hasattr(copier, "Settings"):
        kwargs["settings"] = copier.Settings(trust=[template_url])

    copier.run_copy(**kwargs)


@app.command()
def update(
    destination: str = typer.Argument(".", help="目标项目目录（默认当前目录）"),
    vcs_ref: Optional[str] = typer.Option(None, "--vcs-ref", help="模板版本（git tag/branch/commit，默认最新）"),
    defaults: bool = typer.Option(False, "--defaults", help="使用默认参数，跳过交互式询问"),
) -> None:
    """更新已有项目（调用 copier recopy）."""
    import copier

    dst = Path(destination).resolve()
    answers_file = dst / ".copier-answers.yml"
    if not answers_file.exists():
        typer.secho(
            f"错误：{dst} 不是 copier 生成的项目（缺少 .copier-answers.yml）",
            fg="red",
            err=True,
        )
        raise typer.Exit(1)

    # 预处理 answers 里的 _src_path，确保 URL 能被 copier 识别
    _ensure_answers_url_normalized(answers_file)

    # 从 answers 里读出模板源，用于 trust 设置
    src_path = _read_answers_src_path(answers_file)

    typer.echo(f"正在更新项目 {dst} ...")

    kwargs: dict[str, Any] = {
        "dst_path": dst,
        "vcs_ref": vcs_ref,
        "defaults": defaults,
    }
    # copier 9.17+ 引入了 Settings/trust；老版本不传此参数
    if hasattr(copier, "Settings") and src_path:
        kwargs["settings"] = copier.Settings(trust=[src_path])

    try:
        copier.run_recopy(**kwargs)
    except copier.errors.UserMessageError as exc:
        typer.secho(f"错误：{exc}", fg="red", err=True)
        raise typer.Exit(1) from exc


def main() -> None:  # pragma: no cover
    """CLI 主入口（[project.scripts] 指向此函数）."""
    app()
