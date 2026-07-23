"""
Generate embeddings for all document chunks.
"""

from __future__ import annotations

import json

import numpy as np

from config import (
    PROCESSED_DATA_DIR,
    EMBEDDINGS_DIR,
)
from retrieval.embedder import Embedder


class EmbeddingIndexer:

    def __init__(self):

        self.embedder = Embedder()

    def build(self):

        with open(
            PROCESSED_DATA_DIR / "documents.json",
            encoding="utf-8",
        ) as f:

            documents = json.load(f)

        texts = [
            doc["content"]
            for doc in documents
        ]

        print(f"\nEmbedding {len(texts)} chunks...\n")

        embeddings = self.embedder.embed_documents(texts)

        EMBEDDINGS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        np.save(
            EMBEDDINGS_DIR / "embeddings.npy",
            embeddings,
        )

        print("\nEmbeddings saved successfully.")
        print(embeddings.shape)


def main():

    EmbeddingIndexer().build()


if __name__ == "__main__":
    main()
