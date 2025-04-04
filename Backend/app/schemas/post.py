from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.objectid import PyObjectId  # Usaremos el mismo tipo personalizado que vimos antes
from uuid import uuid4


class PostBase(BaseModel):
    name: str = Field(None, min_length=1, max_length=255)
    title: str = Field(None,min_length=1, max_length=100)  # ge=0 para valores positivos
    desc: str = Field(None, min_length=1)
    image_url: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostInDb(PostBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    deleted_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    

class Post(PostInDb):
    pass