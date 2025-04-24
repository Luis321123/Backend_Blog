from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import BackgroundTasks, HTTPException
from app.core.security import hash_password, verify_password
from app.models.User import User
from app.models.UserSessions import UserSession
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import CRUDBase
from app.controllers.user_session import user_session as user_session_controller
from app.services.jwt import _generate_tokens

class AuthController(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: Session, *, email: str):
        return db.query(self.model).filter(User.email == email).first()
    
    async def post_login_token(self, db: Session, obj_in: OAuth2PasswordRequestForm):
        try:
            user = await self.get_by_email(db=db, email=obj_in.username)
            
            if not user:
                raise HTTPException(status_code=404, detail="El correo electrónico no está registrado")
           
            if not verify_password(obj_in.password, user.hashed_password):
                raise HTTPException(status_code=401, detail="Contraseña inválida")
            
            response = _generate_tokens(user)
            
            # Registrar sesión (opcional)
            db_obj_in = {
                "user_id": user.id,
                "token": response.get("access_token")
            }
            await user_session_controller.create_user_session(session=db, obj_in=db_obj_in)
            
            return response
            
        except HTTPException:
            raise
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Error en el inicio de sesión: {str(ex)}")
   
    async def post_logout_user(self, db: Session, current_user: User, request: Request):
        try:
            data_session = db.query(UserSession).filter(
                UserSession.user_id == current_user.id,
                UserSession.token == request.headers.get("Authorization").split()[1]
            ).first()
            
            if data_session:
                user_session_controller.remove_user_session(session=db, session_id=data_session.id)
                
            return {"message": "Sesión cerrada exitosamente"}
            
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Error al cerrar sesión: {str(ex)}")

    #async def forgot_password(self, email: str, db: Session, background_tasks: BackgroundTasks):
       # try:
         #   user = await self.get_by_email(db=db, email=email)
           # if not user:
         #       return  # Por seguridad no revelamos si el email existe
         #       
         #   await send_password_reset_email(user=user, background_tasks=background_tasks)
            
        #except Exception as ex:
         #   raise HTTPException(status_code=500, detail=f"Error al procesar solicitud: {str(ex)}")

   # async def reset_password(self, obj_in: PasswordReset, db: Session):
    #    try:
   #         user = await self.get_by_email(db=db, email=obj_in.email)
     #       if not user:
     #           raise HTTPException(status_code=404, detail="Usuario no encontrado")

        #    # Verificar token (implementación básica)
      #      token_valid = verify_password(user.get_reset_token(), obj_in.token)
      #      if not token_valid:
       #         raise HTTPException(status_code=400, detail="Token inválido o expirado")
            
         #   # Actualizar contraseña
         #   user.hashed_password = hash_password(obj_in.password)
       #     db.commit()

        #    return {"message": "Contraseña actualizada exitosamente"}

        except HTTPException:
            raise
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar contraseña: {str(ex)}")

auth = AuthController(User)