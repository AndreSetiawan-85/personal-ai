from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.chat import ChatRequest, ChatResponse
from app.models.message import Message
from app.services.ollama import ollama_service
from app.database import SessionLocal

from fastapi.responses import StreamingResponse


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    user_message = Message(
        role="user",
        content=request.message
    )

    db.add(user_message)
    db.commit()

    reply = ollama_service.generate_response(request.message)

    assistant_message = Message(
        role="assistant",
        content=reply
    )

    db.add(assistant_message)
    db.commit()

    return ChatResponse(reply=reply)

@router.get("/chat/history")
def chat_history(
    db: Session = Depends(get_db)
):
    messages = (
        db.query(Message)
        .order_by(Message.created_at)
        .all()
    )

    return messages

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        ollama_service.stream_response(request.message),
        media_type="text/plain",
    )