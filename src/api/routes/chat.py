from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from src.services.chat import chat_service

router = APIRouter()

class MessageCreate(BaseModel):
    content: str

class Message(BaseModel):
    message_id: str
    role: str
    content: str
    timestamp: datetime

class ConversationCreate(BaseModel):
    user_id: str
    initial_message: Optional[str] = None

# Routes
@router.post("/conversations")
async def create_conversation(data: ConversationCreate):
    """建立新對話"""
    try:
        conversation = await chat_service.create_conversation(data.user_id)
        
        if data.initial_message:
            response = await chat_service.generate_response(
                conversation_id=conversation["conversation_id"],
                user_message=data.initial_message
            )
            return {
                "conversation_id": conversation["conversation_id"],
                "initial_response": response.get("response")
            }
        
        return {"conversation_id": conversation["conversation_id"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"建立對話失敗：{str(e)}")

@router.post("/conversations/{conversation_id}/messages")
async def send_message(conversation_id: str, message: MessageCreate):
    """在對話中發送訊息"""
    try:
        response = await chat_service.generate_response(
            conversation_id=conversation_id,
            user_message=message.content
        )
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"發送訊息失敗：{str(e)}")

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, limit: Optional[int] = 50):
    """獲取對話歷史"""
    try:
        messages = await chat_service.get_conversation_history(
            conversation_id=conversation_id,
            limit=limit
        )
        return {"conversation_id": conversation_id, "messages": messages}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取對話歷史失敗：{str(e)}")

@router.get("/conversations")
async def get_active_conversations(user_id: str):
    """獲取用戶的所有進行中對話"""
    try:
        conversations = await chat_service.get_active_conversations(user_id)
        return {"conversations": conversations}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取對話列表失敗：{str(e)}")

@router.delete("/conversations/{conversation_id}")
async def end_conversation(conversation_id: str):
    """結束/封存對話"""
    try:
        result = await chat_service.end_conversation(conversation_id)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"結束對話失敗：{str(e)}")