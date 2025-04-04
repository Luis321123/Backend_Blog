from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class BebidasBase(BaseModel):
    slug: str  | None= None 
    title: str | None = None
    desc: str | None = None
    content: int | None = None
    img: Optional[str] = None


class BebidasCreate(BebidasBase):
    pass

class BebidasUpdate(BebidasBase):
    pass

class BebidasInDb(BebidasBase):
    uuid: UUID4
    created_at: datetime = None
    deleted_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class Bebidas(BebidasInDb):
    pass