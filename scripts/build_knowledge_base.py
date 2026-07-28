"""
Build the complete knowledge base.

Runs:
1. Document ingestion
2. Embedding generation
3. Keyword index creation
"""

from ingestion.pipeline import main as ingest
from retrieval.embedding_index import main as embeddings
from retrieval.indexer import main as keyword_index


def main():

    print("=" * 60)
    print("Building Kuberion AI Knowledge Base")
    print("=" * 60)

    print("\nStep 1/3 - Processing documents")
    ingest()

    print("\nStep 2/3 - Generating embeddings")
    embeddings()

    print("\nStep 3/3 - Building keyword index")
    keyword_index()

    print("\nKnowledge base successfully built.")


if __name__ == "__main__":
    main()
