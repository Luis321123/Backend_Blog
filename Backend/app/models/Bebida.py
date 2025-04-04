from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.BaseModel import BaseModel

class Bebida(BaseModel):
    __tablename__ = 'bebidas'

    uuid = Column(
        UUID(150), primary_key=True,  index=True, default=uuid4
    )   
    name = Column(String(255))
    coste = Column(Integer)
    status = Column(String(255))
    time_get = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True, default=None)

    notifications = relationship("Notification", back_populates="bebida")