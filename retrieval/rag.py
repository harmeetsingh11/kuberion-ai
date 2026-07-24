"""
End-to-end RAG pipeline.
"""

from __future__ import annotations

from app.llm import LLM
from retrieval.prompt_builder import PromptBuilder
from retrieval.reranker import Reranker


class RAGPipeline:
    """
    End-to-end Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        retriever,
    ):
        self.retriever = retriever
        self.reranker = Reranker()
        self.prompt_builder = PromptBuilder()
        self.llm = LLM()

    def ask(
        self,
        question: str,
    ) -> str:

        documents = self.retriever.search(
            question,
            limit=10,
        )

        documents = self.reranker.rerank(
            query=question,
            documents=documents,
            limit=5,
        )

        prompt = self.prompt_builder.build(
            question,
            documents,
        )

        answer = self.llm.ask(prompt)

        return {
            "answer": answer,
            "documents": documents,
        }
