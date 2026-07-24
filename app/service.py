"""
Application service layer.
"""

from __future__ import annotations

from app.models import (
    ChatResponse,
    SearchResponse,
    Source,
)
from retrieval.rag import RAGPipeline
from retrieval.retrievers.hybrid import HybridSearch
from utils import get_logger

logger = get_logger(__name__)


class RAGService:
    """
    Service exposing RAG functionality.
    """

    def __init__(self):

        self.pipeline = RAGPipeline(
            retriever=HybridSearch(),
        )

        self.search_engine = HybridSearch()

    def ask(
        self,
        question: str,
    ) -> dict:
        """
        Returns the raw pipeline output.

        Used by API, Gradio and future clients.
        """

        logger.info(
            "Chat request: %s",
            question,
        )

        result = self.pipeline.ask(
            question,
        )

        logger.info(
            "Chat request completed.",
        )

        return result

    def chat(
        self,
        question: str,
    ) -> ChatResponse:

        result = self.ask(
            question,
        )

        return ChatResponse(
            answer=result["answer"],
            sources=[
                Source(
                    title=document["title"],
                    url=document["url"],
                )
                for document in result["documents"]
            ],
        )

    def search(
        self,
        query: str,
    ) -> SearchResponse:

        logger.info(
            "Search request: %s",
            query,
        )

        documents = self.search_engine.search(
            query,
        )

        logger.info(
            "Search request completed.",
        )

        return SearchResponse(
            documents=[
                Source(
                    title=document["title"],
                    url=document["url"],
                )
                for document in documents
            ]
        )
