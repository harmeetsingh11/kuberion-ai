"""
Shared utility functions used across the project.
"""

from __future__ import annotations

import logging
import subprocess
import sys
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


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Returns a configured logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger
