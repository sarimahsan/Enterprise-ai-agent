from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    
    # Database
    DATABASE_URL: Optional[str] = "sqlite:///./flowforge.db"
    
    # Notion (optional)
    NOTION_API_KEY: Optional[str] = None
    
    # Google (optional)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()