from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.chat import ChatRequest, ChatResponse
from app.models.message import Message
from app.services.agent import agent_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    user_message = request.message

    reply = agent_service.run(
        user_message
    )

    user_db = Message(
        role="user",
        content=user_message
    )

    assistant_db = Message(
        role="assistant",
        content=reply
    )

    db.add(user_db)
    db.add(assistant_db)
    db.commit()

    return {
        "reply": reply
    }