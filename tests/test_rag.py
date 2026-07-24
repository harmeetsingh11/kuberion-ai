from retrieval.rag import RAGPipeline
from retrieval.retrievers.hybrid import HybridSearch


def main():

    rag = RAGPipeline(
        retriever=HybridSearch(),
    )

    response = rag.ask("How do Pods communicate?")

    print()
    print(response["answer"])

    print("\nSources\n")

    for i, doc in enumerate(
        response["documents"],
        start=1,
    ):
        print(f"{i}. {doc['title']}")
        print(f"   {doc['url']}")


if __name__ == "__main__":
    main()
