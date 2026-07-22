"""
Download or update the official Kubernetes documentation repository.
"""

from __future__ import annotations

from pathlib import Path
import logging

from config import (
    RAW_DATA_DIR,
    DOCS_REPOSITORY_DIR,
    KUBERNETES_DOCS_REPO,
    DEFAULT_BRANCH,
)
from utils import run_command


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class KubernetesDocsLoader:
    """Clone or update the Kubernetes documentation repository."""

    def __init__(self) -> None:
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    def clone_or_update(self) -> Path:
        """
        Clone the repository if it does not exist,
        otherwise pull the latest changes.
        """

        if not DOCS_REPOSITORY_DIR.exists():
            logger.info("Cloning Kubernetes documentation...")

            run_command(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "--branch",
                    DEFAULT_BRANCH,
                    KUBERNETES_DOCS_REPO,
                    str(DOCS_REPOSITORY_DIR),
                ]
            )

        else:
            logger.info("Updating Kubernetes documentation...")

            run_command(
                ["git", "pull"],
                cwd=DOCS_REPOSITORY_DIR,
            )

        logger.info("Repository ready.")

        return DOCS_REPOSITORY_DIR


def main() -> None:
    loader = KubernetesDocsLoader()

    repo_path = loader.clone_or_update()

    print(f"\nRepository location:\n{repo_path}")


if __name__ == "__main__":
    main()
