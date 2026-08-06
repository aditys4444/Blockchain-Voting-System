import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_TITLE: str = "Blockchain Voting System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "b4d7c71e9882a466184e909194e8200632a7e71b2d0fa3b8")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours for dev convenience
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 32-byte secret key for AES-256 GCM vote encryption
    VOTE_ENCRYPTION_KEY: str = os.getenv("VOTE_ENCRYPTION_KEY", "12345678901234567890123456789012")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./blockchain_voting.db")
    
    # Mining
    BLOCKCHAIN_DIFFICULTY: int = 2

    class Config:
        case_sensitive = True

settings = Settings()
