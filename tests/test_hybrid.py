from retrieval.retrievers.hybrid import HybridSearch


def main():

    search = HybridSearch()

    results = search.search("How do Pods communicate?")

    print()

    print(f"Results: {len(results)}")

    print()

    for result in results:

        print(result["title"])


if __name__ == "__main__":
    main()
