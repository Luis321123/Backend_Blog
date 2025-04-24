from datetime import datetime, date
from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr
from sqlalchemy import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class UserBase(BaseModel):
    username: str = None
    last_name: str = None
    is_active: bool = True
    is_superuser: bool = False
    email: EmailStr = None
    birth: date | None = None
    phone: str = None
    address: str = None
    gender: str = None 
    
# Properties to receive via API on creation
class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    pass

class UserInDB(UserBase):
    uuid: UUID4
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDB):
    pass
