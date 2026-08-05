from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.chat import ChatRequest, ChatResponse
from app.models.message import Message
from app.services.agent import agent_service
from app.services.ollama import ollama_service
from app.services.streaming import StreamEvent

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
    db: Session = Depends(get_db),
):
    user_message = Message(
        role="user",
        content=request.message,
    )

    db.add(user_message)
    db.commit()

    reply = agent_service.run(request.message)

    assistant_message = Message(
        role="assistant",
        content=reply,
    )

    db.add(assistant_message)
    db.commit()

    return ChatResponse(reply=reply)


@router.get("/chat/history")
def chat_history(
    db: Session = Depends(get_db),
):
    messages = (
        db.query(Message)
        .order_by(Message.created_at)
        .all()
    )

    return messages


@router.post("/chat/stream")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    history = (
        db.query(Message)
        .order_by(Message.created_at)
        .all()
    )

    prompt = ""

    for message in history:
        prompt += (
            f"{message.role}: "
            f"{message.content}\n"
        )

    prompt += (
        f"user: {request.message}\n"
        "assistant:"
    )

    user_message = Message(
        role="user",
        content=request.message,
    )

    db.add(user_message)
    db.commit()

    def generate():

        full_response = ""

        # Status pertama
        yield StreamEvent.status("Thinking...")

        # Streaming jawaban dari Ollama
        for chunk in ollama_service.stream_response(prompt):

            full_response += chunk

            yield StreamEvent.chunk(chunk)

        assistant_message = Message(
            role="assistant",
            content=full_response,
        )

        db.add(assistant_message)
        db.commit()

        # Status selesai
        yield StreamEvent.done()

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
    )