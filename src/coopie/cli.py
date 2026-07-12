from __future__ import annotations

import argparse
import os
import subprocess
import sys
import typing
from pathlib import Path

from coopie import __version__

_DEFAULT_TEMPLATE_REPO = "https://gitee.com/gooker_young/coopie.git"
_TEMPLATE_ENV_VAR = "COOPIE_TEMPLATE_REPO"
_COPIER_TIMEOUT = 600  # 秒，copier copy/update 超时阈值


def _get_git_config(key: str) -> str | None:
    """从 git 配置中查询指定键的值，查不到时返回 None."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return None
    value = result.stdout.strip()
    return value or None


def _resolve_template_repo(cli_value: str | None) -> str:
    """解析模板源：--template 优先，其次环境变量，最后默认 GitHub 仓库."""
    if cli_value:
        return cli_value
    env_value = os.environ.get(_TEMPLATE_ENV_VAR)
    if env_value:
        return env_value
    return _DEFAULT_TEMPLATE_REPO


def _build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器，返回 argparse.ArgumentParser 对象."""
    parser = argparse.ArgumentParser(
        prog="coopie",
        description="基于 copier 的通用 Python 项目模板工具。",
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    template_help = f"模板源（URL 或本地路径）；不指定则读环境变量 {_TEMPLATE_ENV_VAR}，再退回默认仓库"

    new_parser = subparsers.add_parser("new", help="新建项目（建立子文件夹）")
    new_parser.add_argument("project_name", type=str, help="项目名称")
    new_parser.add_argument(
        "--type",
        dest="project_type",
        choices=["library", "cli", "gui", "web"],
        default=None,
        help="项目类型（不指定则交互选择）",
    )
    new_parser.add_argument("--template", dest="template", default=None, help=template_help)

    init_parser = subparsers.add_parser("init", help="在当前目录初始化项目")
    init_parser.add_argument(
        "--type",
        dest="project_type",
        choices=["library", "cli", "gui", "web"],
        default=None,
        help="项目类型（不指定则交互选择）",
    )
    init_parser.add_argument("--template", dest="template", default=None, help=template_help)

    update_parser = subparsers.add_parser("update", help="更新当前目录中的已生成项目模板")
    update_parser.add_argument("-A", "--skip-answered", action="store_true", help="跳过所有问题")
    update_parser.add_argument("-T", "--skip-tasks", action="store_true", help="跳过所有任务")

    test_parser = subparsers.add_parser("test", help="模拟检查模板更新是否产生冲突")
    test_parser.add_argument("-A", "--skip-answered", action="store_true", help="跳过所有问题")
    test_parser.add_argument("-T", "--skip-tasks", action="store_true", help="跳过所有任务")

    return parser


def _append_author_data(cmd: list[str]) -> None:
    """从 git 配置读取作者信息并追加到命令列表."""
    author_name = _get_git_config("user.name")
    if author_name:
        cmd.extend(["--data", f"author_name={author_name}"])
    author_email = _get_git_config("user.email")
    if author_email:
        cmd.extend(["--data", f"author_email={author_email}"])


def _is_directory_nonempty(path: Path) -> bool:
    """检查目录是否包含非 .git 的文件或子目录."""
    return any(entry.name != ".git" for entry in path.iterdir())


def _run_copier(cmd: list[str]) -> None:
    """执行 copier 子命令，静默 uv 的 INFO 级日志并加超时保护.

    覆盖 RUST_LOG=warning 避免父进程的 RUST_LOG=info 让 uv 输出大量 PubGrub 解析日志。
    超时（由 _COPIER_TIMEOUT 控制）后提示用户检查网络或用 --template 指定本地/镜像源。
    """
    env = {**os.environ, "RUST_LOG": "warning"}
    try:
        subprocess.run(cmd, check=True, timeout=_COPIER_TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        print(
            f"\n命令执行超时（{_COPIER_TIMEOUT} 秒），可能是网络问题导致拉取模板仓库缓慢。\n"
            f"可通过 --template 指定本地路径或镜像源，或设置环境变量 {_TEMPLATE_ENV_VAR}=<url>。",
            file=sys.stderr,
        )
        sys.exit(1)


def _run_new(args: argparse.Namespace) -> None:
    """新建项目到子目录."""
    dest_dir = Path.cwd() / args.project_name.replace("-", "_")
    dest_dir.mkdir(parents=True, exist_ok=True)

    template_repo = _resolve_template_repo(args.template)
    cmd: list[str] = ["uvx", "copier", "copy", "--data", f"project_name={args.project_name}"]
    if args.project_type:
        cmd.extend(["--data", f"project_type={args.project_type}"])
    _append_author_data(cmd)
    cmd.extend([template_repo, str(dest_dir)])
    _run_copier(cmd)


def _run_init(args: argparse.Namespace) -> None:
    """在当前目录初始化项目."""
    cwd = Path.cwd()
    if _is_directory_nonempty(cwd):
        response = input("当前目录非空，继续初始化可能覆盖已有文件。是否继续？[y/N] ")
        if response.lower() != "y":
            print("已取消初始化。")
            return

    project_name = cwd.name
    template_repo = _resolve_template_repo(args.template)
    cmd: list[str] = ["uvx", "copier", "copy", "--data", f"project_name={project_name}"]
    if args.project_type:
        cmd.extend(["--data", f"project_type={args.project_type}"])
    _append_author_data(cmd)
    cmd.extend([template_repo, "."])
    _run_copier(cmd)


def _run_update(args: argparse.Namespace) -> None:
    """更新当前目录中的已生成项目模板."""
    cmd: list[str] = ["uvx", "copier", "update"]
    if args.skip_answered:
        cmd.append("--skip-answered")
    if args.skip_tasks:
        cmd.append("--skip-tasks")
    _run_copier(cmd)


def _run_test(args: argparse.Namespace) -> None:
    """模拟检查模板更新是否产生冲突."""
    cmd: list[str] = ["uvx", "copier", "update", "--pretend"]
    if args.skip_answered:
        cmd.append("--skip-answered")
    if args.skip_tasks:
        cmd.append("--skip-tasks")
    _run_copier(cmd)


_COMMAND_DISPATCH: dict[str, typing.Callable[[argparse.Namespace], None]] = {
    "new": _run_new,
    "init": _run_init,
    "update": _run_update,
    "test": _run_test,
}


def main() -> None:
    """主函数，解析命令行参数并执行对应子命令."""
    parser = _build_parser()
    args = parser.parse_args()

    assert args.command is not None  # required=True 保证

    handler = _COMMAND_DISPATCH[args.command]
    try:
        handler(args)
    except subprocess.CalledProcessError as exc:
        print(f"\n命令执行失败（退出码 {exc.returncode}），请查看上方 copier 输出的错误信息。", file=sys.stderr)
        sys.exit(exc.returncode)
