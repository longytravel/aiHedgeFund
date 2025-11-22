"""
AIHedgeFund - Configuration Management

Sprint 0: Basic settings structure
Story 1.1: Will expand with full configuration from .env
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Sprint 0: Minimal configuration
    Story 1.1: Will expand with all settings from .env.template
    """

    # Application
    app_name: str = Field(default="AIHedgeFund", description="Application name")
    app_env: str = Field(default="development", description="Environment: development, production")
    app_debug: bool = Field(default=True, description="Enable debug mode")
    app_host: str = Field(default="0.0.0.0", description="Host to bind to")
    app_port: int = Field(default=8000, description="Port to bind to")

    # Database (Story 1.2 will configure)
    postgres_user: str = Field(default="aihedgefund", description="PostgreSQL username")
    postgres_password: str = Field(default="devpassword", description="PostgreSQL password")
    postgres_db: str = Field(default="aihedgefund", description="PostgreSQL database name")
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")

    @property
    def database_url(self) -> str:
        """Construct async database URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # Redis (Story 1.7 will configure)
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_password: Optional[str] = Field(default=None, description="Redis password")
    redis_db: int = Field(default=0, description="Redis database number")

    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # LLM Configuration (Story 1.8 will configure)
    use_mock_llm: bool = Field(default=True, description="Use Mock LLM for zero-cost testing")
    llm_provider: str = Field(default="openai", description="Primary LLM provider")
    llm_model: str = Field(default="gpt-4", description="Default LLM model")

    # Security (Story 1.5 will configure)
    secret_key: str = Field(default="dev-secret-key-change-in-production", description="Secret key")

    # Logging (Story 1.6 will configure)
    log_level: str = Field(default="INFO", description="Logging level")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields in .env
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: Application settings loaded from .env

    Usage:
        from src.config import get_settings
        settings = get_settings()
        print(settings.database_url)
    """
    return Settings()


# ============================================================================
# Story 1.1 onwards will add:
# - API key validation
# - Feature flags
# - Agent configuration
# - Scheduling configuration
# - Cost tracking settings
# ============================================================================
