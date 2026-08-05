import json
import requests

from app.core.config import settings

class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.MODEL_NAME

    def generate_response(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "think": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    def stream_response(self, prompt: str):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "think": False,
            },
            stream=True,
            timeout=120,
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                data = json.loads(
                    line.decode("utf-8")
                )

                if "response" in data:
                    yield data["response"]

ollama_service = OllamaService()