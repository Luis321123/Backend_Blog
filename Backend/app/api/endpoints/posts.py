from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.post import PostCreate, PostUpdate, PostInDb 
from app.core.database import get_db
from app.controllers.posts import PostController

router = APIRouter()

@router.post("/", response_model=PostInDb, status_code=status.HTTP_201_CREATED)
async def create_bebida(post: PostCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    controller = PostController(db)
    try:
        return await controller.create(post)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear bebida: {str(e)}"
        )

@router.get("/", response_model=list[PostInDb])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncIOMotorDatabase = Depends(get_db)):

    controller = PostController(db)
    try:
        return await controller.get_all(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los posts: {str(e)}"
        )

@router.get("/{post_id}", response_model=PostInDb)
async def read_post(post_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):

    controller = PostController(db)
    try:
        post = await controller.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="post no encontrada"
            )
        return post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener bebida: {str(e)}"
        )

@router.put("/{post_id}", response_model=PostInDb)
async def update_post(
    post_id: str,
    post: PostUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)): 

    controller = PostController(db)
    try:
        update_post = await controller.update(post_id, post)
        if not update_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post no encontrado"
            )
        return update_post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar bebida: {str(e)}"
        )

@router.delete("/{post_update}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):

    controller = PostController(db)
    try:
        success = await controller.soft_delete(post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="post no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el post : {str(e)}"
        )