	
"""# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server
    PORT: int = 8000
    FRONTEND_URL: str = 'http://localhost:3000'

    # Database
    DATABASE_URL: str

    # AI
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = 'gemini-2.5-flash'

    # Email
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASS: str          # Gmail App Password
    EMAIL_FROM_NAME: str = 'QualyX Sales'

    # WhatsApp
    WHATSAPP_TOKEN: str = ''
    WHATSAPP_PHONE_ID: str = ''
    WHATSAPP_VERIFY_TOKEN: str = ''

    # Google Calendar
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''

    # n8n
    N8N_SECRET: str = ''

    class Config:
        env_file = '.env'

settings = Settings()"""

# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Server
    PORT: int = 8000
    FRONTEND_URL: str = 'http://localhost:3000'

    # Database (separate params — matches your .env)
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 5432

    # AI
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = 'gemini-2.5-flash-lite'

    # Email (optional for now)
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    EMAIL_FROM_NAME: str = 'QualyX Sales'

    # WhatsApp (optional for now)
    WHATSAPP_TOKEN: str = ''
    WHATSAPP_PHONE_ID: str = ''
    WHATSAPP_VERIFY_TOKEN: str = ''

    # Google Calendar (optional for now)
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''

    # n8n (optional for now)
    N8N_SECRET: str = ''

    # Add these to your Settings class
    SUPABASE_JWT_SECRET: str = ''
    SUPABASE_URL: str = ''

    class Config:
        env_file = '.env'
        extra = 'ignore'  # Ignore any extra fields in .env

settings = Settings()
