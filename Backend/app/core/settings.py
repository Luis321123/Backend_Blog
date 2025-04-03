from pydantic_settings import BaseSettings
from pathlib import Path
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # MongoDB
    MONGODB_USER: str
    MONGODB_PASS: str
    MONGODB_CLUSTER: str
    MONGODB_DBNAME: str = "blogdb"
    
    @property
    def mongodb_uri(self) -> str:
        """Genera la URI de conexión de forma segura"""
        return (
            f"mongodb+srv://{self.MONGODB_USER}:"
            f"{quote_plus(self.MONGODB_PASS)}@"
            f"{self.MONGODB_CLUSTER}/"
            f"{self.MONGODB_DBNAME}?"
            "retryWrites=true&w=majority&appName=BlogDatabase"
        )
    
    class Config:
        # Busca el .env en el directorio padre
        env_file = Path(__file__).parent.parent.parent / ".env"
        env_file_encoding = 'utf-8'

# Instancia singleton
settings = Settings()