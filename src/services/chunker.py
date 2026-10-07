from typing import List


class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str) -> List[str]:
        # Usunięcie zbędnych białych znaków
        cleaned_text = " ".join(text.split())
        if not cleaned_text:
            return []

        chunks = []
        start = 0
        text_len = len(cleaned_text)

        while start < text_len:
            end = start + self.chunk_size
            chunk = cleaned_text[start:end]
            chunks.append(chunk)

            if end >= text_len:
                break

            start += self.chunk_size - self.overlap

        return chunks


chunker = TextChunker()
