"""
Clean parsed Markdown documents while preserving useful content.
"""

from __future__ import annotations

import re

from ingestion.models import RawDocument


class MarkdownCleaner:
    """
    Clean Markdown content before chunking.
    """

    SHORTCODE_PATTERN = re.compile(r"\{\{<.*?>\}\}|\{\{%.*?%\}\}", re.DOTALL)
    MULTIPLE_BLANK_LINES = re.compile(r"\n{3,}")
    HTML_COMMENT_PATTERN = re.compile(
        r"<!--.*?-->",
        re.DOTALL,
    )

    def clean(self, document: RawDocument) -> RawDocument:
        """
        Return a cleaned version of the document.
        """

        content = document.content

        # Remove Hugo shortcodes
        content = self.SHORTCODE_PATTERN.sub("", content)

        content = self.HTML_COMMENT_PATTERN.sub("", content)

        # Normalize line endings
        content = content.replace("\r\n", "\n")

        # Remove trailing spaces
        content = "\n".join(line.rstrip() for line in content.splitlines())

        # Collapse excessive blank lines
        content = self.MULTIPLE_BLANK_LINES.sub("\n\n", content)

        # Final trim
        content = content.strip()

        document.content = content

        return document


def main() -> None:
    from ingestion.extractor import DocumentExtractor
    from ingestion.parser import MarkdownParser

    extractor = DocumentExtractor()
    parser = MarkdownParser()
    cleaner = MarkdownCleaner()

    # Find the first document that actually contains content
    for file_path in extractor.discover():
        document = parser.parse(file_path)

        if document.content.strip():
            cleaned = cleaner.clean(document)

            print(f"\nTitle: {cleaned.title}\n")
            print("Preview:\n")
            print(cleaned.content[:1000])
            break


if __name__ == "__main__":
    main()
