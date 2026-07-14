from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import typing
from pathlib import Path

from coopie import __version__

_DEFAULT_TEMPLATE_REPO = "https://gitee.com/gooker_young/coopie.git"
_TEMPLATE_ENV_VAR = "COOPIE_TEMPLATE_REPO"
_COPIER_TIMEOUT = 600  # 秒，copier copy/update 超时阈值

# 历史标签 v0.3.0 ~ v0.7.1 的模板含文件名带双引号的 rule-12 文件，
# Windows 文件系统不允许文件名含双引号，导致 copier update 无法检出这些标签。
# v0.7.2 起该文件已移除，是可正常检出的最早版本。
_BROKEN_COMMIT_MIN = (0, 3, 0)
_BROKEN_COMMIT_MAX = (0, 7, 1)
_FALLBACK_COMMIT = "v0.7.2"


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
    """解析模板源：--template 优先，其次环境变量，最后默认 Gitee 仓库."""
    if cli_value:
        return cli_value
    env_value = os.environ.get(_TEMPLATE_ENV_VAR)
    if env_value:
        return env_value
    return _DEFAULT_TEMPLATE_REPO


def _parse_version(version: str) -> tuple[int, int, int] | None:
    """解析版本号字符串（如 'v0.4.2'）为整数元组（如 (0, 4, 2)），无法解析时返回 None."""
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", version.strip())
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def _patch_broken_answers_commit() -> bool:
    """检查并修补 .copier-answers.yml 中指向不可检出标签的 _commit 字段.

    历史标签 v0.3.0 ~ v0.7.1 含文件名带双引号的 rule-12 文件，Windows 无法检出。
    若检测到 _commit 落在该范围，自动升级到 _FALLBACK_COMMIT（v0.7.2）。
    返回 True 表示已修补，False 表示无需修补或文件不存在。
    """
    answers_file = Path.cwd() / ".copier-answers.yml"
    if not answers_file.is_file():
        return False
    content = answers_file.read_text(encoding="utf-8")
    match = re.search(r"^_commit:\s*(.+)$", content, re.MULTILINE)
    if not match:
        return False
    commit_value = match.group(1).strip()
    version = _parse_version(commit_value)
    if version is None:
        return False
    if not (_BROKEN_COMMIT_MIN <= version <= _BROKEN_COMMIT_MAX):
        return False
    new_content = re.sub(
        r"^_commit:\s*.+$",
        f"_commit: {_FALLBACK_COMMIT}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    answers_file.write_text(new_content, encoding="utf-8")
    print(
        f"检测到模板版本 {commit_value} 在 Windows 上无法检出（含非法文件名），"
        f"已自动将 .copier-answers.yml 的 _commit 升级到 {_FALLBACK_COMMIT}。",
        file=sys.stderr,
    )
    return True


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
    设置 core.quotePath=false 避免 git 转义非 ASCII 文件名，导致 copier 在 Windows 上
    因路径编码错误（WinError 123）无法更新含中文文件名的模板文件。
    """
    env = {
        **os.environ,
        "RUST_LOG": "warning",
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.quotePath",
        "GIT_CONFIG_VALUE_0": "false",
    }
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
    _patch_broken_answers_commit()
    cmd: list[str] = ["uvx", "copier", "update"]
    if args.skip_answered:
        cmd.append("--skip-answered")
    if args.skip_tasks:
        cmd.append("--skip-tasks")
    _run_copier(cmd)


def _run_test(args: argparse.Namespace) -> None:
    """模拟检查模板更新是否产生冲突."""
    _patch_broken_answers_commit()
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
