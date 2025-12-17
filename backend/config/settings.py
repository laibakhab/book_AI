"""
Configuration settings for the RAG retrieval pipeline testing tool.
"""

import os
from typing import Optional
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Settings:
    """Configuration settings loaded from environment variables."""

    # Cohere settings
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    COHERE_MODEL: str = os.getenv("COHERE_MODEL", "embed-multilingual-v2.0")  # Updated to match the vector dimensions of the Qdrant collection

    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "rag_embeddings")

    # Application settings
    DEFAULT_TOP_K: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    MAX_TOP_K: int = int(os.getenv("MAX_TOP_K", "100"))
    MIN_TOP_K: int = int(os.getenv("MIN_TOP_K", "1"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration values are present."""
        errors = []

        if not cls.COHERE_API_KEY:
            errors.append("COHERE_API_KEY is required")

        if not cls.QDRANT_URL:
            errors.append("QDRANT_URL is required")

        if not cls.QDRANT_API_KEY:
            errors.append("QDRANT_API_KEY is required")

        if not cls.QDRANT_COLLECTION:
            errors.append("QDRANT_COLLECTION is required")

        if cls.DEFAULT_TOP_K < cls.MIN_TOP_K or cls.DEFAULT_TOP_K > cls.MAX_TOP_K:
            errors.append(f"DEFAULT_TOP_K must be between {cls.MIN_TOP_K} and {cls.MAX_TOP_K}")

        if errors:
            for error in errors:
                print(f"Configuration error: {error}")
            return False

        return True


# Create a global instance of settings
settings = Settings()