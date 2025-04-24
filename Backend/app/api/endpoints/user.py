from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_session
from app.controllers.user import user as user_controller
from app.schemas.user import UserCreate  # Asegúrate de tener este schema
from app.api.deps import get_current_user  # Opcional para protección de ruta

router = APIRouter(prefix="/users", tags=["users"])

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user: Optional[dict] = Depends(get_current_user)  # Opcional si quieres proteger la ruta
):
    """
    Crea un nuevo usuario en el sistema
    
    Parámetros:
    - user_data: Datos del usuario a crear (email, password, etc.)
    - session: Sesión de base de datos
    - current_user: Usuario autenticado (opcional para rutas protegidas)
    
    Retorna:
    - El usuario creado en formato UserResponse
    """
    try:
        # Verifica si el usuario ya existe (implementa esta lógica en tu controller)
        existing_user = await user_controller.get_user_by_email(session, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crea el nuevo usuario
        new_user = await user_controller.create_user(
            user_data=user_data,  # Cambiado de 'data' a 'user_data' para más claridad
            session=session
        )
        
        return new_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )