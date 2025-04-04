from fastapi import APIRouter, Depends, Form, status
from typing import Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.posts import PostCreate, PostUpdate
from app.controllers.posts import post_controller

router = APIRouter()

@router.get('/post', status_code=status.HTTP_200_OK)
async def get_post(post_uuid: Optional[str] = None,session: Session = Depends(get_session)):
    posts = await post_controller.get_post(db=session,uuid=post_uuid)
    return posts

@router.get('/posts', status_code=status.HTTP_200_OK)
async def get_all_posts(session: Session = Depends(get_session)):
    posts = await post_controller.get_all_posts(db=session)
    return posts

@router.post('/post', status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate = Form(...), session: Session = Depends(get_session)):
    post = await post_controller.create_post(data=data, session=session)
    return post

@router.put('/post', status_code=status.HTTP_200_OK)
async def update_a_post(post_uuid: str, data: PostUpdate = Form(...), session: Session = Depends(get_session)):
    update = await post_controller.update_post(data=data, post_uuid=post_uuid, session=session)
    return update

@router.delete('/post',status_code=status.HTTP_200_OK)
async def delete_post(post_uuid: str, session: Session = Depends(get_session)):
    await post_controller.delete_post(post_uuid=post_uuid, session=session)
    return JSONResponse({'message': 'Your post has been deleted successfully'})