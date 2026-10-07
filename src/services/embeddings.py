from typing import List
from google import genai
from src.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.EMBEDDING_MODEL

    def get_embedding(self, text: str) -> List[float]:
        """Generuje wektor dla pojedynczego zapytania."""
        clean_text = text.replace("\n", " ")
        response = self.client.models.embed_content(
            model=self.model,
            contents=clean_text
        )
        return response.embeddings[0].values

    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generuje wektory dla listy fragmentów dokumentu."""
        if not texts:
            return []
        
        cleaned_texts = [t.replace("\n", " ") for t in texts]
        response = self.client.models.embed_content(
            model=self.model,
            contents=cleaned_texts
        )
        return [e.values for e in response.embeddings]


embedding_service = EmbeddingService()