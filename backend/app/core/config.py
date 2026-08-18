from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    OLLAMA_URL: str
    MODEL_NAME: str
    EMBED_MODEL_NAME: str
    DATABASE_URL: str

    WEB_SEARCH_DEFAULT_MAX_RESULTS: int
    WEB_SEARCH_DEFAULT_TRUST_SCORE: int
    WEB_SEARCH_MINIMUM_TRUST_SCORE: int

    WEB_SEARCH_TRUSTED_SOURCES: dict[str, int]
    WEB_SEARCH_CATEGORIES: dict[str, dict]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()