from typing import List, Optional
from pydantic import BaseModel, Field


class IngestDocumentRequest(BaseModel):
    title: str = Field(..., description="Tytuł lub nazwa dokumentu", example="Wytyczne projektowe UI/UX")
    content: str = Field(..., description="Treść dokumentu do zindeksowania")
    metadata: Optional[dict] = Field(default_factory=dict, description="Dodatkowe metadane (np. kategoria, autor)")


class IngestResponse(BaseModel):
    status: str
    document_title: str
    chunks_indexed: int


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Pytanie użytkownika", example="Czym są design tokens?")
    top_k: int = Field(default=3, ge=1, le=10, description="Liczba relewantnych fragmentów do pobrania")


class SourceReference(BaseModel):
    title: str
    text_excerpt: str
    similarity_score: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceReference]
    model_used: str
    