"""
Prometheus metrics for Kuberion AI.
"""

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "kuberion_requests_total",
    "Total number of user questions",
)

REQUEST_LATENCY = Histogram(
    "kuberion_request_latency_seconds",
    "End-to-end request latency",
)

LLM_LATENCY = Histogram(
    "kuberion_llm_latency_seconds",
    "LLM response latency",
)

RETRIEVAL_LATENCY = Histogram(
    "kuberion_retrieval_latency_seconds",
    "Retrieval latency",
)
