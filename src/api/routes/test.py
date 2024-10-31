from fastapi import APIRouter, HTTPException
from src.db import mongodb_client, redis_client, vector_store
from src.core.config import settings
from src.llm.engine import llm_engine
from pydantic import BaseModel

router = APIRouter()

class TestMessage(BaseModel):
    message: str

@router.get("/test/mongodb")
async def test_mongodb():
    try:
        # Test MongoDB connection
        await mongodb_client.admin.command('ping')
        return {"status": "connected", "message": "MongoDB connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {str(e)}")

@router.get("/test/redis")
async def test_redis():
    try:
        # Test Redis connection
        await redis_client.set("test_key", "test_value")
        result = await redis_client.get("test_key")
        await redis_client.delete("test_key")
        return {"status": "connected", "test_value": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis connection failed: {str(e)}")

@router.get("/test/vector")
async def test_vector():
    try:
        # Test vector store connection by performing a simple operation
        test_doc = "This is a test document"
        result = vector_store.collection.query(
            query_texts=[test_doc],
            n_results=1
        )
        return {"status": "connected", "query_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector store connection failed: {str(e)}")

@router.post("/test/llm")
async def test_llm(message: TestMessage):
    """Test LLM functionality"""
    try:
        response = await llm_engine.generate_response(
            messages=[{"role": "user", "content": message.message}],
            system_prompt="You are a helpful AI assistant."
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM test failed: {str(e)}")