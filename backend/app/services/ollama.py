import requests

from app.core.config import settings


def generate_response(message: str) -> str:
    response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={
            "model": settings.MODEL_NAME,
            "prompt": message,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]