from fastapi import APIRouter
from fastapi import HTTPException
from config.settings import settings
from models.chat_request import ChatRequestModel
from models.chat_response import ChatResponse
from services.chat_service import ChatService

chat_router=APIRouter(prefix="/chat")

chat_service=ChatService()

@chat_router.post("")
def sales_chat(req:ChatRequestModel):
    ai_reply=chat_service.ai_chat(req)
    return ChatResponse(ai_reply=ai_reply)