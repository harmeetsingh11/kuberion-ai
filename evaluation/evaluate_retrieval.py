"""
Evaluate retrieval methods.
"""

from __future__ import annotations

import json

from retrieval.keyword import KeywordSearch
from retrieval.reranker import Reranker
from retrieval.retrievers.hybrid import HybridSearch
from retrieval.retrievers.vector import VectorSearch


def evaluate(name, retriever, questions, reranker=None):

    print(f"\n{name}")
    print("-" * 60)

    correct = 0

    for item in questions:
        question = item["question"]
        expected = item["expected"]

        results = retriever.search(
            question,
            limit=5,
        )

        if reranker is not None:
            results = reranker.rerank(
                question,
                results,
                limit=5,
            )

        found = any(expected.lower()
                    in doc["title"].lower() for doc in results)

        if found:
            correct += 1

        print(f"{'✓' if found else '✗'} {question}")

    accuracy = correct / len(questions) * 100

    print()
    print(f"Accuracy: {accuracy:.1f}%")


def main():

    with open(
        "evaluation/questions.json",
        encoding="utf-8",
    ) as f:
        questions = json.load(f)

    evaluate(
        "Keyword Search",
        KeywordSearch(),
        questions,
    )

    evaluate(
        "Vector Search",
        VectorSearch(),
        questions,
    )

    evaluate(
        "Hybrid Search",
        HybridSearch(),
        questions,
    )

    evaluate(
        "Hybrid + Reranker",
        HybridSearch(),
        questions,
        reranker=Reranker(),
    )


if __name__ == "__main__":
    main()
