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
    """Chunk ready for indexing."""

    chunk_id: str
    source_path: str
    title: str
    section: str
    content: str
