from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()


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


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Hello Personal AI"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
        "model": "qwen3:8b",
        "prompt": request.message,
        "stream": False,
        "think": False
        },
        timeout=120
    )

    data = ollama_response.json()

    return {
        "reply": data["response"]
    }