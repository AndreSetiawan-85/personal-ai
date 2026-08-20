from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.tasks import router as tasks_router
from app.core.config import settings
from app.database import init_db
from app.models import Conversation, Message, Task, User
from app.services.task_scheduler import task_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[APP] Starting application...")

    init_db()

    print("[APP] Database initialized.")

    task_scheduler.start()

    try:
        yield
    finally:
        task_scheduler.stop()

        print("[APP] Application stopped.")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}"
    }