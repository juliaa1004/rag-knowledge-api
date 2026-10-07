# Enterprise RAG Knowledge Engine

Inteligentna wyszukiwarka i asystent wiedzy oparty na architekturze **RAG** (Retrieval-Augmented Generation), wykorzystujący technologie **FastAPI**, **Qdrant** oraz **Google Gemini**.

---

### Czym jest ten projekt, jaki ma cel i jak działa?

### 1. Czym to jest?
To gotowy serwis backendowy (API), który łączy bazę wiedzy Twojej firmy lub projektu z modelem sztucznej inteligencji. Pozwala zadawać pytania we własnym języku i otrzymywać precyzyjne odpowiedzi oparte wyłącznie na dostarczonych dokumentach.

### 2. Jaki ma cel?
Standardowe modele językowe (LLM) mogą "zmyślać" fakty (tzw. halucynacje) lub nie znać wewnętrznych danych Twojej firmy. 
**Główny cel tego projektu:**
* Wyeliminowanie halucynacji AI poprzez dostarczanie modelowi zweryfikowanych fragmentów tekstu jako źródła prawdy.
* Bezpieczne i szybkie przeszukiwanie tysięcy stron dokumentacji na podstawie semantyki, a nie tylko dokładnych fraz kluczowych.

### 3. Jak to działa w praktyce?
Cały proces dzieli się na dwa etapy:
1. **Wgrywanie wiedzy (Ingestia)**:
   * Wgrywasz dokumenty tekstowe do systemu.
   * Aplikacja dzieli długi tekst na mniejsze, logiczne części.
   * Model embeddingów (`gemini-embedding-001`) zamienia każdy fragment tekstu na ciąg liczb (wektor), który reprezentuje jego matematyczne znaczenie.
   * Wektory wraz z oryginalnym tekstem trafiają do bazy wektorowej **Qdrant**.

2. **Zadawanie pytań (Wyszukiwanie i Odpowiedź)**:
   * Zadajesz pytanie (np. *"Ile dni ma klient na zwrot towaru?"*).
   * Pytanie również jest zamieniane na wektor.
   * Baza **Qdrant** błyskawicznie znajduje fragmenty dokumentów o najbardziej zbliżonym znaczeniu.
   * Znalezione fragmenty wraz z pytaniem trafiają do modelu **Google Gemini**, który układa zwięzłą, precyzyjną odpowiedź, powołując się na znalezione źródła.

### Architektura i Stack Technologiczny

* **Backend API**: [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
* **Walidacja danych**: [Pydantic v2](https://docs.pydantic.dev/) + `pydantic-settings`
* **Baza wektorowa**: [Qdrant](https://qdrant.tech/) (lokalny storage osadzony na dysku)
* **Model embeddingów**: `gemini-embedding-001` (wymiarowość: 3072, metryka kosinusowa)
* **Model generatywny (LLM)**: `gemini-3.8-flash` (zoptymalizowany pod minimalne opóźnienia, `thinking_budget: 0`)

---

###  Przepływ danych (Data Flow)

1. **Ingestia (`POST /rag/ingest`)**:
   * Tekst trafia do chunkera dzielącego treść na semantyczne fragmenty.
   * Model embeddingowy generuje 3072-wymiarowe wektory dla każdego fragmentu.
   * Wektory wraz z metadanymi i fragmentami tekstu (`payload`) są zapisywane w kolekcji Qdrant.

2. **Wyszukiwanie i Generacja (`POST /rag/query`)**:
   * Pytanie użytkownika jest wektoryzowane za pomocą `gemini-embedding-001`.
   * Qdrant wyszukuje najbardziej zbliżone wektory na podstawie podobieństwa kosinusowego (*cosine similarity*).
   * Pobrane fragmenty zasilają prompt systemowy jako zweryfikowany kontekst.
   * Gemini generuje precyzyjną, ugruntowaną odpowiedź wraz z metadanymi i wskaźnikiem trafności źródeł (*similarity score*).

   ---

### Lokalne uruchomienie

1. **Sklonuj repozytorium i przejdź do katalogu projektu**:
   ```bash
   git clone <URL_REPOZYTORIUM>
   cd rag-knowledge-api

2. **Skonfiguruj środowisko wirtualne**:
   ```python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. **Uzupełnij zmienne środowiskowe:**:
   ```bash
   cp .env.example .env

5. **Uruchom serwer**:
   ```bash
   uvicorn src.main:app --reload --port 8000

   
