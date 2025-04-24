from uuid import uuid4
from sqlalchemy import Column, DateTime, String,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.BaseModel import BaseModel

class Roles(BaseModel):
    __tablename__= 'roles'

    uuid = Column(
        UUID(150), primary_key=True, index=True, default=uuid4
    )

    name = Column(String(50))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)

    #RELEACIONES
    users = relationship("User", back_populates="roles")
