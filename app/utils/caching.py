from cachetools import LRUCache
import hashlib
from app.config.env_manager import get_settings

env_settings = get_settings()

document_cache = LRUCache(maxsize=env_settings.CACHE_SIZE)

def get_cache():
    return document_cache

def get_cache_key(pdf_content: bytes) -> str:
    return hashlib.md5(pdf_content).hexdigest()