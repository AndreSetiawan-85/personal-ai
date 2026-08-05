from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json

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

    reply = agent_service.run(
        request.message
    )

    assistant_message = Message(
        role="assistant",
        content=reply
    )

    db.add(assistant_message)
    db.commit()

    return ChatResponse(
        reply=reply
    )

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
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    user_message = Message(
        role="user",
        content=request.message
    )

    db.add(user_message)
    db.commit()

    def generate():
        full_response = ""

        try:
            for event in agent_service.run_stream(
                request.message
            ):
                try:
                    data = json.loads(event)

                    if data.get("type") == "chunk":
                        full_response += data.get(
                            "content",
                            ""
                        )

                except Exception:
                    pass

                yield event

            assistant_message = Message(
                role="assistant",
                content=full_response
            )

            db.add(assistant_message)
            db.commit()

        except Exception as e:
            yield json.dumps(
                {
                    "type": "error",
                    "message": str(e)
                }
            ) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"
    )