"""
Fixed-size chunking strategy.
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
