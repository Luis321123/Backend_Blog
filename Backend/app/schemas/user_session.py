from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

# Shared properties
class UserSessionBase(BaseModel):
    user_uuid: UUID4 = None
    token: str = None

# Properties to receive via API on creation
class UserSessionCreate(UserSessionBase):
    pass
    
class UserInDB(UserSessionBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class UserSession(UserInDB):
    pass
