from typing import Literal

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings for the Team Productivity Platform.

    Loads configuration from the .env file and provides strongly typed,
    validated settings throughout the application.
    """

    APP_NAME: str = "Team Productivity Platform"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Modern Team Productivity Platform API"

    ENVIRONMENT: Literal["development", "testing", "staging", "production"] = (
        "development"
    )
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    JWT_ISSUER: str = "team-productivity-platform"
    JWT_AUDIENCE: str = "team-productivity-platform-users"

    PASSWORD_HASH_ALGORITHM: str = "argon2"

    SECRET_KEY: str = "change-this-secret"

    BCRYPT_ROUNDS: int = 12

    SECURE_COOKIES: bool = False

    SESSION_COOKIE_NAME: str = "tpp_session"
    ACCESS_COOKIE_NAME: str = "tpp_access_token"
    REFRESH_COOKIE_NAME: str = "tpp_refresh_token"

    MAX_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCK_MINUTES: int = 15

    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=list)

    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    CACHE_ENABLED: bool = True

    RATE_LIMIT_DEFAULT: str = "100/minute"

    OPEN_LIBRARY_BASE_URL: str = "https://openlibrary.org"

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@teamproductivity.com"

    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    EMAIL_ENABLED: bool = False

    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24

    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False

    SENTRY_DSN: str = ""

    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    UPLOAD_DIR: str = "uploads"
    STATIC_DIR: str = "static"
    MEDIA_DIR: str = "media"

    MAX_UPLOAD_SIZE_MB: int = 25

    ALLOWED_IMAGE_EXTENSIONS: list[str] = Field(default_factory=list)
    ALLOWED_DOCUMENT_EXTENSIONS: list[str] = Field(default_factory=list)

    ENABLE_REGISTRATION: bool = True
    ENABLE_BOOKS_API: bool = True
    ENABLE_EMAIL_VERIFICATION: bool = False
    ENABLE_NOTIFICATIONS: bool = False
    ENABLE_ANALYTICS: bool = False

    ENABLE_SWAGGER: bool = True
    ENABLE_REDOC: bool = True

    OPENAPI_URL: str = "/openapi.json"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    DEFAULT_LANGUAGE: str = "en"
    TIMEZONE: str = "Asia/Kolkata"

    REQUEST_TIMEOUT: int = 30

    WEB_APP_URL: str = "http://localhost:3000"
    MOBILE_APP_SCHEME: str = "tpp://"

    STORAGE_PROVIDER: str = "local"

    @field_validator(
        "BACKEND_CORS_ORIGINS",
        "ALLOWED_IMAGE_EXTENSIONS",
        "ALLOWED_DOCUMENT_EXTENSIONS",
        mode="before",
    )
    @classmethod
    def split_comma_separated_values(cls, value):
        """
        Convert comma-separated strings from .env into Python lists.
        """
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @computed_field
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @computed_field
    @property
    def database_url_safe(self) -> str:
        """
        Returns a masked database URL for logging.
        """
        if "@" not in self.DATABASE_URL:
            return self.DATABASE_URL

        protocol, remainder = self.DATABASE_URL.split("://", 1)

        if "@" not in remainder:
            return self.DATABASE_URL

        credentials, host = remainder.split("@", 1)

        if ":" in credentials:
            username = credentials.split(":")[0]
            credentials = f"{username}:********"

        return f"{protocol}://{credentials}@{host}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()