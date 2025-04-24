from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user  # Cambiado de get_current_church_user
from app.core.database import get_session
from app.controllers.auth import auth as auth_controller
#from app.schemas.auth_schemas import PasswordResetRequest, PasswordReset
from app.schemas.user import UserInDB  # Cambiado de ChurchUserInDB

router = APIRouter()

@router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """Autenticación básica con username/password"""
    data_in = await auth_controller.post_login_token(db=session, obj_in=data)
    return JSONResponse(data_in)

@router.put("/logout", status_code=status.HTTP_200_OK)
async def user_logout(
    session: Session = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user)  # Cambiado de church_user
):
    """Cierre de sesión"""
    await auth_controller.post_logout_user(db=session, user=current_user)
    return JSONResponse(content='Sesión cerrada correctamente')

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
#async def forgot_password(
 #   data: PasswordResetRequest,
  #  background_tasks: BackgroundTasks,
   # db: Session = Depends(get_session)
#):
   # """Solicitud de recuperación de contraseña"""
 #   await auth_controller.forgot_password(
  #      email=data.email,
   #     db=db,
    #    background_tasks=background_tasks
    #)
    #return JSONResponse(content='Se ha enviado un correo para restablecer la contraseña')

#@router.put("/reset-password", status_code=status.HTTP_200_OK)
#async def reset_password(
 #   obj_in: PasswordReset,
  #  session: Session = Depends(get_session)
#):
#    """Restablecimiento de contraseña"""
 #   await auth_controller.reset_password(obj_in=obj_in, db=session)
  #  return JSONResponse(content='Contraseña actualizada correctamente')

class GoogleToken(BaseModel):
    token: str

@router.post("/login/google", status_code=status.HTTP_200_OK)
async def login_google(
    token_data: GoogleToken,
    db: Session = Depends(get_session)
):
    """Autenticación con Google (versión simplificada)"""
    try:
        response = await auth_controller.google_login(
            token=token_data.token,
            db=db
        )
        return JSONResponse(response)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en autenticación con Google: {str(e)}"
        )