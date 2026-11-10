"""
IRONCORE Core Settings & Configuration.
12-Factor app principles with strong typing via Pydantic Settings.
"""
from typing import List, Optional
from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    PROJECT_NAME: str = "IRONCORE SaaS Platform"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"  # development, staging, production, testing

    # Security & Auth
    SECRET_KEY: str = "ironcore-super-secret-key-change-in-production-min-32-chars-long!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    COOKIE_DOMAIN: Optional[str] = None
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    # Initial Super Admin (Seeded securely)
    SUPERADMIN_EMAIL: EmailStr = "gowthamk81487@gmail.com"
    SUPERADMIN_PASSWORD: str = "IroncoreSuperAdmin#2026Pass!"
    SUPERADMIN_FULL_NAME: str = "Platform Super Admin"

    # Database
    # Default to sqlite+aiosqlite for local self-contained tests if Postgres is not spun up,
    # or PostgreSQL in standard deployment.
    DATABASE_URL: str = "postgresql+asyncpg://ironcore_user:ironcore_secure_pwd@localhost:5432/ironcore_db"
    DATABASE_URL_SYNC: str = "postgresql://ironcore_user:ironcore_secure_pwd@localhost:5432/ironcore_db"

    # Redis for distributed caching, rate-limiting, and sessions
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    # Razorpay (India Payment Gateway)
    RAZORPAY_KEY_ID: str = "rzp_test_ironcore_key"
    RAZORPAY_KEY_SECRET: str = "rzp_test_ironcore_secret"
    RAZORPAY_WEBHOOK_SECRET: str = "rzp_webhook_secret_ironcore"

    # Rate Limiting
    RATE_LIMIT_LOGIN_PER_MIN: int = 5
    RATE_LIMIT_DEFAULT_PER_MIN: int = 120

    # System Logs
    LOG_LEVEL: str = "INFO"


settings = Settings()
