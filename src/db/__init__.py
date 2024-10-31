from typing import Any, Dict
from src.core.config import settings

# Export database clients for easy access
from .mongodb import mongodb_client, chat_collection, user_collection, knowledge_collection
from .redis import redis_client
from .vector import vector_store

__all__ = [
    "mongodb_client",
    "chat_collection",
    "user_collection",
    "knowledge_collection",
    "redis_client",
    "vector_store"
]