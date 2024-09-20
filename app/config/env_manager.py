import os
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or None
    SLACK_API_TOKEN: str = os.getenv("SLACK_API_TOKEN") or None

def get_settings() -> Settings:
    return Settings()