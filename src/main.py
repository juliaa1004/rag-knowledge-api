from fastapi import FastAPI
from src.core.config import settings
from src.api.routes import router as rag_router

app = FastAPI(
    title="Domain RAG API",
    description="Asynchroniczny silnik wiedzy dziedzinowej z bazą wektorową Qdrant",
    version="0.1.0"
)

app.include_router(rag_router)


@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "healthy",
        "collection": settings.QDRANT_COLLECTION,
        "embedding_model": settings.EMBEDDING_MODEL
    }
