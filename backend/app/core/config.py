"""
Application configuration management.

This module handles loading configuration from environment variables,
YAML files, and provides validated configuration objects for the application.
"""

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables can be set in .env file or system environment.
    """

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/aihedgefund",
        description="PostgreSQL connection URL"
    )

    # API Keys
    eodhd_api_key: Optional[str] = Field(
        default=None,
        description="EODHD API key for financial data"
    )
    alpha_vantage_api_key: Optional[str] = Field(
        default=None,
        description="Alpha Vantage API key for emergency fallback"
    )

    # LLM Provider API Keys
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key"
    )
    google_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API key"
    )

    # Application Settings
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # Project Paths
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent.parent,
        description="Project root directory"
    )

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from .env (docker-compose vars)


class DataSourcesConfig:
    """
    Data sources configuration loaded from YAML file.

    Handles:
    - Provider enable/disable
    - Priority ordering
    - API key substitution from environment variables
    - Failover settings
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize data sources configuration.

        Args:
            config_path: Path to data_sources.yaml file.
                        If None, uses default config/data_sources.yaml
        """
        if config_path is None:
            # Default to config/data_sources.yaml in project root
            project_root = Path(__file__).parent.parent.parent.parent
            config_path = project_root / "config" / "data_sources.yaml"

        self.config_path = config_path
        self._raw_config: Dict[str, Any] = {}
        self.providers: Dict[str, Dict[str, Any]] = {}
        self.failover: Dict[str, Any] = {}
        self.primary_provider: Optional[str] = None
        self.priority_order: list[str] = []

        self._load_config()

    def _load_config(self) -> None:
        """Load and parse YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Data sources config not found: {self.config_path}"
            )

        with open(self.config_path, 'r') as f:
            self._raw_config = yaml.safe_load(f)

        # Extract primary provider
        self.primary_provider = self._raw_config.get("primary_fundamental_provider")

        # Load provider configurations
        providers_config = self._raw_config.get("providers", {})
        for provider_name, provider_config in providers_config.items():
            # Substitute environment variables in API keys
            processed_config = self._substitute_env_vars(provider_config.copy())
            self.providers[provider_name] = processed_config

        # Load failover configuration
        self.failover = self._raw_config.get("failover", {})

        # Build priority order (sorted by priority field)
        self._build_priority_order()

    def _substitute_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Substitute environment variable placeholders in config.

        Converts ${VAR_NAME} to the value of os.environ['VAR_NAME'].

        Args:
            config: Configuration dictionary

        Returns:
            Configuration with environment variables substituted
        """
        for key, value in config.items():
            if isinstance(value, str):
                # Match ${VAR_NAME} pattern
                matches = re.findall(r'\$\{([^}]+)\}', value)
                for var_name in matches:
                    env_value = os.environ.get(var_name, "")
                    value = value.replace(f"${{{var_name}}}", env_value)
                config[key] = value
            elif isinstance(value, dict):
                config[key] = self._substitute_env_vars(value)

        return config

    def _build_priority_order(self) -> None:
        """Build ordered list of providers by priority."""
        # Get providers with priority defined
        providers_with_priority = [
            (name, config.get("priority", 999))
            for name, config in self.providers.items()
            if config.get("enabled", False)
        ]

        # Sort by priority (lower number = higher priority)
        providers_with_priority.sort(key=lambda x: x[1])

        self.priority_order = [name for name, _ in providers_with_priority]

    def get_provider_config(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific provider.

        Args:
            provider_name: Name of the provider

        Returns:
            Provider configuration dictionary, or None if not found
        """
        return self.providers.get(provider_name)

    def is_provider_enabled(self, provider_name: str) -> bool:
        """
        Check if a provider is enabled.

        Args:
            provider_name: Name of the provider

        Returns:
            True if provider is enabled, False otherwise
        """
        provider_config = self.providers.get(provider_name, {})
        return provider_config.get("enabled", False)

    def get_enabled_providers(self) -> list[str]:
        """
        Get list of all enabled provider names.

        Returns:
            List of enabled provider names in priority order
        """
        return [
            name for name in self.priority_order
            if self.is_provider_enabled(name)
        ]

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate configuration.

        Checks:
        - At least one provider enabled
        - Required API keys present for enabled providers
        - Priority values are unique

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check at least one provider enabled
        if not self.get_enabled_providers():
            errors.append("No providers enabled in configuration")

        # Check API keys for enabled providers requiring them
        for provider_name in self.get_enabled_providers():
            config = self.providers[provider_name]

            # Check if provider requires API key
            if "api_key" in config:
                api_key = config["api_key"]
                if not api_key or api_key.startswith("${"):
                    errors.append(
                        f"Provider '{provider_name}' enabled but API key not set. "
                        f"Check environment variable."
                    )

        # Check priority uniqueness
        priorities = [
            config.get("priority")
            for config in self.providers.values()
            if "priority" in config
        ]
        if len(priorities) != len(set(priorities)):
            errors.append("Provider priorities must be unique")

        return (len(errors) == 0, errors)


# Global settings instance
settings = Settings()

# Global data sources config instance (lazy loaded)
_data_sources_config: Optional[DataSourcesConfig] = None


def get_data_sources_config() -> DataSourcesConfig:
    """
    Get data sources configuration (singleton pattern).

    Returns:
        DataSourcesConfig instance
    """
    global _data_sources_config

    if _data_sources_config is None:
        _data_sources_config = DataSourcesConfig()

    return _data_sources_config
