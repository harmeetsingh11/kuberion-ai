"""
Hybrid retrieval combining keyword and vector search.
"""

from __future__ import annotations

from retrieval.keyword import KeywordSearch
from retrieval.retrievers.vector import VectorSearch
from retrieval.fusion import ReciprocalRankFusion


class HybridSearch:
    """
    Combines keyword and semantic retrieval.
    """

    def __init__(self):

        self.keyword = KeywordSearch()
        self.vector = VectorSearch()
        self.fusion = ReciprocalRankFusion()

    def search(
        self,
        query: str,
        limit: int = 5,
    ):

        keyword_results = self.keyword.search(
            query,
            limit=20,
        )

        vector_results = self.vector.search(
            query,
            limit=20,
        )

        results = self.fusion.fuse(
            keyword_results,
            vector_results,
        )

        unique_results = []

        seen_urls = set()

        for doc in results:

            if doc["url"] in seen_urls:
                continue

            seen_urls.add(doc["url"])

            unique_results.append(doc)

        return unique_results[:limit]


def main():

    search = HybridSearch()

    results = search.search("How do Pods communicate?")

    print()

    print(f"Results: {len(results)}\n")

    for i, result in enumerate(results, start=1):

        print(f"{i}. {result['title']}")
        print(result["url"])
        print(result["content"][:180])
        print("-" * 80)


if __name__ == "__main__":
    main()
