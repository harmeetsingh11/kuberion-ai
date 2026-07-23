"""
Sentence Transformer embedder.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class Embedder:
    """
    Generates embeddings for documents and queries.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
    ):
        self.model = SentenceTransformer(model_name)

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
