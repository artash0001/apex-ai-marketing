"""
Apex AI Marketing - Settings Management

All configuration via environment variables, managed with pydantic-settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Database ──────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://apex:apex123@localhost:5432/apex_marketing"
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── AI Engine (Anthropic Claude) ──────────────────────────────────
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_MODEL: str = "claude-sonnet-4-20250514"
    PREMIUM_MODEL: str = "claude-opus-4-20250514"

    # ── Email (Resend) ────────────────────────────────────────────────
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "hello@apexaimarketing.pro"
    FROM_NAME: str = "Apex AI Marketing"

    # ── Authentication ────────────────────────────────────────────────
    JWT_SECRET: str = "change-this-to-a-random-secret-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 hours
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    # ── Telegram Notifications ────────────────────────────────────────
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # ── Website & Integrations ────────────────────────────────────────
    SITE_URL: str = "https://apexaimarketing.pro"
    CALENDLY_URL: str = "https://calendly.com/apex-ai-marketing"
    WEB3FORMS_KEY: str = ""

    # ── Brand Configuration ───────────────────────────────────────────
    BRAND_NAME: str = "Apex AI Marketing"
    BRAND_POSITIONING: str = "AI Growth Infrastructure for predictable pipeline."

    # ── Localization ──────────────────────────────────────────────────
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: List[str] = ["en", "ru"]

    # ── Market Configuration ──────────────────────────────────────────
    PRIMARY_MARKET: str = "dubai"
    TIMEZONE: str = "Asia/Dubai"
    WORK_DAYS: List[str] = ["sunday", "monday", "tuesday", "wednesday", "thursday"]

    # ── File Storage ──────────────────────────────────────────────────
    DELIVERABLES_DIR: str = "deliverables"
    STATIC_DIR: str = "static"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "case_sensitive": False,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
