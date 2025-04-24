from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.core.security import is_password_strong_enough
from app.models.User import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import CRUDBase

# Configuración para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    async def create_user(self, user_data: UserCreate, session: Session):
        """
        Crea un nuevo usuario en el sistema con contraseña hasheada
        
        Args:
            user_data (UserCreate): Datos del usuario a crear
            session (Session): Sesión de base de datos
            
        Returns:
            User: El usuario creado
            
        Raises:
            HTTPException: Si el password no es seguro o el email ya existe
        """
        try:
            # Verificar si el usuario ya existe
            existing_user = session.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
            
            # Validar fortaleza de la contraseña
            if not is_password_strong_enough(user_data.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, números y caracteres especiales"
                )
            
            # Hashear la contraseña
            hashed_password = pwd_context.hash(user_data.password)
            
            # Crear el objeto usuario
            db_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                username=user_data.username,
                is_active=True,
                is_superuser=False  # Por defecto no es superusuario
            )
            
            # Guardar en base de datos
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            
            return db_user
            
        except HTTPException:
            raise  # Re-lanzamos las excepciones HTTP que ya habíamos capturado
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el usuario: {str(e)}"
            )

    async def get_user_by_email(self, session: Session, email: str) -> User | None:
        """Obtiene un usuario por su email"""
        return session.query(User).filter(User.email == email).first()

user = UserController(User)