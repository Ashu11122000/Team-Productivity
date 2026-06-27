from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration for the Team Productivity Platform.
    
    Loads settings from the .env file and makes them available throughout the FastAPI Application.
    """
    APP_NAME: str = "Team Productivity Platform"
    APP_VERSION: str = "1.0.0"
    
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    API_V1_PREFIX: str = "/api/v1"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    JWT_ISSUER: str = "team-productivity-platform"
    JWT_AUDIENCE: str = "team-productivity-platform-users"
    
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default_factory = lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )
    
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    RATE_LIMIT_DEFAULT: str = "100/minute"
    OPEN_LIBRARY_BASE_URL: str = "https://openlibrary.org"
    
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@teamproductivity.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24
    
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    
    SENTRY_DSN: str = ""
    
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    MAX_UPLOAD_SIZE_MB: int = 25
    
    ALLOWED_IMAGE_EXTENSIONS: list[str] = Field(
        default_factory = lambda: [
            "jpg",
            "jpeg",
            "png",
            "webp",
            "svg",
        ]
    )
    
    ALLOWED_DOCUMENT_EXTENSIONS: list[str] = Field(
        default_factory = lambda: [
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
        ]
    )
    
    BCRYPT_ROUNDS: int = 12
    
    SECURE_COOKIES: bool = False
    SESSION_COOKIE_NAME: str = "tpp_session"
    
    ENABLE_REGISTRATION: bool = True
    ENABLE_BOOKS_API: bool = True
    ENABLE_EMAIL_VERIFICATION: bool = True
    ENABLE_NOTIFICATIONS: bool = False
    ENABLE_ANALYTICS: bool = False
    
    WEB_APP_URL: str = "http://localhost:3000"
    MOBILE_APP_SCHEME: str = "tpp://"
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
    )
    
settings = Settings()