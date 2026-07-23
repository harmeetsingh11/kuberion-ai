"""
Cross-encoder reranker.
"""

from __future__ import annotations

from sentence_transformers import CrossEncoder

from config import RERANKER_MODEL


class Reranker:
    """
    Re-ranks retrieved documents using a CrossEncoder.
    """

    def __init__(self):

        self.model = CrossEncoder(RERANKER_MODEL)

    def rerank(
        self,
        query: str,
        documents: list[dict],
        limit: int = 5,
    ) -> list[dict]:

        pairs = [
            (
                query,
                doc["content"],
            )
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(scores, documents),
            key=lambda x: x[0],
            reverse=True,
        )

        return [
            document
            for _, document in ranked[:limit]
        ]
