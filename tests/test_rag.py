from retrieval.rag import RAGPipeline
from retrieval.keyword import KeywordSearch


def main():

    rag = RAGPipeline(
        retriever=KeywordSearch(),
    )

    answer = rag.ask(
        "How do Pods communicate?"
    )

    print()
    print(answer)


if __name__ == "__main__":
    main()
