from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import get_token_user
from app.models.User import User

message_not_authorised = 'Not authorised, consult an administrator'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    request: Request, 
    optional_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_session)
) -> User:
    """
    Obtiene el usuario actual a partir del token JWT.
    Busca primero en cookies (access_token) y luego en el header Authorization.
    """
    token = request.cookies.get('access_token')
    if token:
        user = await get_token_user(token=token, db=db)
    elif optional_token:
        user = await get_token_user(token=optional_token, db=db)
    else:
        raise HTTPException(status_code=401, detail=message_not_authorised)
    
    if not user:
        raise HTTPException(status_code=401, detail=message_not_authorised)
    
    return user

async def get_current_admin(
    request: Request, 
    optional_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_session)
) -> User:
    """
    """
    user = await get_current_user(request=request, optional_token=optional_token, db=db)

    if not user.is_admin:  # Asumiendo que tu modelo User tiene un campo is_admin
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user

async def get_current_superuser(
    request: Request, 
    optional_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_session)
) -> User:
    """
    Obtiene el usuario actual y verifica que sea superusuario.
    """
    user = await get_current_user(request=request, optional_token=optional_token, db=db)
    
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser access required")
    
    return user