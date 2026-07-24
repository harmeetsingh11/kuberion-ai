"""
Shared model registry.
"""

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder,
)

from config import (
    EMBEDDING_MODEL,
    RERANKER_MODEL,
)

_embedding_model = None
_reranker_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        print("Loading embedding model...")

        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    return _embedding_model


def get_reranker_model():

    global _reranker_model

    if _reranker_model is None:

        print("Loading reranker model...")

        _reranker_model = CrossEncoder(RERANKER_MODEL)

    return _reranker_model
