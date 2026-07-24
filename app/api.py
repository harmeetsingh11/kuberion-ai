"""
FastAPI application.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from app.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    SearchRequest,
    SearchResponse,
)
from app.container import get_service
import time

from fastapi import Request

from utils import get_logger

app = FastAPI(
    title="Kuberion AI",
    description="Production-ready Retrieval-Augmented Generation (RAG) assistant for Kubernetes documentation.",
    version="1.0.0",
    contact={
        "name": "Harmeet Singh",
    },
    license_info={
        "name": "MIT",
    },
)

register_exception_handlers(app)
logger = get_logger(__name__)


@app.middleware("http")
async def log_request_time(
    request: Request,
    call_next,
):

    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    logger.info(
        "%s %s completed in %.2f seconds",
        request.method,
        request.url.path,
        duration,
    )

    return response


service = get_service()


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health Check",
)
def health():

    return HealthResponse(
        status="ok",
    )


@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["RAG"],
    summary="Ask Kubernetes Questions",
)
def chat(
    request: ChatRequest,
):

    return service.chat(
        request.question,
    )


@app.post(
    "/search",
    response_model=SearchResponse,
    tags=["Search"],
    summary="Hybrid Document Search",
)
def search(
    request: SearchRequest,
):

    return service.search(
        request.query,
    )
