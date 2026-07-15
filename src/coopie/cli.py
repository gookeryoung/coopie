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
import subprocess
from pathlib import Path
from typing import Optional

import typer

from coopie import __version__

__all__ = ["app", "main"]

# 默认模板源（国内 Gitee，访问稳定）
DEFAULT_URL = "https://gitee.com/gooker_young/coopie.git"

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
    cmd: list[str] = ["copier", "copy", "--trust", url, destination]
    if vcs_ref:
        cmd += ["--vcs-ref", vcs_ref]
    if defaults:
        cmd.append("--defaults")
    typer.echo(f"正在从 {url} 创建项目到 {destination} ...")
    _run_copier(cmd)


@app.command()
def update(
    destination: str = typer.Argument(".", help="目标项目目录（默认当前目录）"),
    vcs_ref: Optional[str] = typer.Option(None, "--vcs-ref", help="模板版本（git tag/branch/commit，默认最新）"),
    defaults: bool = typer.Option(False, "--defaults", help="使用默认参数，跳过交互式询问"),
) -> None:
    """更新已有项目（调用 copier recopy）."""
    dst = Path(destination).resolve()
    answers_file = dst / ".copier-answers.yml"
    if not answers_file.exists():
        typer.secho(
            f"错误：{dst} 不是 copier 生成的项目（缺少 .copier-answers.yml）",
            fg="red",
            err=True,
        )
        raise typer.Exit(1)
    cmd: list[str] = ["copier", "recopy", "--trust", str(dst)]
    if vcs_ref:
        cmd += ["--vcs-ref", vcs_ref]
    if defaults:
        cmd.append("--defaults")
    typer.echo(f"正在更新项目 {dst} ...")
    _run_copier(cmd)


def _run_copier(cmd: list[str]) -> None:
    """执行 copier 命令，处理常见错误.

    copier 内部用 ``pathlib.Path.read_text()`` 读取 ``.copier-answers.yml`` 未指定编码，
    在 Windows GBK 区域会因非 ASCII 内容（如中文描述）触发 UnicodeDecodeError。
    启用 Python UTF-8 模式（PEP 540）使子进程默认编码为 UTF-8，Linux/macOS 无影响。
    """
    env = {**os.environ, "PYTHONUTF8": "1"}
    try:
        subprocess.run(cmd, check=True, env=env)
    except FileNotFoundError as exc:
        typer.secho(
            "错误：未找到 copier 命令，请确认 copier 已安装（pip install copier）",
            fg="red",
            err=True,
        )
        raise typer.Exit(1) from exc
    except subprocess.CalledProcessError as exc:
        raise typer.Exit(exc.returncode) from exc


def main() -> None:  # pragma: no cover
    """CLI 主入口（[project.scripts] 指向此函数）."""
    app()
