from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

# Shared properties
class Rol(BaseModel):
    user_uuid: UUID4 = None
    name: str = None
    
# Properties to receive via API on creation
class RolCreated(Rol):
   pass

class RolUpdate(Rol):
    pass
    
class RolInDB(Rol):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

