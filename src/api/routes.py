from fastapi import APIRouter, HTTPException
from src.schemas.rag import IngestDocumentRequest, IngestResponse, QueryRequest, QueryResponse
from src.services.rag_engine import rag_engine

router = APIRouter(prefix="/rag", tags=["RAG Knowledge Engine"])


@router.post("/ingest", response_model=IngestResponse, summary="Indeksuj dokument w bazie wiedzy")
def ingest_document(payload: IngestDocumentRequest):
    try:
        chunks_count = rag_engine.ingest_document(
            title=payload.title,
            content=payload.content,
            metadata=payload.metadata
        )
        return IngestResponse(
            status="success",
            document_title=payload.title,
            chunks_indexed=chunks_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas indeksowania: {str(e)}")


@router.post("/query", response_model=QueryResponse, summary="Zadaj pytanie do bazy wiedzy")
def query_knowledge_base(payload: QueryRequest):
    try:
        result = rag_engine.answer_query(
            query=payload.query,
            top_k=payload.top_k
        )
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            model_used=result["model_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas odpowiadania: {str(e)}")
    