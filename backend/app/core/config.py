from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "AI Fisherman API"
    debug: bool = False

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Vector Store
    chroma_persist_dir: str = "./data/chroma"

    # Embedding Settings
    embedding_provider: str = "gemini"  # gemini or local
    embedding_model: str = "BAAI/bge-m3"  # local model name (when provider=local)

    # LLM Settings
    llm_provider: str = "gemini"  # openai, anthropic, or gemini
    openai_api_key: str = ""
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash-exp"

    # Content paths
    content_dir: str = "./content"

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/app.db"

    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days

    # OAuth - GitHub
    github_client_id: str = ""
    github_client_secret: str = ""

    # OAuth - Google
    google_client_id: str = ""
    google_client_secret: str = ""

    # Frontend URL (for OAuth redirect)
    frontend_url: str = "http://localhost:5173"

    # Backend URL (for OAuth callback)
    backend_url: str = "http://localhost:8000"

    @property
    def chroma_path(self) -> Path:
        return Path(self.chroma_persist_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()
