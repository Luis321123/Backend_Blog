from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.posts import PostCreate,PostUpdate
from app.services.base import CRUDBase
from app.models.Post import Post
from app.responses.posts import post_response_create, post_response_get

class PostController(CRUDBase[Post, PostCreate, PostUpdate]): 
    async def get_post(self, db: Session, uuid: str = None):
        query = db.query(self.model).filter(self.model.deleted_at == None)
        
        if uuid:
            post_current = query.filter(self.model.uuid == uuid).first()
            if not post_current:
                raise HTTPException(status_code=404, detail="Post UUID not found.")
            return post_current 
        

    async def get_all_posts(self, db: Session, skip: int = 0, limit: int = 100):
        query = db.query(self.model).filter(self.model.deleted_at == None)
        return query.offset(skip).limit(limit).all()
            
    async def create_post(self, data: PostCreate, session: Session):
        try:
            post_current = self.create(db=session, obj_in=data)
            return post_response_create(post_current)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")
    
    async def update_post(self, data: PostUpdate, post_uuid: str, session: Session):
        try:
            post_current = await self.get_post(db=session, uuid=post_uuid)
            if not post_current:
                raise HTTPException(status_code=404, detail="uuid of post not found.")
            
            post_update=self.update(db=session, db_obj=post_current, obj_in=data)
            return post_update
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    
    async def delete_post(self, post_uuid:str, session: Session):
        try:
            self.get(session, post_uuid)
            self.remove(db=session, uuid=post_uuid)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

post_controller=PostController(Post)