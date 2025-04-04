from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class PostBase(BaseModel):
    slug: str  | None= None 
    title: str | None = None
    desc: str | None = None
    content: str | None = None
    img: Optional[str] = None


class PostCreate(PostBase): 
    pass

class PostUpdate(PostBase):
    pass

class PostInDb(PostBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class Post(PostInDb):
    pass