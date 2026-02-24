from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://apex:apex123@localhost:5432/apex_digital"
    redis_url: str = "redis://localhost:6379"

    # AI — Kimi API (OpenAI-compatible)
    kimi_api_key: str = ""
    kimi_base_url: str = "https://api.moonshot.cn/v1"
    default_model: str = "kimi-k2.5"
    premium_model: str = "kimi-k2.5"

    # Email (Resend)
    resend_api_key: str = ""
    from_email: str = "hello@apexdigital.ai"
    from_name: str = "APEX Digital"

    # Auth
    jwt_secret: str = "your-secret-key-change-this"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    admin_username: str = "admin"
    admin_password: str = "admin123"

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Website
    site_url: str = "https://apexdigital.ai"
    api_url: str = "http://localhost:8000"

    # Agency Branding
    agency_name: str = "APEX Digital"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()
