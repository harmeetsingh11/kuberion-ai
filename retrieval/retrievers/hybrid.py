"""
Hybrid retrieval combining keyword and vector search.
"""

from __future__ import annotations

from retrieval.keyword import KeywordSearch
from retrieval.retrievers.vector import VectorSearch


class HybridSearch:
    """
    Combines keyword and semantic retrieval.
    """

    def __init__(self):

        self.keyword = KeywordSearch()
        self.vector = VectorSearch()

    def search(
        self,
        query: str,
        limit: int = 5,
    ):

        per_retriever = limit * 2

        keyword_results = self.keyword.search(
            query,
            limit=per_retriever,
        )

        vector_results = self.vector.search(
            query,
            limit=per_retriever,
        )

        results = []

        seen_urls = set()

        keyword_index = 0
        vector_index = 0

        while len(results) < limit:

            if keyword_index < len(keyword_results):

                doc = keyword_results[keyword_index]

                keyword_index += 1

                if doc["url"] not in seen_urls:

                    seen_urls.add(doc["url"])

                    results.append(doc)

            if len(results) >= limit:
                break

            if vector_index < len(vector_results):

                doc = vector_results[vector_index]

                vector_index += 1

                if doc["url"] not in seen_urls:

                    seen_urls.add(doc["url"])

                    results.append(doc)

            if (
                keyword_index >= len(keyword_results)
                and vector_index >= len(vector_results)
            ):
                break

        return results


def main():

    search = HybridSearch()

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
