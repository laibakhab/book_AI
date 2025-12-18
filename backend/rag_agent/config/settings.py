import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "book_content")

settings = type('Settings', (object,), {
    'OPENAI_API_KEY': OPENAI_API_KEY,
    'OPENAI_MODEL': OPENAI_MODEL,
    'QDRANT_URL': QDRANT_URL,
    'QDRANT_API_KEY': QDRANT_API_KEY,
    'QDRANT_COLLECTION': QDRANT_COLLECTION
})
