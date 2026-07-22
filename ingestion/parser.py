"""
Parse Markdown documents and extract front matter metadata.
"""

from __future__ import annotations

from pathlib import Path

import frontmatter

from ingestion.models import RawDocument


class MarkdownParser:
    """
    Parse Kubernetes Markdown documentation into RawDocument objects.
    """

    def parse(self, file_path: Path) -> RawDocument:
        """
        Parse a Markdown file.

        Args:
            file_path: Path to the Markdown document.

        Returns:
            RawDocument
        """

        post = frontmatter.load(file_path)

        title = post.metadata.get("title", file_path.stem)

        metadata = {
            key: str(value)
            for key, value in post.metadata.items()
        }

        return RawDocument(
            source_path=file_path,
            title=title,
            content=post.content,
            metadata=metadata,
        )


def main() -> None:

    from ingestion.extractor import DocumentExtractor

    extractor = DocumentExtractor()

    parser = MarkdownParser()

    files = extractor.discover()

    document = parser.parse(files[0])

    print()

    print("Title:")
    print(document.title)

    print()

    print("Metadata Keys:")
    print(document.metadata.keys())

    print()

    print("Content Preview:")
    print(document.content[:500])


if __name__ == "__main__":
    main()
