"""
Evaluate retrieval methods.
"""

from __future__ import annotations
from pathlib import Path
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

        found = any(expected.lower() in doc["title"].lower() for doc in results)

        if found:
            correct += 1

        print(f"{'✓' if found else '✗'} {question}")

    accuracy = correct / len(questions) * 100

    print()
    print(f"Accuracy: {accuracy:.1f}%")

    return accuracy


def main():

    with open(
        "evaluation/questions.json",
        encoding="utf-8",
    ) as f:
        questions = json.load(f)

    scores = {}

    scores["Keyword Search"] = evaluate(
        "Keyword Search",
        KeywordSearch(),
        questions,
    )

    scores["Vector Search"] = evaluate(
        "Vector Search",
        VectorSearch(),
        questions,
    )

    scores["Hybrid Search"] = evaluate(
        "Hybrid Search",
        HybridSearch(),
        questions,
    )

    scores["Hybrid + Reranker"] = evaluate(
        "Hybrid + Reranker",
        HybridSearch(),
        questions,
        reranker=Reranker(),
    )

    winner = max(scores, key=scores.get)

    print("\n" + "=" * 60)
    print("Retrieval Evaluation Summary")
    print("=" * 60)

    for method, score in scores.items():
        print(f"{method:<25} {score:.1f}%")

    print(f"\nBest Method: {winner}")

    output_dir = Path("evaluation/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    report = output_dir / "retrieval_results.md"

    with open(report, "w", encoding="utf-8") as f:

        f.write("# Retrieval Evaluation\n\n")

        f.write("| Method | Accuracy |\n")
        f.write("|--------|---------:|\n")

        for method, score in scores.items():
            f.write(f"| {method} | {score:.1f}% |\n")

        f.write("\n")

        f.write(f"**Best Retrieval Method:** {winner}\n")

    print(f"\nReport saved to: {report}")


if __name__ == "__main__":
    main()
