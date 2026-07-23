from app.llm import LLM


def main():

    llm = LLM()

    answer = llm.ask(
        "Reply with exactly: Groq is working."
    )

    print(answer)


if __name__ == "__main__":
    main()
