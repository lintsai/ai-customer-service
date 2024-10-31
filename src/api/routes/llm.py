from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from src.llm.engine import llm_engine

router = APIRouter()

class GenerateRequest(BaseModel):
    messages: List[Dict[str, str]]
    system_prompt: Optional[str] = None

class TextAnalysisRequest(BaseModel):
    text: str

@router.post("/generate")
async def generate_response(request: GenerateRequest):
    """Generate response using LLM"""
    try:
        response = await llm_engine.generate_response(
            messages=request.messages,
            system_prompt=request.system_prompt
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/sentiment")
async def analyze_sentiment(request: TextAnalysisRequest):
    """Analyze text sentiment"""
    try:
        result = await llm_engine.analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/intent")
async def detect_intent(request: TextAnalysisRequest):
    """Detect user intent"""
    try:
        result = await llm_engine.detect_intent(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))