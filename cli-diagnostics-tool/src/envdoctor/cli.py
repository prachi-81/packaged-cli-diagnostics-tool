
import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path


def collect_diagnostics():
    """Collect environment information in a consistent structure."""

    disk = shutil.disk_usage(Path.cwd())

    tools = ["git", "python", "pip", "code"]
    tool_status = {
        name: shutil.which(name) is not None
        for name in tools
    }

    env_names = ["PATH", "HOME", "USERPROFILE"]
    env_status = {
        name: bool(os.environ.get(name))
        for name in env_names
    }

    return {
        "python_version": platform.python_version(),
        "operating_system": platform.system(),
        "disk_space": {
            "total_bytes": disk.total,
            "free_bytes": disk.free,
        },
        "environment_variables": env_status,
        "developer_tools": tool_status,
    }


def create_report(data):
    """Create a readable report from diagnostic data."""

    lines = [
        "DEVELOPER ENVIRONMENT HEALTH REPORT",
        "=" * 36,
        f"Python version: {data['python_version']}",
        f"Operating system: {data['operating_system']}",
        "",
        "Disk space:",
        f"  Total: {data['disk_space']['total_bytes']} bytes",
        f"  Free:  {data['disk_space']['free_bytes']} bytes",
        "",
        "Environment variables:",
    ]

    for name, available in data["environment_variables"].items():
        status = "Available" if available else "Missing"
        lines.append(f"  {name}: {status}")

    lines.append("")
    lines.append("Developer tools:")

    for name, available in data["developer_tools"].items():
        status = "Found" if available else "Not found"
        lines.append(f"  {name}: {status}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Check developer environment health."
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Display the report as JSON.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Save the report to a file.",
    )

    args = parser.parse_args()
    data = collect_diagnostics()

    if args.json:
        report = json.dumps(data, indent=2)
    else:
        report = create_report(data)

    print(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")
        print(f"\nReport saved to: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
