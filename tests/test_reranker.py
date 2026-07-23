from retrieval.retrievers.hybrid import HybridSearch
from retrieval.reranker import Reranker


def main():

    retriever = HybridSearch()

    reranker = Reranker()

    documents = retriever.search(
        "How do Pods communicate?",
        limit=10,
    )

    ranked = reranker.rerank(
        "How do Pods communicate?",
        documents,
        limit=5,
    )

    print()

    print(f"Results: {len(ranked)}\n")

    for document in ranked:

        print(document["title"])


if __name__ == "__main__":
    main()
