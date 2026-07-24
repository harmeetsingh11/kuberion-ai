"""
Sentence Transformer embedder.
"""

from __future__ import annotations

from retrieval.model_registry import get_embedding_model


class Embedder:
    """
    Generates embeddings for documents and queries.
    """

    def __init__(self):
        self.model = get_embedding_model()

    def embed_documents(
        self,
        texts: list[str],
    ):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

    def embed_query(
        self,
        query: str,
    ):

        return self.model.encode(
            query,
            normalize_embeddings=True,
        )
