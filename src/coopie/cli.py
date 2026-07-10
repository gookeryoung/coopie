import argparse
import subprocess
from pathlib import Path


def main():
    """主函数，解析命令行参数并创建新项目."""
    parser = argparse.ArgumentParser(
        description="Create a new Python project from a template."
    )
    parser.add_argument("project_name", type=str, help="Name of the new project.")
    args = parser.parse_args()

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
        "--data", f"project_name={args.project_name}",
        "https://github.com/gookeryoung/coopie",
        str(dest_dir),
    ]
    subprocess.run(cmd)
