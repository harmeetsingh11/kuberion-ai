"""
Discover Kubernetes documentation files for ingestion.
"""

from __future__ import annotations

from pathlib import Path

from config import DOCS_REPOSITORY_DIR


class DocumentExtractor:
    """
    Discover markdown documentation files from the official
    Kubernetes documentation repository.
    """

    def __init__(self) -> None:
        self.docs_directory = (
            DOCS_REPOSITORY_DIR
            / "content"
            / "en"
            / "docs"
        )

        self.extensions = {".md", ".mdx"}

    def discover(self) -> list[Path]:
        """
        Return all supported markdown documentation files.
        """

        markdown_files: list[Path] = []

        for extension in self.extensions:
            markdown_files.extend(
                self.docs_directory.rglob(f"*{extension}")
            )

        return sorted(markdown_files)


def main() -> None:

    extractor = DocumentExtractor()

    files = extractor.discover()

    print(f"\nTotal documentation files: {len(files)}\n")

    print("First 10 files:\n")

    for file in files[:10]:
        print(file.relative_to(DOCS_REPOSITORY_DIR))


if __name__ == "__main__":
    main()
