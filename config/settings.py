"""
Application settings and configuration.
"""

import os
from typing import Optional


class Settings:
    """Application settings."""

    # API Configuration
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Database Configuration
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return os.getenv(key, default)


settings = Settings()
