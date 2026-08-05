import requests

from app.core.config import settings


class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.MODEL_NAME

    def generate_response(self, message: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": message,
                "stream": False,
                "think": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]


ollama_service = OllamaService()