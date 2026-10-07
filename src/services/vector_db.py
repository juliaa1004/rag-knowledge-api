from typing import List, Dict, Any
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from src.core.config import settings


class VectorDBService:
    def __init__(self):
        # Inicjalizacja lokalnej bazy Qdrant na dysku
        self.client = QdrantClient(path="data/qdrant_storage")
        self.collection_name = settings.QDRANT_COLLECTION
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )

    def upsert_chunks(self, chunks: List[str], vectors: List[List[float]], metadata: dict = None) -> None:
        points = []
        meta = metadata or {}
        for chunk, vector in zip(chunks, vectors):
            point_id = str(uuid.uuid4())
            payload = {
                "text": chunk,
                **meta
            }
            points.append(PointStruct(id=point_id, vector=vector, payload=payload))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search_similar(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        # Nowe wersje qdrant-client używają query_points
        if hasattr(self.client, "query_points"):
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=top_k
            )
            points = response.points
        else:
            # Fallback dla starszych wersji
            points = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )

        results = []
        for point in points:
            results.append({
                "title": point.payload.get("title", "Brak tytułu"),
                "text_excerpt": point.payload.get("text", ""),
                "similarity_score": round(float(point.score), 4)
            })
        return results


vector_db = VectorDBService()