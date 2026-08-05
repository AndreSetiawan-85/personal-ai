from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.ollama import ollama_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = ollama_service.generate_response(request.message)

    return ChatResponse(reply=reply)