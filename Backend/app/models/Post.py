from uuid import uuid4
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.models.BaseModel import BaseModel

class Post(BaseModel):
    __tablename__ = 'posts'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )   
    slug = Column(String(255),nullable=True)
    title = Column(String, nullable=False)
    desc = Column(String(255),nullable=False)
    content = Column(String(255),nullable=True)
    img = Column(String(255),nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)
