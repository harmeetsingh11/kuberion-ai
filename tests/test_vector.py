from retrieval.retrievers.vector import VectorSearch


def main():

    search = VectorSearch()

    results = search.search(
        "How do Pods communicate?"
    )

    print()

    print(f"Results: {len(results)}")

    print()

    print(results[0]["title"])


if __name__ == "__main__":
    main()
