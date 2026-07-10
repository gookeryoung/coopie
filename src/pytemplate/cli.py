import argparse
import subprocess
from pathlib import Path


def main():
    """主函数，解析命令行参数并创建新项目."""
    parser = argparse.ArgumentParser(
        description="Create a new Python project from a template."
    )
    parser.add_argument("project_name", type=str, help="Name of the new project.")
    parser.add_argument(
        "dest", type=str, default=".", help="Destination directory for the new project."
    )
    args = parser.parse_args()

    if not args.project_name:
        parser.error("project_name is required")

    if not args.dest:
        parser.error("dest is required")

    cmd = [
        "uvx",
        "copier",
        "copy",
        "https://github.com/gookeryoung/pytemplate",
        args.project_name,
        Path(args.dest),
    ]
    subprocess.run(cmd)
