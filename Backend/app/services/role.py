from typing import Optional
from sqlalchemy.orm import Session

from app.services.base import CRUDBase
from app.schemas.role import RolInDB, RolCreated, RolUpdate
from app.models.Roles import Roles as RolesModel

class ServicesRole(CRUDBase[RolesModel, RolCreated, RolUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[RolInDB]:
        return db.query(self.model).filter(self.model.name == name).first()

role = ServicesRole(RolesModel)