"""
Evaluate multiple prompt templates.
"""

from pathlib import Path

PROMPTS = [
    "baseline_prompt.txt",
    "rag_prompt.txt",
    "improved_rag_prompt.txt",
]


def main():

    print("\nPrompt Templates\n")
    print("-" * 60)

    for prompt in PROMPTS:

        path = Path("prompts") / prompt

        print(f"✓ {prompt}")

        print(f"Characters: {len(path.read_text())}")

        print()


if __name__ == "__main__":
    main()
