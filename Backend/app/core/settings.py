import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App
    APP_NAME:  str = os.environ.get("APP_NAME", "projecto_prueba")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))

    # Frontend App
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:3000")

     # Backend App
    BACKEND_HOST: str = os.environ.get("BACKEND_HOST", "http://localhost:8000")
    
    # PostgreSQL Database Config
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")  
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")  
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")  
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT"))  
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")  
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Seeders of first user
    FIRST_ADMIN_EMAIL: str = os.environ.get("FIRST_ADMIN_EMAIL")
    FIRST_ADMIN_PASSWORD: str =  os.environ.get("FIRST_ADMIN_PASSWORD")
    FIRST_ADMIN_ACCOUNT_NAME: str = os.environ.get("FIRST_ADMIN_ACCOUNT_NAME")
    FIRST_ADMIN_ACCOUNT_LASTNAME: str = os.environ.get("FIRST_ADMIN_ACCOUNT_LASTNAME")

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()
