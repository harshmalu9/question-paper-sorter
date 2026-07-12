# Application configuration using pydantic-settings.
# Values are read from environment variables with sensible defaults.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Question Paper Sorter API"
    API_PREFIX: str = "/api/v1"
    UPLOAD_DIR: str = "backend/uploads"
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    model_config = {
        "env_prefix": "QPS_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
