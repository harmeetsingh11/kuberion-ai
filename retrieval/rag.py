"""
End-to-end RAG pipeline.
"""

from __future__ import annotations

from app.llm import LLM
from retrieval.keyword import KeywordSearch
from retrieval.prompt_builder import PromptBuilder


class RAGPipeline:

    def __init__(
        self,
        retriever,
    ):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm = LLM()

    def ask(
        self,
        question: str,
    ) -> str:

        documents = self.retriever.search(question)

        prompt = self.prompt_builder.build(
            question,
            documents,
        )

        answer = self.llm.ask(prompt)

        return answer
