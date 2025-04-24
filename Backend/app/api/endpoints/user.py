from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.controllers.user import user as user_controller
from app.schemas.user import UserCreate, UserUpdate

router= APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def user_create(data: UserCreate, session:Session = Depends(get_session)):
    user_create = await user_controller.create_user(user_data=data, db=session)
    return user_create

@router.get('/get/{user_uuid}', status_code=status.HTTP_200_OK)
async def user_get(user_uuid: str, session: Session = Depends(get_session)):
    user = await user_controller.get_user_by_uuid(db=session, uuid=user_uuid)
    return user

@router.get('/all', status_code=status.HTTP_200_OK)
async def user_all(session: Session = Depends(get_session)):
    users = await user_controller.get_all_users(db=session)
    return users

@router.put('/update/{user_uuid}', status_code=status.HTTP_200_OK)
async def user_update(user_uuid: str, data: UserUpdate, session: Session = Depends(get_session)):
    update = await user_controller.update_user(db=session, user_uuid=user_uuid, obj_in=data)
    return update

@router.delete('/delete/{user_uuid}', status_code=status.HTTP_200_OK)
async def user_delete(user_uuid: str, session: Session = Depends(get_session)):
    delete = await user_controller.delete_user(db=session, user_uuid=user_uuid)
    return delete