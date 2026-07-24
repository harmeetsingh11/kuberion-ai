from retrieval.keyword import KeywordSearch
from retrieval.prompt_builder import PromptBuilder


def main():

    search = KeywordSearch()

    docs = search.search("How do Pods communicate?")

    builder = PromptBuilder()

    prompt = builder.build(
        "How do Pods communicate?",
        docs,
    )

    print(prompt)


if __name__ == "__main__":
    main()
