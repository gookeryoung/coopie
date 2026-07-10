from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


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


def main():
    """主函数，解析命令行参数并创建或更新项目."""
    parser = argparse.ArgumentParser(description="Create a new Python project from a template.")
    parser.add_argument(
        "project_name",
        type=str,
        nargs="?",
        help="Name of the new project.",
    )
    parser.add_argument(
        "--update",
        "-U",
        action="store_true",
        help="更新当前目录中已生成的项目模板",
    )
    args = parser.parse_args()

    if args.update:
        if args.project_name:
            parser.error("project_name 与 --update 互斥")
        cmd = [
            "uvx",
            "--with",
            "jinja2-time",
            "copier",
            "update",
            "--trust",
        ]
        subprocess.run(cmd, check=True)
        return

    if not args.project_name:
        parser.error("project_name is required")

    dest_dir = Path.cwd() / args.project_name.replace("-", "_")
    dest_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "uvx",
        "--with",
        "jinja2-time",
        "copier",
        "copy",
        "--trust",
        "--data",
        f"project_name={args.project_name}",
    ]

    author_name = _get_git_config("user.name")
    if author_name:
        cmd.extend(["--data", f"author_name={author_name}"])
    author_email = _get_git_config("user.email")
    if author_email:
        cmd.extend(["--data", f"author_email={author_email}"])

    cmd.extend(["https://github.com/gookeryoung/coopie", str(dest_dir)])
    subprocess.run(cmd, check=True)
