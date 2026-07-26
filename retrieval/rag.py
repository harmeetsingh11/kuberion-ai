"""
End-to-end RAG pipeline.
"""

from __future__ import annotations

from app.llm import LLM
from retrieval.prompt_builder import PromptBuilder
from retrieval.reranker import Reranker
from retrieval.query_rewriter import QueryRewriter


class RAGPipeline:
    """
    End-to-end Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        retriever,
        prompt_file="rag_prompt.txt",
        reranker=None,
        llm=None,
    ):
        self.retriever = retriever
        self.reranker = reranker or Reranker()
        self.prompt_builder = PromptBuilder(prompt_file)
        self.llm = llm or LLM()
        self.query_rewriter = QueryRewriter()

    def ask(
        self,
        question: str,
    ) -> str:

        rewritten_question = self.query_rewriter.rewrite(question)

        documents = self.retriever.search(
            rewritten_question,
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
