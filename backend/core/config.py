from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Core LLM
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    
    # Lead Generation
    APOLLO_API_KEY: str = ""
    HUNTER_API_KEY: str = ""
    
    # Email & Outreach
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = ""
    
    # Calendar & Meetings
    GOOGLE_CALENDAR_CREDENTIALS_PATH: str = ""
    GOOGLE_CALENDAR_EMAIL: str = ""
    
    # SMS & Voice
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # LinkedIn
    LINKEDIN_API_KEY: str = ""
    LINKEDIN_OAUTH_TOKEN: str = ""
    
    # CRM
    SALESFORCE_CLIENT_ID: str = ""
    SALESFORCE_CLIENT_SECRET: str = ""
    SALESFORCE_INSTANCE_URL: str = ""
    HUBSPOT_API_KEY: str = ""
    
    # Database (optional, for future use)
    DATABASE_URL: str = "sqlite:///./flowforge.db"
    
    # App Settings
    APP_ENV: str = "development"
    API_PORT: int = 8000

settings = Settings()