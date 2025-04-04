from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.objectid import PyObjectId

class MongoDBModel(BaseModel):
    """
    Modelo base para MongoDB con soporte para:
    - ObjectId (_id)
    - Timestamps
    - Soft delete
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    def soft_delete(self):
        """Marca el documento como eliminado"""
        self.deleted_at = datetime.utcnow()

    def is_deleted(self) -> bool:
        """Verifica si el documento está marcado como eliminado"""
        return self.deleted_at is not None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}