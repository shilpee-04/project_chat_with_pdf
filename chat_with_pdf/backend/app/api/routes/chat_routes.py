from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    question: str
    store_ids: List[str]
    chat_history: Optional[List[Dict]] = []
    mode: str = "multi-turn"

class ChatResponse(BaseModel):
    response: str
    context: str
    timestamp: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_pdf(request: ChatRequest):
    """Chat with uploaded PDFs"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        if not request.store_ids:
            raise HTTPException(status_code=400, detail="No document stores provided")
        
        # Get response from chat service
        response, context = chat_service.chat(
            question=request.question,
            store_ids=request.store_ids,
            chat_history=request.chat_history,
            mode=request.mode
        )
        
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        
        return ChatResponse(
            response=response,
            context=context,
            timestamp=timestamp
        )
        
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Error processing chat request")

