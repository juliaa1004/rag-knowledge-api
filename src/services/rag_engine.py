from typing import List, Dict, Any
from google import genai
from google.genai import types
from src.core.config import settings
from src.services.chunker import chunker
from src.services.embeddings import embedding_service
from src.services.vector_db import vector_db


class RAGEngine:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.completion_model = settings.COMPLETION_MODEL

    def ingest_document(self, title: str, content: str, metadata: dict = None) -> int:
        """Dzieli dokument, generuje embeddingi i zapisuje je w bazie wektorowej."""
        chunks = chunker.split_text(content)
        if not chunks:
            return 0

        vectors = embedding_service.get_embeddings_batch(chunks)
        doc_metadata = {"title": title, **(metadata or {})}
        vector_db.upsert_chunks(chunks=chunks, vectors=vectors, metadata=doc_metadata)
        return len(chunks)

    def answer_query(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Pobiera kontekst z bazy i generuje odpowiedź z Gemini."""
        query_vector = embedding_service.get_embedding(query)
        relevant_sources = vector_db.search_similar(query_vector=query_vector, top_k=top_k)

        context_parts = []
        for i, src in enumerate(relevant_sources, 1):
            context_parts.append(f"[{i}] Dokument '{src['title']}':\n{src['text_excerpt']}")
        context_text = "\n\n".join(context_parts)

        system_instruction = (
            "Jesteś precyzyjnym asystentem wiedzy dziedzinowej. Odpowiadaj wyłącznie na podstawie "
            "podanego poniżej kontekstu. Jeśli w kontekście nie ma odpowiedzi, "
            "odpowiedz wprost: 'Brak wystarczających informacji w bazie wiedzy, aby odpowiedzieć na to pytanie.' "
            "Nie wymyślaj faktów.\n\n"
            f"KONTEKST:\n{context_text}"
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )

        response = self.client.models.generate_content(
            model=self.completion_model,
            contents=query,
            config=config
        )

        return {
            "answer": response.text,
            "sources": relevant_sources,
            "model_used": self.completion_model
        }


rag_engine = RAGEngine()

