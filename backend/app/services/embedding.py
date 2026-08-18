import math
import requests

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.EMBED_MODEL_NAME

    def embed(self, text):
        if not text or not text.strip():
            return None

        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text.strip()
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data.get("embedding")

        except Exception as e:
            print("Embedding error:", e)
            return None

    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot = sum(x * y for x, y in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(x * x for x in vec_a))
        norm_b = math.sqrt(sum(y * y for y in vec_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)


embedding_service = EmbeddingService()
