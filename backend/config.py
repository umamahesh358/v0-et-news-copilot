"""Configuration settings for ET News Copilot backend"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # API Keys
    groq_api_key: Optional[str] = None
    
    # Text Processing Configuration
    chunk_size: int = 512
    chunk_overlap: int = 50
    
    # Feature Flags
    enable_related_articles: bool = True
    enable_qa: bool = True
    enable_insights: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
