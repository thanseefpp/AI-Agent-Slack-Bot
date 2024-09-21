import os
from dotenv import load_dotenv


load_dotenv() # Load .env file

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or None
    SLACK_API_TOKEN: str = os.getenv("SLACK_API_TOKEN") or None
    SLACK_CHANNEL: str = os.getenv("SLACK_CHANNEL") or None
    EMBEDDING_MODEL: str = "text-embedding-3-small"  # Embedding model for OpenAI (lower cost model)
    ENCODING_NAME: str = "cl100k_base"  # Encoding for token counting with tiktoken
    CACHE_SIZE: int = 100
    
def get_settings() -> Settings:
    return Settings()