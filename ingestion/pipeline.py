"""
Run the complete ingestion pipeline and save document chunks.
"""

from __future__ import annotations

import hashlib
import json

from config import PROCESSED_DATA_DIR
from ingestion.cleaner import MarkdownCleaner
from ingestion.chunkers import FixedChunker
from ingestion.extractor import DocumentExtractor
from ingestion.parser import MarkdownParser


def generate_chunk_id(source_path: str, content: str) -> str:
    """
    Generate a deterministic chunk ID.
    """
    return hashlib.sha256(
        f"{source_path}:{content}".encode("utf-8")
    ).hexdigest()[:16]


def main() -> None:
    extractor = DocumentExtractor()
    parser = MarkdownParser()
    cleaner = MarkdownCleaner()
    chunker = FixedChunker()

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output = []

    files = extractor.discover()

    for file_path in files:

        document = parser.parse(file_path)

        document = cleaner.clean(document)

        if not document.content.strip():
            continue

        chunks = chunker.chunk(document)

        for chunk in chunks:

            chunk.chunk_id = generate_chunk_id(
                chunk.source_path,
                chunk.content,
            )

            relative = chunk.source_path.split("content/en/")[-1]

            url = ("https://kubernetes.io/" +
                   relative.replace(".md", "/").replace("_index/", ""))

            output.append(
                {
                    "id": chunk.chunk_id,
                    "title": chunk.title,
                    "section": chunk.section,
                    "content": chunk.content,
                    "source": chunk.source_path,
                    "url": url,
                    "metadata": chunk.metadata,
                }
            )

    output_file = PROCESSED_DATA_DIR / "documents.json"

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nChunks created: {len(output)}")

    print(f"Saved to:\n{output_file}")


if __name__ == "__main__":
    main()
