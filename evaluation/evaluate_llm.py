"""
Compare multiple prompt templates.
"""

from __future__ import annotations
from groq import RateLimitError
import json
import time
from pathlib import Path

from retrieval.rag import RAGPipeline
from retrieval.retrievers.hybrid import HybridSearch

PROMPTS = [
    "baseline_prompt.txt",
    "rag_prompt.txt",
    "improved_rag_prompt.txt",
]


def evaluate_prompt(prompt_file, questions):

    rag = RAGPipeline(
        HybridSearch(),
        prompt_file=prompt_file,
    )

    latency = []
    hallucinations = 0
    answer_lengths = []
    source_counts = []

    print(f"\n{prompt_file}")
    print("-" * 70)

    for item in questions:

        question = item["question"]
        expected_found = item["expected_found"]

        start = time.perf_counter()

        try:
            response = rag.ask(question)
        except RateLimitError:
            print("\nGroq daily token limit reached.")
            print(f"Stopped evaluation for: {prompt_file}")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break

        elapsed = time.perf_counter() - start

        answer = response["answer"]

        docs = response["documents"]

        latency.append(elapsed)

        answer_lengths.append(len(answer.split()))

        source_counts.append(len(docs))

        fallback = "I couldn't find that information in the Kubernetes documentation."

        passed = (not expected_found and fallback in answer) or (
            expected_found and fallback not in answer
        )

        if passed:
            hallucinations += 1

        print(
            f"{question[:40]:40}"
            f"{elapsed:7.2f}s"
            f"{len(docs):4}"
            f"{'PASS' if passed else 'FAIL':>8}"
        )
    if not latency:
        return {
            "prompt": prompt_file,
            "latency": 0,
            "answer_length": 0,
            "sources": 0,
            "hallucinations": 0,
        }
    return {
        "prompt": prompt_file,
        "latency": sum(latency) / len(latency),
        "answer_length": sum(answer_lengths) / len(answer_lengths),
        "sources": sum(source_counts) / len(source_counts),
        "hallucinations": hallucinations,
    }


def save_report(results):

    Path("evaluation/results").mkdir(
        parents=True,
        exist_ok=True,
    )

    report = "# LLM Prompt Evaluation\n\n"

    report += (
        "| Prompt | Avg Latency (s) | Avg Words | "
        "Avg Sources | Hallucination Pass |\n"
    )

    report += (
        "|--------|----------------:|----------:|-------------:|------------------:|\n"
    )

    total_questions = 10

    for r in results:

        report += (
            f"| {r['prompt']} "
            f"| {r['latency']:.2f} "
            f"| {r['answer_length']:.0f} "
            f"| {r['sources']:.1f} "
            f"| {r['hallucinations']}/{total_questions} |\n"
        )

    best = max(
        results,
        key=lambda x: (
            x["hallucinations"],
            -x["latency"],
        ),
    )

    report += "\n"
    report += f"**Best Prompt:** `{best['prompt']}`\n"

    output = Path("evaluation/results/llm_prompt_comparison.md")

    output.write_text(
        report,
        encoding="utf-8",
    )

    print("\n")
    print("=" * 70)

    for r in results:

        print(
            f"{r['prompt']:30}"
            f"{r['latency']:7.2f}s   "
            f"{r['hallucinations']}/{total_questions}"
        )

    print("\nBest Prompt:", best["prompt"])
    print("Report saved to:", output)


def main():

    with open(
        "evaluation/llm_questions.json",
        encoding="utf-8",
    ) as f:

        questions = json.load(f)

    results = []

    for prompt in PROMPTS:

        results.append(
            evaluate_prompt(
                prompt,
                questions,
            )
        )

    save_report(results)


if __name__ == "__main__":
    main()
