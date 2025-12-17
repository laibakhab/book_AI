import os  
from typing import Optional  
  
class Settings:  
    \"\"\" >> temp_settings_fixed.py && echo     Configuration settings for the RAG Agent Backend. >> temp_settings_fixed.py && echo     Loaded from environment variables with sensible defaults. >> temp_settings_fixed.py && echo     \"\"\"  
  
    # Qdrant Configuration  
    QDRANT_URL: str = os.getenv(\"QDRANT_URL\", \"http://localhost:6333\")  
    QDRANT_API_KEY: Optional[str] = os.getenv(\"QDRANT_API_KEY\", None)  
    QDRANT_COLLECTION: str = os.getenv(\"QDRANT_COLLECTION\", \"book_content\")  
 
    # OpenAI Configuration  
    OPENAI_API_KEY: str = os.getenv(\"OPENAI_API_KEY\", \"\")  
    OPENAI_MODEL: str = os.getenv(\"OPENAI_MODEL\", \"gpt-4-turbo\")  
  
    # Agent Configuration  
    DEFAULT_TOP_K: int = int(os.getenv(\"DEFAULT_TOP_K\", \"5\"))  
    MIN_TOP_K: int = int(os.getenv(\"MIN_TOP_K\", \"1\"))  
    MAX_TOP_K: int = int(os.getenv(\"MAX_TOP_K\", \"20\"))  
  
    # Temperature settings for response generation  
    DEFAULT_TEMPERATURE: float = float(os.getenv(\"DEFAULT_TEMPERATURE\", \"0.7\"))  
    MIN_TEMPERATURE: float = float(os.getenv(\"MIN_TEMPERATURE\", \"0.0\"))  
    MAX_TEMPERATURE: float = float(os.getenv(\"MAX_TEMPERATURE\", \"1.0\"))  
 
    # Confidence threshold for responses  
    CONFIDENCE_THRESHOLD: float = float(os.getenv(\"CONFIDENCE_THRESHOLD\", \"0.5\"))  
  
    # Maximum tokens for response generation  
    MAX_RESPONSE_TOKENS: int = int(os.getenv(\"MAX_RESPONSE_TOKENS\", \"1000\"))  
  
    # Performance settings  
    REQUEST_TIMEOUT: int = int(os.getenv(\"REQUEST_TIMEOUT\", \"30\"))  # seconds  
  
    # Validation and quality settings  
    ENABLE_CONTENT_VALIDATION: bool = os.getenv(\"ENABLE_CONTENT_VALIDATION\", \"true\").lower() == \"true\"  
    ENABLE_CITATION_CHECK: bool = os.getenv(\"ENABLE_CITATION_CHECK\", \"true\").lower() == \"true\"  
  
    def validate(self) - 
        \"\"\" >> temp_settings_fixed.py && echo         Validate that all required settings are properly configured. >> temp_settings_fixed.py && echo. >> temp_settings_fixed.py && echo         Returns: >> temp_settings_fixed.py && echo             True if all required settings are valid, False otherwise >> temp_settings_fixed.py && echo         \"\"\"  
        errors = []  
  
        # Validate required API keys are present  
        if not self.OPENAI_API_KEY:  
            errors.append(\"OPENAI_API_KEY is required\")  
  
        if not self.QDRANT_URL:  
            errors.append(\"QDRANT_URL is required\")  
  
        # Validate top_k values  
