"""
Prompt builder for the RAG pipeline.
"""

from __future__ import annotations


class PromptBuilder:

    SYSTEM_PROMPT = """
You are Kuberion AI, an expert Kubernetes documentation assistant.

Answer ONLY from the provided documentation context.

If the documentation does not contain enough information, reply:

"I couldn't find that information in the Kubernetes documentation."

Do not invent facts.
""".strip()

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

        return f"""
{self.SYSTEM_PROMPT}

Question:

{question}

Documentation:

{context}

Answer:
""".strip()
