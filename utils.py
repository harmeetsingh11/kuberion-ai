"""
Shared utility functions used across the project.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def run_command(
    command: list[str],
    cwd: Path | None = None,
) -> subprocess.CompletedProcess:
    """
    Execute a shell command.

    Args:
        command: Command as a list of arguments.
        cwd: Optional working directory.

    Returns:
        subprocess.CompletedProcess
    """

    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )
