from typing import Optional
from sqlalchemy.orm import Session

from app.services.base import CRUDBase
from app.schemas.user import UserInDB
from app.models.User import User as UserModel

class ServiceUser(CRUDBase[UserModel]):
    def get_by_name(self, db: Session, name: str) -> Optional[UserInDB]:
        return db.query(self.model).filter(self.model.name == name).first()

user = ServiceUser(UserModel)