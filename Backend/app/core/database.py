from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .settings import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_connection()
        return cls._instance

    def init_connection(self):
        try:
            self.client = MongoClient(
                settings.mongodb_uri,
                server_api=ServerApi('1'),
                connectTimeoutMS=10000,
                socketTimeoutMS=30000
            )
            self.client.admin.command('ping')
            logger.info("✅ Conexión a MongoDB establecida")
        except Exception as e:
            logger.error(f"❌ Error de conexión: {str(e)}")
            self.client = None

    def get_db(self):
        return self.client[settings.MONGODB_DBNAME]

# Instancia global
mongodb = MongoDBConnection()