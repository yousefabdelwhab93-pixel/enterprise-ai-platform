
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Enterprise AI Knowledge & Support Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Inception API
    INCEPTION_API_KEY: str = ""
    INCEPTION_MODEL: str = ""

    # Jina Embeddings
    JINA_API_KEY: str = ""
    JINA_EMBEDDING_MODEL: str = ""

    # Milvus
    MILVUS_URI: str = "http://localhost:19530"
    MILVUS_TOKEN: str = ""

    # PostgreSQL
    DATABASE_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
