"""
Keyword search using minsearch.
"""

from __future__ import annotations

import json

import minsearch

from config import PROCESSED_DATA_DIR


class KeywordSearch:

    def __init__(self):

        self.index = minsearch.Index(
            text_fields=[
                "title",
                "section",
                "content",
            ],
            keyword_fields=[
                "source",
            ],
        )

        with open(
            PROCESSED_DATA_DIR / "documents.json",
            encoding="utf-8",
        ) as f:

            self.documents = json.load(f)

        self.index.fit(self.documents)

    def search(
        self,
        query: str,
        limit: int = 5,
    ):

        return self.index.search(
            query=query,
            num_results=limit,
        )


def main():

    search = KeywordSearch()

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
