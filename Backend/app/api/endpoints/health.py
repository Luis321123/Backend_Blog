from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pymongo.database import Database
from app.core.database import MongoDBConnectionManager, get_db
from app.core.settings import settings
import logging

router = APIRouter(tags=["Health Check"])
logger = logging.getLogger(__name__)

@router.get("/health", summary="Verifica el estado del servicio y la conexión a MongoDB")
async def health_check(db: Database = Depends(get_db)):
    """
    Realiza una comprobación completa del estado del servicio:
    - Verifica conexión a MongoDB
    - Obtiene información básica del servidor
    - Confirma acceso a la base de datos configurada
    """
    try:
        # Verificación 1: Ping al servidor
        ping_result = db.command('ping')
        if ping_result.get('ok') != 1:
            raise HTTPException(
                status_code=503,
                detail="El servidor MongoDB no respondió correctamente al ping"
            )
        
        # Verificación 2: Obtener información del servidor
        server_info = db.command('serverStatus')
        
        # Verificación 3: Listar colecciones (para confirmar acceso a la DB)
        collections = db.list_collection_names()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "db": {
                    "name": settings.MONGODB_DBNAME,
                    "status": "connected",
                    "version": server_info["version"],
                    "collections_count": len(collections)
                },
                "system": {
                    "mongodb_uri": settings.mongodb_uri.replace(settings.MONGODB_PASS, "***"),  # Ocultamos la contraseña
                    "cluster": settings.MONGODB_CLUSTER
                }
            }
        )
        
    except HTTPException:
        raise  # Re-lanzamos las excepciones HTTP que ya manejamos
        
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "suggestion": "Verifique la conexión a MongoDB y las credenciales en .env"
            }
        )