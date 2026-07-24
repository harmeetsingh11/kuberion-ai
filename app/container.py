"""
Application dependency container.
"""

from __future__ import annotations

from app.service import RAGService

_service: RAGService | None = None


def get_service() -> RAGService:
    """
    Return the shared RAG service instance.
    """

    global _service

    if _service is None:
        _service = RAGService()

    return _service
