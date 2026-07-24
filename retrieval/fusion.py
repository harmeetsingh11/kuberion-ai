"""
Rank fusion algorithms.
"""

from __future__ import annotations


class ReciprocalRankFusion:
    """
    Reciprocal Rank Fusion (RRF).

    score = Σ 1 / (k + rank)
    """

    def __init__(
        self,
        k: int = 60,
    ):
        self.k = k

    def fuse(
        self,
        *rankings,
    ):

        scores = {}

        documents = {}

        for ranking in rankings:

            for rank, doc in enumerate(
                ranking,
                start=1,
            ):

                doc_id = doc["id"]

                documents[doc_id] = doc

                scores.setdefault(
                    doc_id,
                    0.0,
                )

                scores[doc_id] += 1 / (self.k + rank)

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return [documents[doc_id] for doc_id, _ in ranked]
