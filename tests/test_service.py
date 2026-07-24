from app.service import RAGService


def main():

    service = RAGService()

    response = service.chat("How do Pods communicate?")

    print()

    print(response.answer)

    print()

    print("Sources:\n")

    for source in response.sources:

        print(source.title)
        print(source.url)
        print()


if __name__ == "__main__":
    main()
