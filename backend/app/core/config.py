"""
Configuration management using Pydantic Settings.
Loads from environment variables with validation.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    See .env.example for all available options.
    """

    # General
    PROJECT_NAME: str = "AudioRepurpose"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # Frontend URL for CORS
    FRONTEND_URL: str = "http://localhost:3000"

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Returns list of allowed CORS origins"""
        return [
            self.FRONTEND_URL,
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://audiorepurpose:changeme@localhost:5432/audiorepurpose_db"
    )

    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_WORKER_CONCURRENCY: int = 2
    CELERY_TASK_TIME_LIMIT: int = 1800  # 30 minutes

    # JWT Authentication
    SECRET_KEY: str = Field(
        default="your-super-secret-key-change-this-in-production-min-32-chars"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # OpenAI
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_TRANSCRIPTION_MODEL: str = "whisper-1"
    OPENAI_CHAT_MODEL: str = "gpt-4-turbo-preview"

    @validator("OPENAI_API_KEY")
    def validate_openai_key(cls, v: str) -> str:
        """Warn if OpenAI key is not set"""
        if not v or v == "":
            print("WARNING: OPENAI_API_KEY not set. AI features will not work.")
        return v

    # Storage (MinIO / S3)
    STORAGE_TYPE: str = "minio"  # "minio" or "s3"

    # MinIO settings
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ROOT_USER: str = "minioadmin"
    MINIO_ROOT_PASSWORD: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "audiorepurpose"
    MINIO_USE_SSL: bool = False

    # AWS S3 settings
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None

    # File upload limits
    MAX_FILE_SIZE_MB_FREE: int = 50
    MAX_FILE_SIZE_MB_PRO: int = 200
    ALLOWED_AUDIO_EXTENSIONS: str = "mp3,wav,m4a,ogg,flac"

    @property
    def ALLOWED_EXTENSIONS_LIST(self) -> List[str]:
        """Returns list of allowed file extensions"""
        return [ext.strip() for ext in self.ALLOWED_AUDIO_EXTENSIONS.split(",")]

    @property
    def MAX_FILE_SIZE_BYTES_FREE(self) -> int:
        """Max file size in bytes for free tier"""
        return self.MAX_FILE_SIZE_MB_FREE * 1024 * 1024

    @property
    def MAX_FILE_SIZE_BYTES_PRO(self) -> int:
        """Max file size in bytes for pro tier"""
        return self.MAX_FILE_SIZE_MB_PRO * 1024 * 1024

    # Usage limits (Freemium)
    FREE_TIER_MONTHLY_UPLOADS: int = 3
    PRO_TIER_MONTHLY_UPLOADS: int = 999999

    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRO_PRICE_ID: Optional[str] = None

    # Email (optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@audiorepurpose.com"

    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
