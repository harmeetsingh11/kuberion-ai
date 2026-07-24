"""
Pydantic request and response models.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    title: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    documents: list[Source]
