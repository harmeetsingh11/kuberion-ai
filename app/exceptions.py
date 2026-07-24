"""
Application exception handlers.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils import get_logger

logger = get_logger(__name__)


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register global exception handlers.
    """

    @app.exception_handler(Exception)
    async def handle_exception(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unhandled exception during %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error.",
            },
        )
