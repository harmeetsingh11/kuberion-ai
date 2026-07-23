from retrieval.rag import RAGPipeline
from retrieval.retrievers.hybrid import HybridSearch


def main():

    rag = RAGPipeline(
        retriever=HybridSearch(),
    )

    answer = rag.ask(
        "How do Pods communicate?"
    )

    print()
    print(answer)


if __name__ == "__main__":
    main()
