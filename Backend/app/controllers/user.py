from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models.User import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import CRUDBase
from app.core.security import is_password_strong_enough

class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_user_by_uuid(self, db: Session, uuid: str) -> User | None:
        try:
            user = db.query(self.model).filter(self.model.uuid == uuid).filter(self.model.is_active == True).first()
            if not user:
                raise HTTPException(status_code=404, detail="usuario no encontrado o ha sido eliminado.")       
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuario: {str(e)}"
            )
        return user

    async def create_user(self, db: Session, user_data: UserCreate) -> User:
        try:
            if not is_password_strong_enough(user_data.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, números y caracteres especiales"
                )
            
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )

            new_user =self.create(db=db, obj_in=user_data)
                 
            return new_user
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear usuario: {str(e)}"
            )

    async def get_all_users(self, db: Session, skip: int = 0, limit: int = 100):
        try:
            query = db.query(self.model).offset(skip).limit(limit)
            return query.all()
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuarios: {str(e)}"
            )
        
    async def update_user(self, db: Session, user_uuid: str, obj_in: UserUpdate):
        try:
            user_current = await self.get_user_by_uuid(db=db, uuid=user_uuid)
            if not user_current:
                raise HTTPException(status_code=404, detail="uuid of user not found.")
            
            self.update(db=db, db_obj=user_current, obj_in=obj_in)
            return user_current
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar usuario: {str(e)}"
            )
        
    async def delete_user(self, db: Session, user_uuid: str):
        try:
            user = await self.get_user_by_uuid(db=db, uuid=user_uuid)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado")
            self.remove(db=db, uuid=user_uuid)
            return f"Usuario {user.username} eliminado exitosamente"
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar usuario: {str(e)}"
            )
    
user = UserController(User)