"""
Cross-encoder reranker.
"""

from __future__ import annotations
from retrieval.model_registry import get_reranker_model


class Reranker:
    """
    Re-ranks retrieved documents using a CrossEncoder.
    """

    def __init__(self):

        self.model = get_reranker_model()

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

        return [document for _, document in ranked[:limit]]
