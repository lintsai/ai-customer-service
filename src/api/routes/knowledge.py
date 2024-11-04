from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from src.llm.engine import llm_engine

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str
    isSpecialKnowledge: bool = False

class SpecialKnowledgeRequest(BaseModel):
    messages: List[Dict[str, str]]

@router.post("/special-knowledge")
async def query_special_knowledge(request: SpecialKnowledgeRequest):
    """特殊知識查詢"""
    try:
        response = await llm_engine.generate_special_knowledge_response(
            messages=request.messages
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))