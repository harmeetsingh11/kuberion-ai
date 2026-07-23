"""
Semantic vector search using cosine similarity.
"""

from __future__ import annotations

import json

import numpy as np

from config import EMBEDDINGS_DIR
from retrieval.embedder import Embedder


class VectorSearch:
    """
    Semantic search over document embeddings.
    """

    def __init__(self):

        self.embedder = None

        self.embeddings = np.load(
            EMBEDDINGS_DIR / "embeddings.npy"
        )

        with open(
            EMBEDDINGS_DIR / "documents.json",
            encoding="utf-8",
        ) as f:

            self.documents = json.load(f)

    def search(
        self,
        query: str,
        limit: int = 5,
    ):

        if self.embedder is None:
            self.embedder = Embedder()

        query_embedding = self.embedder.embed_query(query)

        scores = np.dot(
            self.embeddings,
            query_embedding,
        )

        top_indices = np.argsort(scores)[::-1][:limit]

        results = [
            self.documents[i]
            for i in top_indices
        ]

        return results


def main():

    search = VectorSearch()

    results = search.search(
        "How do Pods communicate?"
    )

    print()

    print(f"Results: {len(results)}\n")

    for i, result in enumerate(results, start=1):

        print(f"{i}. {result['title']}")
        print(result["url"])
        print(result["content"][:180])
        print("-" * 80)


if __name__ == "__main__":
    main()
