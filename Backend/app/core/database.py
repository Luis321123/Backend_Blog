from typing import Generator, Optional
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
from .settings import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBConnectionManager:
    """
    Gestiona la conexión a MongoDB de manera similar al patrón de SQLAlchemy
    """
    _client: Optional[MongoClient] = None

    @classmethod
    def initialize(cls):
        """Inicializa la conexión global a MongoDB"""
        try:
            cls._client = MongoClient(
                settings.mongodb_uri,
                server_api=ServerApi('1'),
                connectTimeoutMS=10000,
                socketTimeoutMS=30000,
                tz_aware=True,  # Para manejo de timezone (similar a tu config de SQL)
                appname="FastAPI_App"  # Identificador de la aplicación
            )
            # Verificar conexión
            cls._client.admin.command('ping')
            logger.info("✅ Conexión a MongoDB establecida")
        except Exception as e:
            logger.error(f"❌ Error de conexión: {str(e)}")
            cls._client = None
            raise

    @classmethod
    def get_db(cls) -> Database:
        """
        Obtiene la instancia de la base de datos
        Similar a SessionLocal en SQLAlchemy
        """
        if cls._client is None:
            cls.initialize()
        return cls._client[settings.MONGODB_DBNAME]

    @classmethod
    def close_connection(cls):
        """Cierra la conexión global"""
        if cls._client:
            cls._client.close()
            cls._client = None
            logger.info("🔌 Conexión a MongoDB cerrada")

def get_db() -> Generator[Database, None, None]:
    """
    Función de dependencia para FastAPI
    Similar a get_session() en SQLAlchemy
    """
    try:
        db = MongoDBConnectionManager.get_db()
        yield db
    except Exception as e:
        logger.error(f"Error al obtener conexión a MongoDB: {str(e)}")
        raise

# Inicialización al importar el módulo
try:
    MongoDBConnectionManager.initialize()
except Exception as e:
    logger.critical(f"No se pudo establecer la conexión inicial con MongoDB: {str(e)}")