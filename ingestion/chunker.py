"""
Document chunking strategies.
"""

from __future__ import annotations

import uuid

from ingestion.models import (
    RawDocument,
    DocumentChunk,
)


class FixedChunker:
    """
    Fixed-size chunking.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        document: RawDocument,
    ) -> list[DocumentChunk]:

        words = document.content.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + self.chunk_size

            text = " ".join(words[start:end])

            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    title=document.title,
                    source_path=str(document.source_path),
                    section=document.title,
                    content=text,
                    metadata=document.metadata,
                )
            )

            start += self.chunk_size - self.overlap

        return chunks


def main():

    from ingestion.extractor import DocumentExtractor
    from ingestion.parser import MarkdownParser
    from ingestion.cleaner import MarkdownCleaner

    extractor = DocumentExtractor()
    parser = MarkdownParser()
    cleaner = MarkdownCleaner()
    chunker = FixedChunker()

    for file in extractor.discover():

        doc = cleaner.clean(parser.parse(file))

        if len(doc.content) > 500:

            chunks = chunker.chunk(doc)

            print()

            print(doc.title)

            print(f"{len(chunks)} chunks")

            print()

            print(chunks[0].content[:600])

            break


if __name__ == "__main__":
    main()
