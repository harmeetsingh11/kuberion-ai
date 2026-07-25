from pathlib import Path


class PromptBuilder:

    def __init__(self, prompt_file: str = "rag_prompt.txt"):

        prompt_path = Path(__file__).parent.parent / "prompts" / prompt_file

        self.template = prompt_path.read_text(encoding="utf-8")

    def build(
        self,
        question: str,
        documents: list[dict],
    ) -> str:

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += f"""
### Document {i}

Title: {doc["title"]}

Section: {doc["section"]}

Content:
{doc["content"]}

Source:
{doc["url"]}

"""

        return self.template.format(
            question=question,
            context=context,
        )
