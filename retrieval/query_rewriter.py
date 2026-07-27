"""
Rule-based and LLM-based query rewriting.
"""

from __future__ import annotations

import re

from app.llm import LLM


class QueryRewriter:

    REPLACEMENTS = {
        "app": "application",
        "apps": "applications",
        "deployments": "deployment",
        "services": "service",
        "config": "configuration",
        "configs": "configuration",
        "secret": "secrets",
        "volume": "persistent volume",
        "volumes": "persistent volumes",
        "storage": "persistent storage",
        "networking": "network",
        "lb": "load balancer",
        "svc": "service",
        "k8s": "kubernetes",
    }

    def __init__(self, strategy: str = "rule"):

        self.strategy = strategy

        if strategy == "llm":
            self.llm = LLM()

    def rewrite(self, query: str) -> str:

        if self.strategy == "llm":
            return self._rewrite_llm(query)

        return self._rewrite_rule(query)

    def _rewrite_rule(self, query: str) -> str:

        query = query.lower().strip()

        query = re.sub(r"[^\w\s]", "", query)

        words = []

        for word in query.split():
            words.append(self.REPLACEMENTS.get(word, word))

        return " ".join(words)

    def _rewrite_llm(self, query: str) -> str:

        prompt = f"""
Rewrite the user's question so it is better for retrieving Kubernetes documentation.

Rules:
- Preserve the original meaning.
- Expand abbreviations.
- Use Kubernetes terminology.
- Return ONLY the rewritten query.
- Do not explain anything.

Question:
{query}
"""

        rewritten = self.llm.ask(prompt)

        return rewritten.strip()
