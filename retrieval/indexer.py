"""
Build a keyword search index using minsearch.
"""

from __future__ import annotations

import json

from config import PROCESSED_DATA_DIR
import minsearch


INDEX_FIELDS = [
    "title",
    "section",
    "content",
]


class KeywordIndexer:
    def __init__(self):
        self.index = minsearch.Index(
            text_fields=INDEX_FIELDS,
            keyword_fields=["source"],
        )

    def load_documents(self):

        file = PROCESSED_DATA_DIR / "documents.json"

        with open(file, encoding="utf-8") as f:
            return json.load(f)

    def build(self):

        documents = self.load_documents()

        self.index.fit(documents)

        return self.index


def main():

    indexer = KeywordIndexer()
    index = indexer.build()
    print()
    print(f"Indexed {len(index.docs)} chunks.")


if __name__ == "__main__":
    main()
