from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

# Create MongoDB client
mongodb_client = AsyncIOMotorClient(settings.MONGO_URI)

# Get database
db = mongodb_client[settings.MONGO_DB_NAME]

# Get collections
chat_collection = db[settings.CHAT_COLLECTION]
user_collection = db[settings.USER_COLLECTION]
knowledge_collection = db[settings.KNOWLEDGE_COLLECTION]

# Export all
__all__ = [
    'mongodb_client',
    'db',
    'chat_collection',
    'user_collection',
    'knowledge_collection'
]