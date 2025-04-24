from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.token import Token
from app.schemas.user import User
from app.controllers.auth import AuthController
from app.core.database import get_session
from app.core.settings import get_settings
from app.api.deps import get_current_user

settings=get_settings()

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    auth_controller = AuthController(db)
    user = auth_controller.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_controller.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me",)
async def read_users_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    auth_controller = AuthController(db)
    role = auth_controller.get_current_user_role(current_user)
    
    return role
    