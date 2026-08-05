from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.ollama import ollama_service
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = ollama_service.generate_response(request.message)

    return ChatResponse(reply=reply)

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        ollama_service.stream_response(request.message),
        media_type="text/plain",
    )