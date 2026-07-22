from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RawDocument:
    """Raw markdown document."""

    source_path: Path
    title: str
    content: str
    metadata: dict[str, str]


@dataclass(slots=True)
class DocumentChunk:
    """
   Chunk ready for indexing.
    """

    chunk_id: str

    title: str

    source_path: str

    section: str

    content: str

    metadata: dict[str, str]
