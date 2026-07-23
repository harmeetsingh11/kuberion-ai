from retrieval.embedder import Embedder


def main():

    embedder = Embedder()

    vector = embedder.embed_query(
        "How do Pods communicate?"
    )

    print(type(vector))
    print(vector.shape)
    print(vector[:10])


if __name__ == "__main__":
    main()
