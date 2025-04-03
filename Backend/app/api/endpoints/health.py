from fastapi import APIRouter, HTTPException
from app.core.database import mongodb
from app.core.settings import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    if not mongodb.client:
        raise HTTPException(
            status_code=503,
            detail="Servicio no disponible - Error de base de datos"
        )
    
    try:
        db = mongodb.get_db()
        server_info = db.command("serverStatus")
        return {
            "status": "healthy",
            "db_version": server_info["version"],
            "db_name": settings.MONGODB_DBNAME
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )