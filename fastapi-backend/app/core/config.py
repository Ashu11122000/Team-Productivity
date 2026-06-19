# BaseSettings automatically reads environment variables
# SettingsConfigDict is used to define configuration behaviors for a BaseSettings model
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This configuration is shared across:
    - Authentication
    - Notes Module
    - Open Library Integration
    - NestJS Service Integration
    - JWT Security
    """
    # Application
    APP_NAME: str = "Team Productivity Platform API"
    APP_VERSION: str = "v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Shared JWT metadata for FastAPI + NestJS
    JWT_ISSUER: str = "team-productivity-platform"
    JWT_AUDIENCE: str = "team-productivity-users"
    
    # NestJS Integration
    # NestJS owns:
    # - Tasks
    # - Categories
    # - Tags
    # - Notifications
    # - Analytics
    # - Activity Logs
    
    NESTJS_API_URL: str = "http://localhost:3001/api/v1"
    
    # Open Library Integration
    OPEN_LIBRARY_BASE_URL: str = "https://openlibrary.org"
    
    # Public Holidays API
    HOLIDAYS_API_BASE_URL: str = (
        "https://date.nager.at/api/v3"
    )
    
    # API Configuration
    API_V_PREFIX: str = "/api/v1"
    
    # Environment Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )
    
    # Computed Database URL
    @property
    def DATABASE_URL(self) -> str:
        """
        SQLAlchemy connection string (Database URL) that SQLAlchemy uses to connect to database
        """
        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )
        
settings = Settings()