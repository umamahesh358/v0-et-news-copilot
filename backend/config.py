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
    GROQ_API_KEY: Optional[str] = None  # Alternative uppercase name
    
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
    
    def get_groq_key(self) -> str:
        """Get GROQ API key with fallback"""
        return self.GROQ_API_KEY or self.groq_api_key or ""


# Create settings instance
settings = Settings()

# Ensure GROQ_API_KEY is available
if not settings.GROQ_API_KEY and settings.groq_api_key:
    settings.GROQ_API_KEY = settings.groq_api_key
