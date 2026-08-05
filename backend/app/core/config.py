import os


class Settings:
    APP_NAME: str = "Personal AI"

    OLLAMA_URL: str = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )

    MODEL_NAME: str = os.getenv(
        "MODEL_NAME",
        "qwen3:8b"
    )


settings = Settings()