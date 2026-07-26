"""
Simple rule-based query rewriting.
"""

from __future__ import annotations

import re


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

    def rewrite(self, query: str) -> str:

        query = query.lower().strip()

        query = re.sub(r"[^\w\s]", "", query)

        words = []

        for word in query.split():
            words.append(self.REPLACEMENTS.get(word, word))

        return " ".join(words)
