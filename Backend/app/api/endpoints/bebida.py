from fastapi import APIRouter, Depends, Form, status
from typing import Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.bebidas import BebidasCreate, BebidasUpdate
from app.controllers.bebidas import bebida_controller

router = APIRouter()

@router.get('/bebida', status_code=status.HTTP_200_OK)
async def get_bebida(bebida_uuid: Optional[str] = None,session: Session = Depends(get_session)):
    disciplines = await bebida_controller.get_bebida(db=session,uuid=bebida_uuid)
    return disciplines

@router.post('/bebida', status_code=status.HTTP_201_CREATED)
async def create_bebida(data: BebidasCreate = Form(...), session: Session = Depends(get_session)):
    bebida = await bebida_controller.create_bebida(data=data, session=session)
    return bebida

@router.put('/bebida', status_code=status.HTTP_200_OK)
async def update_bebida(bebida_uuid: str, data:BebidasUpdate=Form(...), session: Session = Depends(get_session)):
    update = await bebida_controller.update_bebida(data=data, bebida_uuid=bebida_uuid, session=session)
    return update

@router.delete('/bebida',status_code=status.HTTP_200_OK)
async def delete_bebida(bebida_uuid: str, session: Session = Depends(get_session)):
    await bebida_controller.delete_bebida(bebida_uuid=bebida_uuid, session=session)
    return JSONResponse({'message': 'Your User has been deleted successfully'})