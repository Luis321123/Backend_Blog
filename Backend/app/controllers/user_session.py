from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.base import CRUDBase
from app.models.UserSessions import UserSession
from app.schemas.user_session import UserSessionCreate


class UserSessionController(CRUDBase[UserSession, UserSessionCreate, UserSessionCreate]):
    async def create_user_session(self, session: Session, obj_in: UserSessionCreate):
        try:
            self.create(db=session, obj_in=obj_in)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

    async def remove_user_session(self, user_uuid:str, session: Session):
            try:
                self.remove(db=session, uuid=user_uuid)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

user_session = UserSessionController(UserSession)
