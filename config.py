"""
Global project configuration.

This module defines all project paths and constants used across the
application. Keeping them in one place avoids hardcoded paths and
makes the project easier to maintain.
"""

from pathlib import Path

# ---------------------------------------------------------------------
# Project Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

EMBEDDINGS_DIR = DATA_DIR / "embeddings"
INDEXES_DIR = DATA_DIR / "indexes"

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

DOCS_REPOSITORY_DIR = RAW_DATA_DIR / "kubernetes-docs"

# ---------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------

KUBERNETES_DOCS_REPO = (
    "https://github.com/kubernetes/website.git"
)

DEFAULT_BRANCH = "main"

# ---------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K_RESULTS = 5
MAX_CONTEXT_CHUNKS = 5

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

EMBEDDING_DIMENSION = 384

TOP_K_RESULTS = 5
