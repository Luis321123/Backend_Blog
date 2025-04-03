from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BusinessUnitBase(BaseModel):
    id: str  | None= None 
    create_at: Optional[datetime] = None
    slug: bool = False 
    tittle: str
    desc: str
    content: str
    img: Optional[str] = None

class BusinessUnitCreate(BusinessUnitBase):
    pass

class BusinessUnitUpdate(BusinessUnitBase):
    pass

class BusinessUnitInDB(BusinessUnitBase):
    uuid: str
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True
        
class BusinessUnit(BusinessUnitInDB):
    pass
